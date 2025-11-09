"""
Title: Personal URL Shortener

Subject: Database-supported redirection and basic statistics.

Components: Flask, Flask-SQLAlchemy, random module

Requirements:
- Define a URL model with the following attributes:
    - short_url
    - original_url
    - click_count
- General a unique short code for a given URL using random module
- Create a dynamic route (/<short_code>) and implement redirection using redirect() function.
- Increment the visit count for the corresponding record each time there is a redirect
"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(8), unique=True, nullable=False)
    original_url = db.Column(db.String(500), nullable=False)
    click_count = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()


def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(length))
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url


@app.route('/', methods=['GET', 'POST'])
def index():
    shortened_url = None

    if request.method == 'POST':
        original_url = request.form['original_url']

        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url

        short_url = generate_short_url()
        new_url = URL(short_url=short_url, original_url=original_url)

        shortened_url = f"{request.host_url}{short_url}"

        db.session.add(new_url)
        db.session.commit()

    return render_template('index.html', shortened_url=shortened_url)


@app.route('/<short_url>')
def direct_to_original(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        url.click_count += 1
        db.session.commit()
        return redirect(url.original_url)
    else:
        return "URL not found", 404


if __name__ == '__main__':
    app.run(debug=True)
