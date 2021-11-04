from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/computers-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.add_toy(request.form['name'])
        return redirect(url_for('index'))
    return render_template('index.html', toys=db.get_all_toys())
    
@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys/<int:id>', methods=["GET", "POST", "DELETE"])
def show(id):

    found_toy = db.find_toy(id)

    if request.method == "POST":
        if request.url[-12::] == "method=PATCH":
            db.change_name(request.form['name'], id)
            return redirect(url_for('index'))
        if request.url[-13::] == "method=DELETE":
            db.delete_toy(id)
            return redirect(url_for('index'))
        
        return redirect(url_for('index'))

    return render_template('show.html', toy=found_toy)

@app.route('/toys/<int:id>/edit')
def edit(id):
    found_toy = db.find_toy(id)

    return render_template('edit.html', toy=found_toy)
