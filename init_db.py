from app import app, db  # make sure 'app' and 'db' are both imported from your app.py

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
