from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, USN Exam Planner"

if __name__ == "__main__":
    app.run(debug=True)