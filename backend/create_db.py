from app import app, db, ExamModel

with app.app_context():
    db.create_all()