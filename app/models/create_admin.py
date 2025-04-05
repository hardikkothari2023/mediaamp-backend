from app import db, create_app
from app.models.user import User

app = create_app()

with app.app_context():
    new_user = User(username="admin", role="admin")
    new_user.set_password("adminpassword")  # Set a secure password

    db.session.add(new_user)
    db.session.commit()

    print("✅ Admin user created successfully!")
