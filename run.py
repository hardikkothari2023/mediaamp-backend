from flasgger import Swagger
from app import create_app
 
app = create_app()
 
swagger_template = {
    "swagger": "2.0",  
    "info": {
        "title": "MediaAmp API",
        "description": "API for MediaAmp Backend Task",
        "version": "1.0.0"
    },
    "securityDefinitions": {   
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "tags": [
        {
            "name": "Auth",
            "description": "User registration and login"
        },
        {
            "name": "Dashboard",
            "description": "Role-based dashboard endpoints"
        },
        {
            "name": "Tasks",
            "description": "Task management and CSV upload"
        }
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "static_url_path": "/flasgger_static",
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
