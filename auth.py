from flask import jsonify, request
from extensions import db, bcrypt
from sqlalchemy import text
import re

def register_user():
    try:
    data = request.get_json() if request.is_json else request.form

    # Extract fields
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

        # Validate input
        if not all([first_name, last_name, email, password]):
            return jsonify({"success": False, "message": "All fields are required"}), 400
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        # Check if user already exists
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
            if result.fetchone():
                return jsonify({"success": False, "message": "User already exists"}), 409

        # Hash the password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert the user into the database
        with db.engine.connect() as connection:
            connection.execute(text('''
                INSERT INTO users (first_name, last_name, email, password_hash)
                VALUES (:first_name, :last_name, :email, :password_hash)
            '''), {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password_hash": password_hash
            })
            connection.commit()

        # Get the created user to return user data
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
            user_row = result.fetchone()
            user_data = {
                "id": user_row[0],
                "first_name": user_row[1],
                "last_name": user_row[2],
                "email": user_row[3]
            }

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user": user_data
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Registration failed. Please try again."
        }), 500