# Create a new order
http POST localhost:5001/order \
  firstName="John" \
  lastName="Doe" \
  homeAddress="123 Main St, City, Country" \
  items:='[
        {
            "name": "Chocolate Chip Cookie",
            "price": 4.99,
            "quantity": 2
        },
        {
            "name": "Milk Bar Cookie",
            "price": 5.99,
            "quantity": 1
        }
    ]'

# Get customer orders
http GET "localhost:5001/order/customer?firstName=John&lastName=Doe&homeAddress=123 Main St, City, Country"

# Update order status (replace ORDER_ID with actual ID from create response)
http PUT localhost:5001/order/ORDER_ID/status \
  status="processing"

# Delete an order (replace ORDER_ID with actual ID)
http DELETE localhost:5001/order/ORDER_ID

# Test invalid order creation (missing required field)
http POST localhost:5001/order \
  firstName="John" \
  lastName="Doe" \
  items:='[{"name": "Cookie", "price": 4.99, "quantity": 1}]'

# Test invalid status update
http PUT localhost:5001/order/ORDER_ID/status \
  status="invalid_status"

# Get orders with partial customer info (should return error)
http GET "localhost:5001/order/customer?firstName=John"
