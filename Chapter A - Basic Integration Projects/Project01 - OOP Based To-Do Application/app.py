"""
Title: Basic CRUD Operations and OOP class integration

Components: Flask, Flask-Alchemy, Object-Oriented Programming

Requirements:
- Define a Task class with attributes: title, description, due_date, status.
- Persist tasks using Flask-SQLAlchemy
- Implement web interface to:
    - Add new tasks
    - List existing tasks
    - Update task status (complete/incomplete)
    - Delete tasks
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task {self.id}: {self.title}>"


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    due_date_str = request.form.get("due_date")

    if not title:
        return "Task title is required", 400

    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD", 400
    else:
        due_date = None

    new_task = Task(title=title, description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = not task.status
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
