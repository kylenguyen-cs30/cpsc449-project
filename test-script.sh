#!/bin/bash

# Set the base URL
BASE_URL="http://localhost:5001"

echo "=== Testing User Registration ==="

# Register User 1
echo "\nRegistering User 1..."
http POST "${BASE_URL}/register" \
  email="john.doe@example.com" \
  firstName="John" \
  lastName="Doe" \
  homeAddress="123 Main St" \
  password="password123"

# Register User 2
echo "\nRegistering User 2..."
http POST "${BASE_URL}/register" \
  email="jane.smith@example.com" \
  firstName="Jane" \
  lastName="Smith" \
  homeAddress="456 Oak Ave" \
  password="password456"

# Register User 3
echo "\nRegistering User 3..."
http POST "${BASE_URL}/register" \
  email="bob.wilson@example.com" \
  firstName="Bob" \
  lastName="Wilson" \
  homeAddress="789 Pine Rd" \
  password="password789"

echo "\n=== Testing Login ==="

# Login User 1
echo "\nLogging in User 1..."
http POST "${BASE_URL}/login" \
  email="john.doe@example.com" \
  password="password123"

# Store the cookies from login (if needed for subsequent requests)
http --session=./session.json POST "${BASE_URL}/login" \
  email="john.doe@example.com" \
  password="password123"

echo "\n=== Testing List Users ==="

# List all users
echo "\nListing all users..."
http --session=./session.json GET "${BASE_URL}/users"

echo "\n=== Testing Logout ==="

# Logout
echo "\nLogging out..."
http --session=./session.json POST "${BASE_URL}/logout"

echo "\nTest completed!"
