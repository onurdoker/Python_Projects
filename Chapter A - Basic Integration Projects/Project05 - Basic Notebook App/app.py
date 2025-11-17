"""
Title: Basic Notebook App Api

Subject: JSON responses and RESTFUL CRUD concept

Components: FLask, Flask-SQLAlchemy, Jsonify

Requirements:
- Define a Note model (with the title and content attributes)
- GET /api/notes: List all notes in JSON format using jsonify()
- POST /api/notes: Add a new note using request.get_json()
- GET /api/notes/<int:id> : Retrieve a single note by IDin JSON format, returning 404 if not found.
"""

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = [
        {
            'id': note.id,
            'title': note.title,
            'content': note.content
            }
        for note in Note.query.all()
        ]

    return jsonify(notes)


@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify(
            {
                'id': new_note.id,
                'title': new_note.title,
                'content': new_note.content
                }), 201


@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get_or_404(id)
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content
        })


if __name__ == '__main__':
    app.run(debug=True)
