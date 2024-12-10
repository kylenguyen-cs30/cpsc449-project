import random
import logging
import re


from flask import Blueprint, request, jsonify, session
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.database_model import User, PublicCrum, PrivateCrum
from app.mysql_connection import db

logger = logging.getLogger(__name__)

# Inventories Container
inventories = {}


# inventory_item id
inventory_id_counter = 1


# -------------------------------------------------------------#
# NOTE: For Public

# Crumbs Container -- do i delete this?
crumbls_public = [
    {
        "name": "Chocolate Chip",
        "description": "The classic chocolate chip cookie",
        "quantity": 65,
        "price": 4.99,
        "ID": 20,
    },
    {
        "name": "Confetti Milk Shake",
        "description": "A confetti sugar cookie rolled in rainbow sprinkles and topped with cake-flavored buttercream and a dollop of whipped cream",
        "quantity": 23,
        "price": 4.99,
        "ID": 46,
    },
    {
        "name": "Kentucky Butter Cake",
        "description": "A yellow butter cake cookie smothered with a melt-in-your-mouth buttery glaze.",
        "quantity": 12,
        "price": 4.99,
        "ID": 26,
    },
    {
        "name": "Pink Velvet Cake Cookie",
        "description": "A velvety cake batter cookie topped with a layer of vanilla cream cheese frosting and pink velvet cookie crumbs.",
        "quantity": 7,
        "price": 4.99,
        "ID": 63,
    },
]
# crumb_id
crumbl_id_public = 1

# NOTE: For Private

# crumb_id
crumb_id_private = 1
# -------------------------------------------------------------#


crumbl_blueprint = Blueprint("crumbl_blueprint", __name__)


@crumbl_blueprint.route("/", methods=["GET"])
def home():
    return jsonify("Crumbl Backend Online!")


# NOTE: Middleware for login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in to access this route"}), 403

        try:
            # verify user still exists in database
            user = User.query.get(session["user_id"])

            if not user:
                session.clear()
                return jsonify({"error": "User not found"}), 401

            # Check if session has expired
            if "last_activity" in session:
                last_activity = datetime.fromtimestamp(session["last_activity"])
                if datetime.now() - last_activity > timedelta(hours=24):
                    session.clear()  # Fixed typo: was session.clears()
                    return (
                        jsonify({"error": "Session expired, please login again"}),
                        401,
                    )

            # Update last_activity timestamp
            session["last_activity"] = datetime.now().timestamp()
            return f(*args, **kwargs)

        except Exception as e:
            raise e

    return decorated_function


# NOTE: Login route
@crumbl_blueprint.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        # validate input
        if not all([email, password]):
            return jsonify({"error": "Email and password are required"}), 400

        # query the user from database
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401

        # create session
        session["user_id"] = user.id
        session["logged_in"] = True
        session["last_activity"] = datetime.now().timestamp()

        # Set session to expire after 24 hours
        session.permanent = True

        return (
            jsonify(
                {
                    "message": "Login successfully",
                    "user": {
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        import traceback

        print("Error occurred:")
        print(traceback.format_exc)
        return jsonify({"error": f"Login failed : {str(e)}"}), 500


# NOTE: email validattion
def is_valid_email(email):
    """
    validate email format using regex pattern
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# NOTE: Register route
@crumbl_blueprint.route("/register", methods=["POST"])
def register():
    # PERF: for frontend, no need yet

    # if request.method == "OPTIONS":
    # return _build_cors_prelight_response()

    global user_id_counter, users

    try:
        # Debug print the request data
        print("Request JSON:", request.json)

        # Get User Input with debug prints
        email = request.json.get("email")
        firstName = request.json.get("firstName")
        lastName = request.json.get("lastName")
        homeAddress = request.json.get("homeAddress")
        password = request.json.get("password")

        # Validate required fields
        if not all([email, homeAddress, password]):
            return jsonify({"error": "Missing required fields"}), 400

        # validate email format
        if not is_valid_email(email):
            return jsonify({"error": "All fields are required"}), 400

        # Check if user already exists - modified for list structure
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User's email already exist"}), 400

        # Create new user instance
        new_user = User(
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
            homeAddress=homeAddress,
        )

        # add to database and commit
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User registered successfully: {email}")
            return (
                jsonify(
                    {
                        "message": "New user Created Successfully",
                        "user": {
                            "user_id": new_user.id,
                            "email": new_user.email,
                            "homeAddress": new_user.homeAddress,
                        },
                    }
                ),
                201,
            )

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Database error occurred"}), 500

    except Exception as e:
        import traceback

        print("Error occurred:")
        print(traceback.format_exc())
        return jsonify({"error": f"Failed to register user: {str(e)}"}), 500


@crumbl_blueprint.route("/users", methods=["GET"])
def list_users():
    return jsonify({"user": users}), 200


@crumbl_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        # Clear all session data
        session.clear()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Logout failed: {str(e)}"}), 500


# -------------------------------------------------------------#
# TODO: CRUD Operations for Inventory: - BETTY
# - Create Inventory Item: Allow the creation of new inventory
# items with fields like item name, description, quantity, and
# price. With auto creation of ID Read Inventory Items: Provide
# APIs to list all inventory items or fetch a single item based on
# its ID.
# - Update Inventory Item: Allow the modification of an inventory
# item's details (name, quantity, price, etc.).by id
# - Delete Inventory Item: Enable deletion of an inventory item by ID
# -------------------------------------------------------------#

#can i delete this?
crumbls = [
    {
        "name": "Chocolate Chip",
        "description": "The classic chocolate chip cookie",
        "quantity": 65,
        "price": 4.99,
        "ID": 20,
    },
    {
        "name": "Confetti Milk Shake",
        "description": "A confetti sugar cookie rolled in rainbow sprinkles and topped with cake-flavored buttercream and a dollop of whipped cream",
        "quantity": 23,
        "price": 4.99,
        "ID": 46,
    },
    {
        "name": "Kentucky Butter Cake",
        "description": "A yellow butter cake cookie smothered with a melt-in-your-mouth buttery glaze.",
        "quantity": 12,
        "price": 4.99,
        "ID": 26,
    },
    {
        "name": "Pink Velvet Cake Cookie",
        "description": "A velvety cake batter cookie topped with a layer of vanilla cream cheese frosting and pink velvet cookie crumbs.",
        "quantity": 7,
        "price": 4.99,
        "ID": 63,
    },
]


# compares and finds cookie
def findCrumbl(cid):
    for crum in crumbls_public:
        if crum["ID"] == cid:
            return crum
    return None


# comment this out later
# assigns a ranom ID number to cookie and ensures it isnt a repeat
def newID():
    while True:
        nid = random.randint(1, 100)
        if findCrumbl(nid) is None:
            return nid


# lists full list of cookies
@crumbl_blueprint.route("/crumbls", methods=["GET"])
def listCookies():
    crumsPublic = PublicCrum.query.all()
    return jsonify([crum.serialize() for crum in crumsPublic])
    #return jsonify(crumbls_public)


# find specific cookie by ID number
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["GET"])
def findCrum(cid):
    crum = PublicCrum.query.get(cid)
    if crum is None:
        return jsonify("error: Crumbl Cookie not found"), 404
    return jsonify(crum.serialize())
    #--------------------------------------
    # foundC = findCrumbl(cid)
    #if foundC is None:
    #    return jsonify("error: Crumbl Cookie not found"), 404
    #return jsonify(foundC)


# creates new crumbl cookie
@crumbl_blueprint.route("/crumbls", methods=["POST"])
def makeCrum():
    global crumbl_id_public
    if (
        not request.json
        or "name" not in request.json
        or "description" not in request.json
        or "quantity" not in request.json
        or "price" not in request.json
    ):
        return jsonify("error missing information"), 400

    try: 
        quant = int(request.json["quantity"])
        if quant < 0:
            return jsonify("Error:Quantity must be non-negative value"),400
        
        priced = round(float(request.json["price"]),2)
        if priced < 0: 
            return jsonify("Error:Price must be non-negative value"),400

    except ValueError:
            return jsonify("Error: Quantity must be integer and price must be float"),400

    while True:
        nID = crumbl_id_public
        crumbl_id_public += 1
        match = PublicCrum.query.get(nID)
        if match is None:
           break
        
    newCrumbl = PublicCrum(
        name = request.json["name"],
        description = request.json["description"],
        quantity= quant,
        price = priced,
        ID = nID,
    )
    db.session.add(newCrumbl)
    db.session.commit()

    return jsonify(newCrumbl.serialize()),201

    #crumbls_public.append(newCrumbl)
    #return jsonify(newCrumbl), 201


# updates existing cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["PUT"])
def updateCrum(cid):
    #crum = findCrumbl(cid)
    crum = PublicCrum.query.get(cid)
    if crum is None:
        jsonify("could not find cookie to update"), 404
    if not request.json:
        jsonify("please use proper json standards"), 400
    
    if "name" in request.json:
        name = request.json.get('name', crum.name)
    
    if "description" in request.json:
        description = request.json.get('description', crum.description)
    
    if "quantity" in request.json:
        try:
            quant = int(request.json.get('quantity',crum.quantity))
            if quant < 0:
                return jsonify("Error:Quantity must be non-negative value"),400
        except ValueError:
            return jsonify("Error: Quantity must be a valid integer"),400
   
    if "price" in request.json:
        try:
            price = round(float(request.json.get('price', crum.price),2))
            if price < 0: 
                return jsonify("Error:Price must be non-negative value"),400
        except ValueError:
            return jsonify("Error: Price must be a valid float"),400
        
    crum.name = name
    crum.description = description
    crum.quantity = quant
    crum.price = price

    db.session.commit()
    return jsonify(crum.serialize())

    #return jsonify(crum)


# deletes crumbl cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["DELETE"])
def deleteCrum(cid):
    #global crumbls_public
    #crum = findCrum(cid)
    crum = PublicCrum.query.get(cid)
    if crum is None:
        return jsonify("Crumble cookie could not be found"), 404
    
    db.session.delete(crum)
    db.session.commit()
    
    return jsonify({'success': 'crumbl cookie deleted'}), 200
    #crumbls_public = [c for c in crumbls if c["ID"] != cid]
    #return "", 204

# -------------------------------------------------------------#
# TODO: USER-Specific Inventory Management: - PHONG
# - Each Logged-in user will have their own inventory items, ensuring
# that users can only access and modify their own data.
# - Use sessions to ensure that only authenticated users can access
# inventory-related CRUD Operations
# -------------------------------------------------------------#
@crumbl_blueprint.route("/mycrumbls", methods=["GET"])
@login_required
def myListCookies():
    # Fetch all private crumbs belonging to the currently logged-in user
    user_crumbls = PrivateCrum.query.filter_by(user_id=session["user_id"]).all()

    # If the user has no items, return a friendly message instead of an error
    if not user_crumbls:
        return jsonify({"message": "You have no items in your inventory."}), 200

    # Return the list of user's items, serialized to JSON
    return jsonify([crum.serialize() for crum in user_crumbls]), 200


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["GET"])
@login_required
def findMyCrum(cid):
    # Query a specific crumb by ID that belongs to the logged-in user
    crum = PrivateCrum.query.filter_by(id=cid, user_id=session["user_id"]).first()

    # If not found, return a 404 error
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found"}), 404

    # If found, return the crumb details
    return jsonify(crum.serialize()), 200


@crumbl_blueprint.route("/mycrumbls", methods=["POST"])
@login_required
def makeMyCrum():
    # Check if the request includes a JSON body
    if not request.json:
        return jsonify({"error": "Missing request body"}), 400

    # Ensure all required fields are present and not empty
    required_fields = ["name", "description", "quantity", "price"]
    for field in required_fields:
        if field not in request.json or request.json[field] == "":
            return jsonify({"error": f"Missing or empty required field: {field}"}), 400

    # Validate quantity is an integer and non-negative
    if not isinstance(request.json["quantity"], int):
        return jsonify({"error": "Quantity must be an integer"}), 400
    if request.json["quantity"] < 0:
        return jsonify({"error": "Quantity must be non-negative"}), 400

    # Validate price is a number and non-negative
    if not isinstance(request.json["price"], (int, float)):
        return jsonify({"error": "Price must be a number"}), 400
    if request.json["price"] < 0:
        return jsonify({"error": "Price must be non-negative"}), 400

    # Create a new private crumb object associated with the current user
    new_crum = PrivateCrum(
        name=request.json["name"],
        description=request.json["description"],
        quantity=request.json["quantity"],
        price=round(float(request.json["price"]), 2),
        user_id=session["user_id"]
    )

    try:
        db.session.add(new_crum)
        db.session.commit()
    except Exception as e:
        # Rollback if any error occurs during the commit
        db.session.rollback()
        # Log the error for debugging
        logger.error(f"Database commit failed while creating crumb: {str(e)}")
        return jsonify({"error": "Failed to create crumb due to a database error"}), 500

    return jsonify(new_crum.serialize()), 201


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["PUT"])
@login_required
def updateMyCrum(cid):
    # Query the crumb by ID for the current user
    crum = PrivateCrum.query.filter_by(id=cid, user_id=session["user_id"]).first()

    # If crumb doesn't exist or doesn't belong to the user, return 404
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found or unauthorized"}), 404

    # Check if the request contains JSON
    if not request.json:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Keep track of whether at least one field gets updated
    updated = False

    # Validate and update 'name' if provided
    if "name" in request.json:
        if not isinstance(request.json["name"], str) or request.json["name"].strip() == "":
            return jsonify({"error": "Name must be a non-empty string"}), 400
        crum.name = request.json["name"]
        updated = True

    # Validate and update 'description' if provided
    if "description" in request.json:
        if not isinstance(request.json["description"], str) or request.json["description"].strip() == "":
            return jsonify({"error": "Description must be a non-empty string"}), 400
        crum.description = request.json["description"]
        updated = True

    # Validate and update 'quantity' if provided
    if "quantity" in request.json:
        if not isinstance(request.json["quantity"], int):
            return jsonify({"error": "Quantity must be an integer"}), 400
        if request.json["quantity"] < 0:
            return jsonify({"error": "Quantity must be non-negative"}), 400
        crum.quantity = request.json["quantity"]
        updated = True

    # Validate and update 'price' if provided
    if "price" in request.json:
        if not isinstance(request.json["price"], (int, float)):
            return jsonify({"error": "Price must be a number"}), 400
        if request.json["price"] < 0:
            return jsonify({"error": "Price must be non-negative"}), 400
        crum.price = round(float(request.json["price"]), 2)
        updated = True

    # If no fields were updated, return an error
    if not updated:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        # Commit changes to the database
        db.session.commit()
    except Exception as e:
        # Rollback if any error occurs during the commit
        db.session.rollback()
        # Log the error for debugging
        logger.error(f"Database commit failed while updating crumb: {str(e)}")
        return jsonify({"error": "Failed to delete crumb due to a database error"}), 500    
    
    return jsonify(crum.serialize()), 200


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["DELETE"])
@login_required
def deleteMyCrum(cid):
    # Query the crumb by ID for the current user
    crum = PrivateCrum.query.filter_by(id=cid, user_id=session["user_id"]).first()

    # If crumb not found or doesn't belong to user, return 404
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found or unauthorized"}), 404

    try:
        # Delete the crumb from the database
        db.session.delete(crum)
        db.session.commit()
    except Exception as e:
        # Rollback if any error occurs during the commit
        db.session.rollback()
        # Log the error for debugging
        logger.error(f"Database commit failed while deleting crumb: {str(e)}")
        return jsonify({"error": "Failed to delete crumb due to a database error"}), 500
    
    # Return a success message
    return jsonify({"message": "Item deleted successfully."}), 200

# -------------------------------------------------------------#
# TODO: Session and Cookie Security: - MATHEW
# - Secure user sessions with encryption (Flask Security key)
# - Implement proper session expiration handing to automatically
# log out.
# -------------------------------------------------------------#
