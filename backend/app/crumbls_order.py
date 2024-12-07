from flask import Blueprint, request, jsonify
from app.mongo_connection import mongo
from bson import ObjectId
from datetime import datetime

# Create blueprint with url_prefix
crumbl_order = Blueprint("order", __name__, url_prefix="/order")


@crumbl_order.route("", methods=["POST"])
def create_order():
    try:
        data = request.json

        # Validate required fields
        required_fields = ["firstName", "lastName", "homeAddress", "items"]
        if not all(field in data for field in required_fields):
            return (
                jsonify(
                    {"error": "Missing required fields", "required": required_fields}
                ),
                400,
            )

        # Calculate total order amount
        total = sum(item["price"] * item["quantity"] for item in data["items"])

        # Create order document
        order = {
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "homeAddress": data["homeAddress"],
            "items": data["items"],
            "total": total,
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        # Insert into MongoDB
        result = mongo.db.orders.insert_one(order)

        return (
            jsonify(
                {
                    "message": "Order created successfully",
                    "order_id": str(result.inserted_id),
                    "total": total,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crumbl_order.route("/customer", methods=["GET"])
def get_customer_orders():
    try:
        # Get query parameters
        firstName = request.args.get("firstName")
        lastName = request.args.get("lastName")
        homeAddress = request.args.get("homeAddress")

        if not all([firstName, lastName, homeAddress]):
            return (
                jsonify(
                    {
                        "error": "Missing required parameters",
                        "required": ["firstName", "lastName", "homeAddress"],
                    }
                ),
                400,
            )

        # Find orders matching customer info
        query = {
            "firstName": firstName,
            "lastName": lastName,
            "homeAddress": homeAddress,
        }

        # Get orders and convert ObjectId to string
        orders = list(mongo.db.orders.find(query).sort("created_at", -1))
        for order in orders:
            order["_id"] = str(order["_id"])
            # Convert datetime objects to ISO format strings
            order["created_at"] = order["created_at"].isoformat()
            order["updated_at"] = order["updated_at"].isoformat()

        return jsonify(orders), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crumbl_order.route("/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    try:
        data = request.json

        if "status" not in data:
            return jsonify({"error": "Missing status field"}), 400

        # Validate status
        valid_statuses = ["pending", "processing", "completed", "cancelled"]
        if data["status"] not in valid_statuses:
            return (
                jsonify({"error": "Invalid status", "valid_statuses": valid_statuses}),
                400,
            )

        # Update order status
        result = mongo.db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": data["status"], "updated_at": datetime.utcnow()}},
        )

        if result.modified_count == 0:
            return jsonify({"error": "Order not found or status not modified"}), 404

        return jsonify({"message": "Order status updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crumbl_order.route("/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        result = mongo.db.orders.delete_one({"_id": ObjectId(order_id)})

        if result.deleted_count == 0:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({"message": "Order deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
