from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class ExamModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    courseID = db.Column(db.String(80), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    def __repr__(self):
        return f"Exam(name = {self.name}, courseID = {self.courseID}, user_id = {self.user_id})"

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    exams = db.relationship("ExamModel", backref="user", lazy=True)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

exam_args = reqparse.RequestParser()
exam_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
exam_args.add_argument("courseID", type=str, required=True, help="CourseID cannot be blank")
exam_args.add_argument("user_id", type=int, required=True, help="User ID is required")

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")

examFields = {
    "id":fields.Integer,
    "name":fields.String,
    "courseID":fields.String,
    "user_id":fields.Integer
}

UserFields = {
    "id":fields.Integer,
    "name":fields.String,
    "email":fields.String
}

class Users(Resource):
    @marshal_with(UserFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(UserFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class UserExams(Resource):
    @marshal_with(examFields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, "User not found")
        exam = ExamModel.query.filter_by(user_id=id).all()
        return exam


class Exams(Resource):
    @marshal_with(examFields)
    def get(self):
        exams = ExamModel.query.all()
        return exams
    
    @marshal_with(examFields)
    def post(self):
        args = exam_args.parse_args()

        user = UserModel.query.get(args["user_id"])
        if not user:
            abort(404, "User not found")

        exam = ExamModel(
            name=args["name"],
            courseID=args["courseID"],
            user_id=args["user_id"]
        )

        db.session.add(exam)
        db.session.commit()

        return exam, 201

class Exam(Resource):
    @marshal_with(examFields)
    def get(self, id):
        exam = ExamModel.query.filter_by(id=id).first()
        if not exam:
            abort(404, "Exam not found")
        return exam
    
    @marshal_with(examFields)
    def delete(self, id):
        args = exam_args.parse_args()
        exam = ExamModel.query.filter_by(id=id).first()
        if not exam:
            abort(404, "Exam not found")
        exam.name = args["name"]
        exam.courseID = args["courseID"]
        db.session.delete(exam)
        db.session.commit()
        exams = ExamModel.query.all()
        return exams, 204

api.add_resource(Exams, '/api/exams')
api.add_resource(Exam, '/api/exams/<int:id>')
api.add_resource(Users, '/api/users')
api.add_resource(UserExams, '/api/users/<int:id>/exams')

@app.route("/")
def hello():
    return "Hello, USN Exam Planner"

if __name__ == "__main__":
    app.run(debug=True, port=5001)

 