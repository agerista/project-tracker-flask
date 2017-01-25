from flask import Flask, request, render_template

import hackbright

# db = SQLAlchemy()

app = Flask(__name__)


@app.route("/")
def index():
    """Display home page"""

    return render_template("index.html")


@app.route("/student-search")
def get_student_form():
    """Which student do you want to search for?"""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)

    rows = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows)
    return html


@app.route("/student-add")
def get_student_add():
    """Which student do you want to add?"""

    return render_template("student_add.html")


@app.route("/student-add-success", methods=["POST"])
def student_add_success():
    """Add a student."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_add_success.html",
                           first_name=first_name,
                           last_name=last_name,
                           github=github,
                           method="POST")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
