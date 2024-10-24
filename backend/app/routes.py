import jwt
import os
import random

from flask import Blueprint, request, jsonify
from functools import wraps
from .models import User
from app import db


crumbl_blueprint = Blueprint("crumbl", __name__)


crumbls = [
    {"name": "Chocolate Chip", "description": "The classic chocolate chip cookie","quantity": 65,"price": 4.99,"ID": 20},
    {"name": "Confetti Milk Shake", "description": "A confetti sugar cookie rolled in rainbow sprinkles and topped with cake-flavored buttercream and a dollop of whipped cream","quantity": 23,"price": 4.99,"ID":46},
    {"name": "Kentucky Butter Cake", "description":"A yellow butter cake cookie smothered with a melt-in-your-mouth buttery glaze.","quantity":12,"price":4.99,"ID":26},
    {"name": "Pink Velvet Cake Cookie", "description": "A velvety cake batter cookie topped with a layer of vanilla cream cheese frosting and pink velvet cookie crumbs.","quantity":7,"price":4.99,"ID":63}
]

@crumbl_blueprint.route("/")
def home():
    return jsonify("Backend Online!")

def findCrumbl(cid):
    for cookie in crumbls:
        if cookie["ID"] == cid:
            return cookie
    return None

def newID():
    while True:
        nid = random.randint(1,100)
        if findCrumbl(nid) is None:
            return nid


@crumbl_blueprint.route('/crumbls', methods=['GET'])
def listCookies():
    return jsonify(crumbls)

@crumbl_blueprint.route('/crumbls/<int:crumbls_id>', methods=['GET'])
def crumblsID(crumbls_id):
    foundC = findCrumbl(crumbls_id)
    if foundC is None:
        return jsonify("error: Crumbl Cookie not found"),404
    return jsonify(foundC)


@crumbl_blueprint.route('/crumbls',methods=['POST'])
def makeCrumbl():
    if not request.json or 'name' not in request.json or 'description' not in request.json or 'quantity' not in request.json or 'price' not in request.json:
        return jsonify("error missing information")
    newCID= newID()
    newCrumbl = {
        'name': request.json['name'],
        'description':request.json['description'],
        'quantity':request.json['quantity'],
        'price':request.json['price'],
        'ID': newCID
    }
    crumbls.append(newCrumbl)
    return jsonify(newCrumbl), 201

    



# -------------------------------------------------------------#
# TODO: User Authentication With Sessions and Cookies: - KYLE
# - User Login :  Implement user login functionality where
# a user can log in by providing credentials (username and
# password). Use sessions and cookies to track and maintain login states.
# - User Registration: Allow new users to register by
# providing a username, password, and email.
# - Session Management: Use Flask's session management to store user
# session data securely
# - Logout: Implement logout functionality that clears the session and
# removes authentication cookies
# -------------------------------------------------------------#

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