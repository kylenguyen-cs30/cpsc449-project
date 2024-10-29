import jwt
import os
import random

from flask import Blueprint, request, jsonify, session
from functools import wraps
# from .models import User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# from app import db


crumbl_blueprint = Blueprint("crumbl_blueprint", __name__)


# -------------------------------------------------------------#
# TODO: User Authentication With Sessions and Cookies: - SHANTANU , KYLE
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

# User Container
users = {}


# NOTE:  Middleware for login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "you must be logged in access this route"}), 403
        return f(*args, **kwargs)

    return decorated_function


@crumbl_blueprint.route("/register", methods=["POST"])
def register():

    # PERF: for frontend, no need yet
    #
    # if request.method == "OPTIONS":
    #     return _build_cors_prelight_response()

    try:
        email = request.json.get("email")
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

        # Check if user already exists
        if email in users:
            return jsonify({"error": "User's email is already existed"}), 400

        # Secure hash password
        password_hash = generate_password_hash(password)

        users[email] = {
            "email": email,
            "homeAddress": homeAddress,
            "password": password_hash,
        }

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

        return (jsonify({"message": "New User Created Successfully !"}), 202)
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"Failed to register user: {str(e)}"}), 501


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


# crumbls = [
#     {
#         "name": "Chocolate Chip",
#         "description": "The classic chocolate chip cookie",
#         "quantity": 65,
#         "price": 4.99,
#         "ID": 20,
#     },
#     {
#         "name": "Confetti Milk Shake",
#         "description": "A confetti sugar cookie rolled in rainbow sprinkles and topped with cake-flavored buttercream and a dollop of whipped cream",
#         "quantity": 23,
#         "price": 4.99,
#         "ID": 46,
#     },
#     {
#         "name": "Kentucky Butter Cake",
#         "description": "A yellow butter cake cookie smothered with a melt-in-your-mouth buttery glaze.",
#         "quantity": 12,
#         "price": 4.99,
#         "ID": 26,
#     },
#     {
#         "name": "Pink Velvet Cake Cookie",
#         "description": "A velvety cake batter cookie topped with a layer of vanilla cream cheese frosting and pink velvet cookie crumbs.",
#         "quantity": 7,
#         "price": 4.99,
#         "ID": 63,
#     },
# ]


@crumbl_blueprint.route("/", methods=["GET"])
def home():
    return jsonify("Backend Online!")

# compares and finds cookie
def findCrumbl(cid):
    for crum in crumbls:
        if crum["ID"] == cid:
            return crum
    return None

#assigns a ranom ID number to cookie and ensures it isnt a repeat
def newID():
    while True:
        nid = random.randint(1, 100)
        if findCrumbl(nid) is None:
            return nid

#lists full list of cookies
@crumbl_blueprint.route("/crumbls", methods=["GET"])
def listCookies():
    return jsonify(crumbls)

#find specific cookie by ID number
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["GET"])
def findCrum(cid):
    foundC = findCrumbl(cid)
    if foundC is None:
        return jsonify("error: Crumbl Cookie not found"), 404
    return jsonify(foundC)

#creates new crumbl cookie
@crumbl_blueprint.route("/crumbls", methods=["POST"])
def makeCrum():
    if (
        not request.json
        or "name" not in request.json
        or "description" not in request.json
        or "quantity" not in request.json
        or "price" not in request.json
    ):
        return jsonify("error missing information"),400
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

#updates existing cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["PUT"])
def updateCrum(cid):
    crum = findCrumbl(cid)
    if crum is None:
        jsonify('could not find cookie to update'), 404
    if not request.json:
        jsonify('please use proper json standards'), 400
    crum['name']= request.json.get('name',crum['name'])
    crum['description']= request.json.get('description',crum['description'])
    crum['quantity']= request.json.get('quantity',crum['quantity'])
    crum['price']= request.json.get('price',crum['price'])
    return jsonify(crum)

#deletes crumbl cookie
@crumbl_blueprint.route("/crumbls/<int:cid>", methods=["DELETE"])
def deleteCrum(cid):
    global crumbls
    crum = findCrum(cid)
    if crum is None:
        return jsonify('Crumble cookie could not be found'), 404
    crumbls = [c for c in crumbls if c['ID']!=cid]
    return '', 204



# -------------------------------------------------------------#
# TODO: USER-Specific Inventory Management: - PHONG
# - Each Logged-in user will have their own inventory items, ensuring
# that users can only access and modify their own data.
# - Use sessions to ensure that only authenticated users can access
# inventory-related CRUD Operations
# -------------------------------------------------------------#


# -------------------------------------------------------------#
# NOTE:
# Using mock users and mock login to add user_id to session
# Update new mock crumbls data
# RuntimeError: The session is unavailable because no secret key was set.
# TODO:
# - Add: `app.secret_key="YOUR_SECRET_KEY"` in __init__.py. 
# -------------------------------------------------------------#

# Mocking users and Login 
users = [
    {
        "id": 1,
        "email": "john.doe@example.com",
        "homeAddress": "123 Main St, Springfield, IL",
        "password": generate_password_hash("jd"),
    },
    {
        "id": 2,
        "email": "jane.smith@example.com",
        "homeAddress": "456 Oak St, Springfield, IL",
        "password": generate_password_hash("js"),
        "firstName": "Jane",
        "lastName": "Smith",
    },
    {
        "id": 3,
        "email": "michael.jordan@example.com",
        "homeAddress": "789 Maple Ave, Chicago, IL",
        "password": generate_password_hash("mj"),
        "firstName": "Michael",
        "lastName": "Jordan",
    },
    {
        "id": 4,
        "email": "susan.williams@example.com",
        "homeAddress": "321 Elm St, Aurora, IL",
        "password": generate_password_hash("sw"),
        "firstName": "Susan",
        "lastName": "Williams",
    },
]

@crumbl_blueprint.route("/login", methods=["POST"])
def login():
    # Example code - assumes you are authenticating a user and retrieving their `user_id`
    email = request.json.get("email")
    password = request.json.get("password")
    user = {}

    # Find user based on email
    for u in users: 
        if u["email"] == email: user = u

    if user and check_password_hash(user["password"], password):
        # Store the `user_id` in the session after successful login
        session["user_id"] = user["id"]
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# Crumble with users_id containers
crumbls = [
    {
        "name": "Chocolate Chip",
        "description": "The classic chocolate chip cookie",
        "quantity": 65,
        "price": 4.99,
        "ID": 20,
        "user_id": 1,
    },
    {
        "name": "Confetti Milk Shake",
        "description": "A confetti sugar cookie rolled in rainbow sprinkles and topped with cake-flavored buttercream and a dollop of whipped cream",
        "quantity": 23,
        "price": 4.99,
        "ID": 46,
        "user_id": 2,
    },
    {
        "name": "Kentucky Butter Cake",
        "description": "A yellow butter cake cookie smothered with a melt-in-your-mouth buttery glaze.",
        "quantity": 12,
        "price": 4.99,
        "ID": 26,
        "user_id": 3,
    },
    {
        "name": "Pink Velvet Cake Cookie",
        "description": "A velvety cake batter cookie topped with a layer of vanilla cream cheese frosting and pink velvet cookie crumbs.",
        "quantity": 7,
        "price": 4.99,
        "ID": 63,
        "user_id": 4,
    },
]

@crumbl_blueprint.route("/mycrumbls", methods=["GET"])
@login_required
def myListCookies():
    user_id = session.get("user_id")
    user_crumbls = [crum for crum in crumbls if crum["user_id"] == user_id]
    return jsonify(user_crumbls)

@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["GET"])
@login_required
def findMyCrum(cid):
    user_id = session.get("user_id")
    foundC = next((crum for crum in crumbls if crum["ID"] == cid and crum["user_id"] == user_id), None)
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
    newCID = newID()
    newCrumbl = {
        "name": request.json["name"],
        "description": request.json["description"],
        "quantity": request.json["quantity"],
        "price": request.json["price"],
        "ID": newCID,
        "user_id": user_id  # Associate new item with the logged-in user
    }
    crumbls.append(newCrumbl)
    return jsonify(newCrumbl), 201

@crumbl_blueprint.route("/mycrumbls/<int:cid>", methods=["PUT"])
@login_required
def updateMyCrum(cid):
    user_id = session.get("user_id")
    crum = next((crum for crum in crumbls if crum["ID"] == cid and crum["user_id"] == user_id), None)
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
    global crumbls
    user_id = session.get("user_id")
    crum = next((crum for crum in crumbls if crum["ID"] == cid and crum["user_id"] == user_id), None)
    if crum is None:
        return jsonify({"error": "Crumbl Cookie not found or unauthorized"}), 404
    crumbls = [c for c in crumbls if not (c["ID"] == cid and c["user_id"] == user_id)]
    return jsonify({"message": "Item deleted successfully."}), 200



# -------------------------------------------------------------#
# TODO: Session and Cookie Security: - MATHEW
# - Secure user sessions with encryption (Flask Security key)
# - Implement proper session expiration handing to automatically
# log out.
# -------------------------------------------------------------#
