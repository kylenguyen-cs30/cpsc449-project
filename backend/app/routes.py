import jwt
import os
import random

from flask import Blueprint, request, jsonify, session
from functools import wraps

# from .models import User
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# from app import db

# User Container
users = {}

# Inventories Container
inventories = {}
# user_ID
user_id_counter = 1

# inventory_item id
inventory_id_counter = 1


# -------------------------------------------------------------#
# NOTE: For Public

# Crumbs Container
crumbs_public = {}
# crumb_id
crumb_id_public = 1

# NOTE: For Private

# Crumbs Container
crumbs_private = [] # crumbs_private = {}
# crumb_id
crumb_id_private = 1
# -------------------------------------------------------------#


crumbl_blueprint = Blueprint("crumbl_blueprint", __name__)


@crumbl_blueprint.route("/", methods=["GET"])
def home():
    return jsonify("Crumbl Backend Online!")


# -------------------------------------------------------------#
# TODO: User Authentication With Sessions and Cookies: - KYLE
# - User Login (SHANTANU) :  Implement user login functionality where
# a user can log in by providing credentials (username and
# password). Use sessions and cookies to track and maintain login states.
# - User Registration (KYLE): Allow new users to register by
# providing a username, password, and email.
# - Session Management (KYLE): Use Flask's session management to store user
# session data securely
# - Logout (SHANTANU): Implement logout functionality that clears the session and
# removes authentication cookies
# -------------------------------------------------------------#


# NOTE: Middleware for login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in to access this route"}), 403

        # Check if session has expired
        if "last_activity" in session:
            last_activity = datetime.fromtimestamp(session["last_activity"])
            if datetime.now() - last_activity > timedelta(hours=24):
                session.clear()  # Fixed typo: was session.clears()
                return jsonify({"error": "Session expired, please login again"}), 401

        # Update last_activity timestamp
        session["last_activity"] = datetime.now().timestamp()
        return f(*args, **kwargs)

    return decorated_function


@crumbl_blueprint.route("/register", methods=["POST"])
def register():
    global user_id_counter

    # PERF: for frontend, no need yet
    #
    # if request.method == "OPTIONS":
    #     return _build_cors_prelight_response()

    try:
        # Get User Input
        email = request.json.get("email")
        firstName = request.json.get("firstName")
        lastName = request.json.get("lastName")
        homeAddress = request.json.get("homeAddress")
        password = request.json.get("password")

        # NOTE: For Part 2
        #
        # --------------------------------------------------------------#
        # checking if the user is already existing
        # existing_user = User.query.filter_by(email=email).first()
        # if existing_user:
        #     return jsonify({"error": "User with this email already existed"}), 401
        # --------------------------------------------------------------#

        # Validate required fields
        if not all([email, homeAddress, password]):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        if email in users:
            return jsonify({"error": "User's email is already existed"}), 400

        # generate User ID
        user_id = f"User_{user_id_counter}"
        user_id_counter += 1

        # Secure hash password
        password_hash = generate_password_hash(password)

        users[email] = {
            "user_id": user_id,
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "homeAddress": homeAddress,
            "password": password_hash,
        }

        # separate index of user_ids and email for quick look up
        if not hasattr(crumbl_blueprint, "user_id_index"):
            crumbl_blueprint.user_id_index = {}
        crumbl_blueprint.user_id_index[user_id] = email

        return (
            jsonify(
                {
                    "message": "New user Created Successfully",
                    "user": {
                        "user_id": user_id,
                        "email": email,
                        "homeAddress": homeAddress,
                    },
                }
            ),
            201,
        )

        # NOTE: For part 2
        #
        # --------------------------------------------------------------#
        # new_user = User(
        #     email=email,
        #     password=password,
        #     homeAddress=homeAddress,
        # )
        #
        # db.session.add(new_user)
        # db.session.commit()
        # --------------------------------------------------------------#

        # return (jsonify({"message": "New User Created Successfully !"}), 202)
    except Exception as e:
        return jsonify({"error": f"Failed to register user: {str(e)}"}), 500


@crumbl_blueprint.route("/users", methods=["GET"])
def list_users():
    return jsonify({"user": users}), 200


# NOTE: Login route
@crumbl_blueprint.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        # Check if user exist
        if email not in users:
            return jsonify({"error": "Invalid email or password "}), 401

        user = users[email]

        # verify password
        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid email or password"}), 401

        # create session
        session["user_id"] = user["user_id"]
        session["logged_in"] = True
        session["last_activity"] = datetime.now().timestamp()

        # Set session to expire after 24 hours
        session.permanent = True

        return (
            jsonify(
                {
                    "message": "Login successfully",
                    "user": {
                        "email": user["email"],
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Login failed : {str(e)}"}), 500


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
    for crum in crumbls:
        if crum["ID"] == cid:
            return crum
    return None


# assigns a ranom ID number to cookie and ensures it isnt a repeat
def newID():
    while True:
        nid = random.randint(1, 100)
        if findCrumbl(nid) is None:
            return nid


# lists full list of cookies
@crumbl_blueprint.route("/crumbls", methods=["GET"])
def listCookies():
    return jsonify(crumbls)


# find specific cookie by ID number
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["GET"])
def findCrum(cid):
    foundC = findCrumbl(cid)
    if foundC is None:
        return jsonify("error: Crumbl Cookie not found"), 404
    return jsonify(foundC)


# creates new crumbl cookie
@crumbl_blueprint.route("/crumbls", methods=["POST"])
def makeCrum():
    if (
        not request.json
        or "name" not in request.json
        or "description" not in request.json
        or "quantity" not in request.json
        or "price" not in request.json
    ):
        return jsonify("error missing information"), 400
    newCID = newID()
    newCrumbl = {
        "name": request.json["name"],
        "description": request.json["description"],
        "quantity": request.json["quantity"],
        "price": request.json["price"],
        "ID": newCID,
    }
    crumbls.append(newCrumbl)
    return jsonify(newCrumbl), 201


# updates existing cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["PUT"])
def updateCrum(cid):
    crum = findCrumbl(cid)
    if crum is None:
        jsonify("could not find cookie to update"), 404
    if not request.json:
        jsonify("please use proper json standards"), 400
    crum["name"] = request.json.get("name", crum["name"])
    crum["description"] = request.json.get("description", crum["description"])
    crum["quantity"] = request.json.get("quantity", crum["quantity"])
    crum["price"] = request.json.get("price", crum["price"])
    return jsonify(crum)


# deletes crumbl cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["DELETE"])
def deleteCrum(cid):
    global crumbls
    crum = findCrum(cid)
    if crum is None:
        return jsonify("Crumble cookie could not be found"), 404
    crumbls = [c for c in crumbls if c["ID"] != cid]
    return "", 204


# -------------------------------------------------------------#
# TODO: USER-Specific Inventory Management: - PHONG
# - Each Logged-in user will have their own inventory items, ensuring
# that users can only access and modify their own data.
# - Use sessions to ensure that only authenticated users can access
# inventory-related CRUD Operations
# -------------------------------------------------------------#
# ]
@crumbl_blueprint.route("/mycrumbls", methods=["GET"])
@login_required
def myListCookies():
    user_id = session.get("user_id")
    user_crumbls = [crum for crum in crumbs_private if crum["user_id"] == user_id]
    return jsonify(user_crumbls)


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["GET"])
@login_required
def findMyCrum(cid):
    user_id = session.get("user_id")
    foundC = next(
        (crum for crum in crumbs_private if crum["ID"] == cid and crum["user_id"] == user_id),
        None,
    )
    if foundC is None:
        return jsonify({"error": "Crumbl Cookie not found"}), 404
    return jsonify(foundC)


@crumbl_blueprint.route("/mycrumbls", methods=["POST"])
@login_required
def makeMyCrum():
    user_id = session.get("user_id")
    if (
        not request.json
        or "name" not in request.json
        or "description" not in request.json
        or "quantity" not in request.json
        or "price" not in request.json
    ):
        return jsonify({"error": "Missing information"}), 400

    global crumb_id_private    
    newCID = crumb_id_private
    crumb_id_private += 1
    newCrumbl = {
        "name": request.json["name"],
        "description": request.json["description"],
        "quantity": request.json["quantity"],
        "price": request.json["price"],
        "ID": newCID,
        "user_id": user_id,  # Associate new item with the logged-in user
    }
    crumbs_private.append(newCrumbl)
    return jsonify(newCrumbl), 201


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["PUT"])
@login_required
def updateMyCrum(cid):
    user_id = session.get("user_id")
    crum = next(
        (crum for crum in crumbs_private if crum["ID"] == cid and crum["user_id"] == user_id),
        None,
    )
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found or unauthorized"}), 404
    if not request.json:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Update fields if provided in request
    crum["name"] = request.json.get("name", crum["name"])
    crum["description"] = request.json.get("description", crum["description"])
    crum["quantity"] = request.json.get("quantity", crum["quantity"])
    crum["price"] = request.json.get("price", crum["price"])
    return jsonify(crum)


@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["DELETE"])
@login_required
def deleteMyCrum(cid):
    global crumbs_private
    user_id = session.get("user_id")
    crum = next(
        (crum for crum in crumbs_private if crum["ID"] == cid and crum["user_id"] == user_id),
        None,
    )
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found or unauthorized"}), 404
    crumbs_private = [c for c in crumbs_private if not (c["ID"] == cid and c["user_id"] == user_id)]
    return jsonify({"message": "Item deleted successfully."}), 200


# -------------------------------------------------------------#
# TODO: Session and Cookie Security: - MATHEW
# - Secure user sessions with encryption (Flask Security key)
# - Implement proper session expiration handing to automatically
# log out.
# -------------------------------------------------------------#


