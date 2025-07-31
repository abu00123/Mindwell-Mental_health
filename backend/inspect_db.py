from app import app, db, User  # Adjust if User model is in a different module

with app.app_context():
    users = User.query.all()
    if not users:
        print("⚠️ No users found in the database.")
    else:
        print(f"✅ Found {len(users)} user(s):")
        for user in users:
            print(f"- ID: {user.id}, Email: {user.email}, Password Hash: {user.password_hash}")

