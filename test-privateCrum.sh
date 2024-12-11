# 1. Create a new order (this worked successfully)
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

# 2. Get customer orders (this worked successfully)
http GET "localhost:5001/order/customer?firstName=John&lastName=Doe&homeAddress=123 Main St, City, Country"

# 3. Update order status (using actual order_id from your output)
http PUT localhost:5001/order/675908f13d4c2da6bfd044bd/status \
  status="processing"

# 4. Delete an order (using actual order_id from your output)
http DELETE localhost:5001/order/675908f13d4c2da6bfd044bd

# Test cases for error handling (these worked as expected)

# 5. Test invalid order creation (missing required field)
http POST localhost:5001/order \
  firstName="John" \
  lastName="Doe" \
  items:='[{"name": "Cookie", "price": 4.99, "quantity": 1}]'

# 6. Test invalid status update
http PUT localhost:5001/order/675908f13d4c2da6bfd044bd/status \
  status="invalid_status"

# 7. Test invalid customer query
http GET "localhost:5001/order/customer?firstName=John"

# Complete test sequence
echo "Running complete test sequence..."
echo "1. Creating new order..."
ORDER_RESPONSE=$(http POST localhost:5001/order \
  firstName="John" \
  lastName="Doe" \
  homeAddress="123 Main St, City, Country" \
  items:='[{"name": "Test Cookie", "price": 4.99, "quantity": 1}]')

# Extract order_id from response
ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.order_id')

echo "Created order with ID: $ORDER_ID"
echo "2. Getting customer orders..."
http GET "localhost:5001/order/customer?firstName=John&lastName=Doe&homeAddress=123 Main St, City, Country"

echo "3. Updating order status..."
http PUT localhost:5001/order/$ORDER_ID/status status="processing"

echo "4. Deleting order..."
http DELETE localhost:5001/order/$ORDER_ID
