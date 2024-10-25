import jwt
import os
import random

from flask import Blueprint, request, jsonify, session
from functools import wraps
from .models import User
from functools import wraps
from werkzeug.security import generate_password_hash
from app import db


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


@crumbl_blueprint.route("/", methods=["GET"])
def home():
    return jsonify("Backend Online!")


def findCrumbl(cid):
    for cookie in crumbls:
        if cookie["ID"] == cid:
            return cookie
    return None


def newID():
    while True:
        nid = random.randint(1, 100)
        if findCrumbl(nid) is None:
            return nid


@crumbl_blueprint.route("/crumbls", methods=["GET"])
def listCookies():
    return jsonify(crumbls)


@crumbl_blueprint.route("/crumbls/<int:crumbls_id>", methods=["GET"])
def crumblsID(crumbls_id):
    foundC = findCrumbl(crumbls_id)
    if foundC is None:
        return jsonify("error: Crumbl Cookie not found"), 404
    return jsonify(foundC)


@crumbl_blueprint.route("/crumbls", methods=["POST"])
def makeCrumbl():
    if (
        not request.json
        or "name" not in request.json
        or "description" not in request.json
        or "quantity" not in request.json
        or "price" not in request.json
    ):
        return jsonify("error missing information")
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


# -------------------------------------------------------------#
# TODO: USER-Specific Inventory Management: - PHONG
# - Each Logged-in user will have their own inventory items, ensuring
# that users can only access and modify their own data.
# - Use sessions to ensure that only authenticated users can access
# inventory-related CRUD Operations
# -------------------------------------------------------------#


# -------------------------------------------------------------#
# TODO: Session and Cookie Security: - MATHEW
# - Secure user sessions with encryption (Flask Security key)
# - Implement proper session expiration handing to automatically
# log out.
# -------------------------------------------------------------#
