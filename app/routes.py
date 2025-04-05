from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import db
from app.models.user import User
from app.models.task_logger import TaskLogger
from app.auth.decorators import role_required
from app.utils.redis_cache import cache_tasks_for_date, get_cached_tasks
from datetime import datetime, date
from io import TextIOWrapper
import csv
from flask_jwt_extended import jwt_required
from app.models.task_manager import TaskManager
from flasgger.utils import swag_from
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User   
from flasgger.utils import swag_from
from flask import request, jsonify
from app.models.user import User  
from app.extensions import db

api_blueprint = Blueprint("api", __name__)



@api_blueprint.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'adminuser'},
                    'password': {'type': 'string', 'example': 'strongpassword123'},
                    'role': {'type': 'string', 'enum': ['admin', 'moderator', 'user'], 'example': 'user'}
                },
                'required': ['username', 'password', 'role']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'User registered successfully'}
                }
            }
        },
        400: {'description': 'Username and password are required'},
        409: {'description': 'Username already exists'},
        415: {'description': 'Request must be JSON'}
    }
})
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
 


@api_blueprint.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Login with username and password to receive JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'adminuser'},
                    'password': {'type': 'string', 'example': 'adminpass'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Login successful'},
                    'token': {'type': 'string', 'example': 'your.jwt.token'}
                }
            }
        },
        401: {'description': 'Invalid username or password'},
        415: {'description': 'Unsupported Media Type'}
    }
})
def login():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
        return jsonify({"message": "Login successful", "token": access_token})

    return jsonify({"error": "Invalid username or password"}), 401

@api_blueprint.route("/admin/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
@swag_from({
    'tags': ['Dashboard'],
    'summary': 'Admin Dashboard',
    'parameters': [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "default": "Bearer <paste_your_token_here>",
            "description": "JWT token in the format: Bearer <your_token>"
        }
    ],
    'responses': {
        200: {
            'description': 'Admin access success',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Welcome to the admin dashboard!'}
                }
            }
        },
        401: {'description': 'Missing or invalid token'},
        403: {'description': 'Access denied'}
    }
})
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})

@api_blueprint.route("/moderator/dashboard", methods=["GET"])
@jwt_required()
@role_required("moderator")
@swag_from({
    'tags': ['Dashboard'],
    'summary': 'Moderator Dashboard',
    'parameters': [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "default": "Bearer <paste_your_token_here>",
            "description": "JWT token in the format: Bearer <your_token>"
        }
    ],
    'responses': {
        200: {
            'description': 'Moderator access success',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Welcome to the moderator dashboard!'}
                }
            }
        },
        401: {'description': 'Missing or invalid token'},
        403: {'description': 'Access denied'}
    }
})
def moderator_dashboard():
    return jsonify({"message": "Welcome to the moderator dashboard!"})

@api_blueprint.route("/user/dashboard", methods=["GET"])
@jwt_required()
@role_required("user")
@swag_from({
    'tags': ['Dashboard'],
    'summary': 'User Dashboard',
    'parameters': [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "default": "Bearer <paste_your_token_here>",
            "description": "JWT token in the format: Bearer <your_token>"
        }
    ],
    'responses': {
        200: {
            'description': 'User access success',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Welcome to the user dashboard!'}
                }
            }
        },
        401: {'description': 'Missing or invalid token'},
        403: {'description': 'Access denied'}
    }
})
def user_dashboard():
    return jsonify({"message": "Welcome to the user dashboard!"})

@api_blueprint.route("/upload-csv", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Upload a CSV file and bulk insert into TaskManager table',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'CSV file containing task data'
        }
    ],
    'security': [
        {
            'Bearer': []
        }
    ],
    'responses': {
        200: {'description': 'CSV data uploaded and stored successfully'},
        400: {'description': 'Invalid CSV or missing fields'},
        500: {'description': 'Internal server error'}
    }
})
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        stream = TextIOWrapper(file.stream, encoding='utf-8')
        csv_reader = csv.DictReader(stream)

        for row in csv_reader:
            task = TaskManager(
                task_name=row['task_name'],
                description=row['description'],
                status=row['status'].lower() == 'true',
                priority=row['priority'],
                created_at=datetime.strptime(row['created_at'], "%m/%d/%Y"),
                assigned_user=row['assigned_user']
            )
            db.session.add(task)

        db.session.commit()

        return jsonify({"message": "Tasks uploaded successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to process CSV: {str(e)}"}), 500
 
from app.models.task_manager import TaskManager
 
@api_blueprint.route("/task", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Create a new task',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'task_name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'status': {'type': 'boolean'},
                    'priority': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date'},
                    'assigned_user': {'type': 'string'},
                },
                'required': ['task_name', 'description', 'status', 'priority', 'created_at', 'assigned_user']
            }
        }
    ],
    'responses': {
        201: {'description': 'Task created successfully'},
        400: {'description': 'Missing fields'}
    }
})
def create_task():
    data = request.get_json()
    try:
        task = TaskManager(
            task_name=data["task_name"],
            description=data["description"],
            status=data["status"],
            priority=data["priority"],
            created_at=datetime.strptime(data["created_at"], "%Y-%m-%d"),
            assigned_user=data["assigned_user"]
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created", "task_id": task.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ✅ GET /task/<id> - Get a task
@api_blueprint.route("/task/<int:id>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get task by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'security': [{'Bearer': []}],
    'responses': {
        200: {'description': 'Task found'},
        404: {'description': 'Task not found'}
    }
})
def get_task(id):
    task = TaskManager.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "id": task.id,
        "task_name": task.task_name,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": task.created_at.isoformat(),
        "assigned_user": task.assigned_user
    })


# ✅ PUT /task/<id> - Update task
@api_blueprint.route("/task/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Update a task by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'task_name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'status': {'type': 'boolean'},
                    'priority': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date'},
                    'assigned_user': {'type': 'string'}
                }
            }
        }
    ],
    'security': [{'Bearer': []}],
    'responses': {
        200: {'description': 'Task updated'},
        404: {'description': 'Task not found'}
    }
})
def update_task(id):
    task = TaskManager.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    try:
        task.task_name = data.get("task_name", task.task_name)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)
        task.priority = data.get("priority", task.priority)
        if "created_at" in data:
            task.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d")
        task.assigned_user = data.get("assigned_user", task.assigned_user)
        db.session.commit()
        return jsonify({"message": "Task updated"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ✅ DELETE /task/<id> - Delete task
@api_blueprint.route("/task/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Delete a task by ID',
    'parameters': [{'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}],
    'security': [{'Bearer': []}],
    'responses': {
        200: {'description': 'Task deleted'},
        404: {'description': 'Task not found'}
    }
})
def delete_task(id):
    task = TaskManager.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
