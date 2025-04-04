from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User  # Import User directly from models.user
from app.auth.decorators import role_required  # Custom decorator for RBAC
import jwt  # Add this at the top if not already present
from app.config import Config  # Add this to access the secret key
from flask_jwt_extended import create_access_token
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # ✅ Correct JWT generation using flask_jwt_extended
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)

        return jsonify({"message": "Login successful", "token": access_token})

    return jsonify({"error": "Invalid username or password"}), 401
# ✅ New route for user registration
@api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # default to "user" if not provided

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    # Create new user with hashed password
    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ✅ Admin-only route (RBAC)
@api_blueprint.route("/admin/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})
