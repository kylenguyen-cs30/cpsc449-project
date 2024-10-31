#!/bin/bash

# Array of test users
declare -a users=(
    "alice:Alice:Johnson:123 Apple St"
    "bob:Bob:Smith:456 Banana Ave"
    "carol:Carol:Davis:789 Cherry Ln"
    "david:David:Wilson:321 Date Rd"
    "eve:Eve:Brown:654 Elder St"
    "frank:Frank:Miller:987 Fig Ave"
    "grace:Grace:Taylor:147 Grape St"
    "henry:Henry:Anderson:258 Hazel Ln"
    "ivy:Ivy:Thomas:369 Ice Rd"
    "jack:Jack:Martinez:741 Jam St"
)

echo "Creating test users..."
echo "----------------------------------------"
echo "Credentials for login:"
echo "----------------------------------------"

for user in "${users[@]}"; do
    # Split the user data
    IFS=':' read -r username firstName lastName address <<< "$user"
    
    # Generate email and password
    email="${username}@example.com"
    password="${username}123!"
    
    # Make the HTTP request
    http POST http://localhost:5001/register \
        email="$email" \
        firstName="$firstName" \
        lastName="$lastName" \
        homeAddress="$address" \
        password="$password"
    
    # Display credentials
    echo "Email: $email"
    echo "Password: $password"
    echo "----------------------------------------"
done

echo "All test users created!"
