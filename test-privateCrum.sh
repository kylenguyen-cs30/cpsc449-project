#!/bin/bash

BASE_URL="http://localhost:5001"

echo "=== First, login as John ==="
http --session=John POST "${BASE_URL}/login" \
  email="john@example.com" \
  password="password123"

echo "\n=== Test 1: List My Crumbls (initially empty) ==="
http --session=John GET "${BASE_URL}/mycrumbls"

echo "\n=== Test 2: Create New Crumbls ==="
# Create first crumbl
echo "\nCreating Chocolate Chip Cookie..."
http --session=John POST "${BASE_URL}/mycrumbls" \
  name="Chocolate Chip Cookie" \
  description="Classic chocolate chip cookie with semi-sweet chocolate chips" \
  quantity:=12 \
  price:=3.99

# Create second crumbl
echo "\nCreating Sugar Cookie..."
http --session=John POST "${BASE_URL}/mycrumbls" \
  name="Sugar Cookie" \
  description="Traditional sugar cookie with sprinkles" \
  quantity:=24 \
  price:=2.99

echo "\n=== Test 3: List My Crumbls (should show new items) ==="
http --session=John GET "${BASE_URL}/mycrumbls"

echo "\n=== Test 4: Get Specific Crumbl (ID 1) ==="
http --session=John GET "${BASE_URL}/mycrumbls/1"

echo "\n=== Test 5: Update Crumbl (ID 1) ==="
http --session=John PUT "${BASE_URL}/mycrumbls/1" \
  name="Premium Chocolate Chip Cookie" \
  price:=4.99 \
  quantity:=10

echo "\n=== Test 6: Verify Update ==="
http --session=John GET "${BASE_URL}/mycrumbls/1"

echo "\n=== Test 7: Delete Crumbl (ID 2) ==="
http --session=John DELETE "${BASE_URL}/mycrumbls/2"

echo "\n=== Test 8: Final List (should show only remaining items) ==="
http --session=John GET "${BASE_URL}/mycrumbls"

echo "\n=== Test 9: Logout ==="
http --session=John POST "${BASE_URL}/logout"

echo "\nTest completed!"
