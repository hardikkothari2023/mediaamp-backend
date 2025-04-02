from flask import Blueprint, jsonify

# Define a Blueprint for API routes
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/your-endpoint', methods=['GET'])
def your_endpoint():
    return jsonify({"message": "API is working!"})
