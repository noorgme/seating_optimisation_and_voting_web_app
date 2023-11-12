from flask import render_template, request, redirect, url_for, flash, session
from . import app, db
from .models import User
from .forms import EmailForm, ScoringForm
import random
import os
from .algorithm import investor_seats

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
            flash('You have been registered!')
        else:
            flash('Email already registered, proceed to scoring.')
        session['email'] = email  # Store email in session
        return redirect(url_for('scoring'))  # Make sure the 'scoring' view function exists
    return render_template('index.html')


@app.route('/scoring', methods=['GET', 'POST'])
def scoring():
    # Redirect to index if no session is present (user not logged in)
    if 'email' not in session:
        flash('Please enter your details to start scoring.')
        return redirect(url_for('index'))

    if request.method == "POST":
        user = User.query.filter_by(email=session.get('email')).first()
        
        # Ensure the user exists in the session
        if not user:
            flash('There was a problem with your session. Please start over.')
            session.pop('email', None)  # Clear the session
            return redirect(url_for('index'))
        
        # Manually get each score from the form and update the user object
        try:
            user.convey_guru = int(request.form.get('conveyrating', 0))
            user.ekai = int(request.form.get('ekairating', 0))
            user.fluenio = int(request.form.get('flueniorating', 0))
            user.guliva = int(request.form.get('gulivarating', 0))
            user.hitcoach = int(request.form.get('hitcoachrating', 0))
            user.hybridcredit = int(request.form.get('hybridrating', 0))
            user.matrx = int(request.form.get('matrxrating', 0))
            user.neutrally = int(request.form.get('neutrallyrating', 0))
            user.omniabiosystems = int(request.form.get('omniarating', 0))
            user.presalesai = int(request.form.get('presalesrating', 0))
            user.propx = int(request.form.get('propxrating', 0))
            user.roma = int(request.form.get('romarating', 0))
        except ValueError:
            # Handle the error if the score is not a valid integer
            flash('There was an error with the input. Please enter valid scores.')
            return redirect(url_for('scoring'))
        
        # Save changes to the database
        db.session.commit()

        flash('Thank you for submitting your scores!')
        session.pop('email', None)  # Clear the session to log out the user
        return redirect(url_for('index'))  # Redirect to a 'thank you' page or some other page

    # If GET request, render the scoring template
    return render_template('scoring.html')

@app.route('/admin', methods =['GET'])
def admin():
    if request.method == "GET":
        return render_template("admin.html")

@app.route('/admin/download', methods=['GET'])
def admin_download():
    # Ensure the output directory exists
    output_dir = os.path.join(app.root_path, 'algorithm')
    companies_dir = os.path.join(output_dir, 'companies.txt')
    os.makedirs(output_dir, exist_ok=True)
    votes_path = os.path.join(output_dir, 'votes.txt')
    output_path = os.path.join(output_dir, 'output.txt')
    
    # Query all users
    users = User.query.all()
    lines = []

    for user in users:
        # Extract scores into a dictionary
        scores = {
            'Convey Guru': user.convey_guru,
            'EKAI': user.ekai,
            'Fluen.io': user.fluenio,
            'Guliva': user.guliva,
            'HIT Coach': user.hitcoach,
            'Hybrid Credit': user.hybridcredit,
            'MATRX': user.matrx,
            'Neutrally': user.neutrally,
            'Omnia Biosystems': user.omniabiosystems,
            'Presales.ai': user.presalesai,
            'PropX': user.propx,
            'ROMA': user.roma
        }

        # Sort scores by value in descending order and resolve ties randomly
        sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], random.random()))

        # Select the top 5 scores
        top_companies = [company for company, score in sorted_scores[:5]]

        # Construct the line to be written to the text file
        line = f"{user.email}," + ",".join(top_companies)
        lines.append(line)
    
    # Write the lines to the output file
    with open(votes_path, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")
    


    # Flash message or log to server that file has been saved
    flash('Top scores have been saved to votes.txt in the output directory.')
    
    # Redirect to the admin page or provide a message
    return redirect(url_for('admin'))

@app.route('/admin/process', methods=['GET'])
def admin_process():
    # Ensure the output directory exists
    output_dir = os.path.join(app.root_path, 'algorithm')
    os.makedirs(output_dir, exist_ok=True)

    companies_dir = os.path.join(output_dir, 'companies.txt')
    votes_path = os.path.join(output_dir, 'votes.txt')
    companies_and_votes = os.path.join(output_dir, 'companies_and_votes.txt')
    output_path = os.path.join(output_dir, 'output.txt')
    
    with open(votes_path, 'r') as votes:
        with open(companies_dir, 'r') as companies:
            with open(companies_and_votes, "w") as input:
                input.write(companies.read())
                input.write(votes.read())
                votes.seek(0)
                companies.seek(0)
    
    # Optimise seats:
    investor_seats.seat(companies_and_votes, output_path)
    return redirect(url_for('index'))