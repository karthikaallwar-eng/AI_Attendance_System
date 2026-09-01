from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# List of all students
students = ["Sudha","Student2","Student3","Student4"]

@app.route("/")
def dashboard():

    try:
        data = pd.read_csv("attendance.csv", names=["Name","Date","Time"])
        present = data["Name"].unique().tolist()
    except:
        present = []

    absent = [s for s in students if s not in present]

    return render_template(
        "dashboard.html",
        present=present,
        absent=absent,
        present_count=len(present),
        absent_count=len(absent)
    )

app.run(debug=True)