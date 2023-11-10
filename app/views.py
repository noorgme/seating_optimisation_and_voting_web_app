from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User
from app.forms import EmailForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash('Email added successfully!')
        return redirect(url_for('scoring'))
    return render_template('index.html', form=form)

@app.route("/scoring", methods = ['GET', 'POST'])
def scoring():
    return render_template("scoring.html")
