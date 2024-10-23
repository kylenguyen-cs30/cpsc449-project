import jwt
import os

from flask import Blueprint, request, jsonify
from functools import wraps
from .models import User
from app import db


crumbl_blueprint = Blueprint("crumbl_blueprint", __name__)


@crumbl_blueprint.route("/", methods=["GET"])
def home():
    return jsonify("Backend Online!")


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


@crumbl_blueprint.route("/register", methods=["POST"])
def register():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    try:
        firstName = request.json.get("firstName")
        lastName = request.json.get("lastName")
        email = request.json.get("email")
        homeAddress = request.json.get("homeAddress")
        password = request.json.get("password")

        # checking if the user is already existing
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already existed"}), 401

        new_user = User(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            homeAddress=homeAddress,
        )

        db.session.add(new_user)
        db.session.commit()

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


# -------------------------------------------------------------#
# TODO: USER-Specific Inventory Management: - PHONG
# - Each Logged-in user will have their own inventory items, ensuring
# that users can only access and modify their own data.
# - Use sessions to ensure that only authenticated users can access
# inventory-related CRUD Operations
# -------------------------------------------------------------#


# -------------------------------------------------------------#
# TODO: Session and Cookie Security:
# - Secure user sessions with encryption (Flask Security key)
# - Implement proper session expiration handing to automatically
# log out.
# -------------------------------------------------------------#
