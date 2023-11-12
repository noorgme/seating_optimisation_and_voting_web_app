from flask import render_template, request, redirect, url_for, flash, session
from . import app, db
from .models import User
from .forms import EmailForm, ScoringForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(email=form.email.data, name=form.name.data)
            db.session.add(user)
            db.session.commit()
            flash('You have been registered!')
        else:
            flash('Email already registered, proceed to scoring.')
        # Store email in session
        session['email'] = form.email.data
        return redirect(url_for('scoring'))
    return render_template('index.html', form=form)


@app.route('/scoring', methods=['POST'])
def submit_scores():
    scoring_form = ScoringForm()
    if request.method == "POST" and scoring_form.validate() and 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            # Update user's score for each startup
            user.convey_guru = scoring_form.convey_guru.data
            user.ekai = scoring_form.ekai.data
            user.fluenio = scoring_form.fluenio.data
            user.guliva = scoring_form.guliva.data
            user.hitcoach = scoring_form.hitcoach.data
            user.hybridcredit = scoring_form.hybridcredit.data
            user.matrx = scoring_form.matrx.data
            user.neutrally = scoring_form.neutrally.data
            user.omniabiosystems = scoring_form.omniabiosystems.data
            user.presalesai = scoring_form.presalesai.data
            user.propx = scoring_form.propx.data
            user.roma = scoring_form.roma.data
            db.session.commit()
            session.pop('email', None)  # Clear the session
            return 'Thank you for submitting your scores!'

    return redirect(url_for('index'))