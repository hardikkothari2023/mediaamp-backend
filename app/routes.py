from flask import Blueprint, request, jsonify
from app import db  # Ensure db is imported
from app.models import User  # Ensure User model is imported

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):  # Ensure password is verified
        return jsonify({"message": "Login successful"})
    
    return jsonify({"error": "Invalid username or password"}), 401
