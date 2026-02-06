from app import app, db, ExamModel, UserModel

with app.app_context():
    db.create_all()