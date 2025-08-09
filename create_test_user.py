from app import app, db, User

with app.app_context():
    # Check if the user already exists
    existing = User.query.filter_by(email="test@example.com").first()
    if existing:
        print("Test user already exists.")
    else:
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        user.set_password("TestPassword123")  # ✅ hashed properly
        db.session.add(user)
        db.session.commit()
        print("✅ Test user created with password: TestPassword123")
