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

    def __repr__(self):
        return f"Exam(name = {self.name}, courseID = {self.courseID})"

exam_args = reqparse.RequestParser()
exam_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
exam_args.add_argument("courseID", type=str, required=True, help="CourseID cannot be blank")

examFields = {
    "id":fields.Integer,
    "name":fields.String,
    "courseID":fields.String
}

class Exams(Resource):
    @marshal_with(examFields)
    def get(self):
        exams = ExamModel.query.all()
        return exams
    
    @marshal_with(examFields)
    def post(self):
        args = exam_args.parse_args()
        exam = ExamModel(name=args["name"], courseID=args["courseID"])
        db.session.add(exam)
        db.session.commit()
        exams = ExamModel.query.all()
        return exams, 201

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

@app.route("/")
def hello():
    return "Hello, USN Exam Planner"

if __name__ == "__main__":
    app.run(debug=True)