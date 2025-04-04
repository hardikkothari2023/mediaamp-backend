from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import db
from app.models.user import User
from app.models.task_logger import TaskLogger
from app.auth.decorators import role_required
from app.utils.redis_cache import cache_tasks_for_date, get_cached_tasks
from datetime import datetime, date


api_blueprint = Blueprint("api", __name__)

# ✅ User Registration
@api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # default to "user" if not provided

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ✅ User Login
@api_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
        return jsonify({"message": "Login successful", "token": access_token})

    return jsonify({"error": "Invalid username or password"}), 401

# ✅ Admin Dashboard
@api_blueprint.route("/admin/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})

# ✅ Moderator Dashboard
@api_blueprint.route("/moderator/dashboard", methods=["GET"])
@jwt_required()
@role_required("moderator")
def moderator_dashboard():
    return jsonify({"message": "Welcome to the moderator dashboard!"})

# ✅ User Dashboard
@api_blueprint.route("/user/dashboard", methods=["GET"])
@jwt_required()
@role_required("user")
def user_dashboard():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome to your dashboard, {current_user}!"})

# ✅ Tasks by Date (with Redis caching)
@api_blueprint.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks_by_date():
    query_date_str = request.args.get("date", date.today().isoformat())

    # Parse string to actual date object
    try:
        query_date = datetime.strptime(query_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Check Redis cache first
    cached = get_cached_tasks(query_date_str)
    if cached:
        return jsonify({"date": query_date_str, "tasks": cached, "cached": True})

    # Query DB using log_date
    logs = TaskLogger.query.filter_by(log_date=query_date).all()

    result = [
        {
            "id": log.id,
            "task_id": log.task_id,
            "status_snapshot": log.status_snapshot,
            "log_date": log.log_date.isoformat(),
        }
        for log in logs
    ]

    # Cache the result in Redis
    cache_tasks_for_date(query_date_str, result)

    return jsonify({"date": query_date_str, "tasks": result, "cached": False})