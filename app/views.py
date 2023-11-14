from flask import render_template, request, redirect, url_for, flash, session
from . import app, db, email_seats
from .models import User
from .forms import EmailForm, ScoringForm
import random
import os
from .algorithm import investor_seats
import re
from collections import defaultdict

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
        
        return redirect(url_for('seats'))  # Redirect to a seating page 

    # If GET request, render the scoring template
    return render_template('scoring.html')

@app.route("/seats", methods=["GET"])
def seats():
    if 'email' not in session:
        # Redirect user to login page if they're not logged in
        return redirect(url_for('index'))  # Ensure you have a login route defined

    user_email = session['email']
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        # Handle the case where the user is not found
        return "User not found", 404

    # Assuming 'round_1', 'round_2', and 'round_3' are columns in your User model
    seating_plan = {
        'round_1': user.round_1,
        'round_2': user.round_2,
        'round_3': user.round_3
    }
    
    return render_template('seats.html', seating_plan=seating_plan)

@app.route('/admin', methods =['GET'])
def admin():
    output_dir = os.path.join(app.root_path, 'algorithm')
    file_path = os.path.join(output_dir, 'parsed.txt')
    if request.method == "GET":
            # Read the content of the file
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            file_content = ''
            flash('File not found.')
        user_count = User.query.count()
        users_with_scores = User.query.filter(
        (User.convey_guru > 0) |
        (User.ekai > 0) |
        (User.fluenio > 0) |
        (User.guliva > 0) |
        (User.hitcoach > 0) |
        (User.hybridcredit > 0) |
        (User.matrx > 0) |
        (User.neutrally > 0) |
        (User.omniabiosystems > 0) |
        (User.presalesai > 0) |
        (User.propx > 0) |
        (User.roma > 0)
        ).count()
        return render_template("admin.html", user_count=user_count, users_with_scores=users_with_scores, file_content=file_content)

@app.route('/admin/add_user', methods=['POST'])
def admin_add_user():
    email = request.form.get('email')
    name = request.form.get('name')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('A user with this email already exists.')
    else:
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()
        flash('New user added successfully.')
    return redirect(url_for('admin'))


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
    return redirect(url_for('admin'))

@app.route('/admin/email', methods=['GET'])
def admin_email():
    
    # Ensure the output directory exists
    output_dir = os.path.join(app.root_path, 'algorithm')
    output_path = os.path.join(output_dir, 'output.txt')
    email_seats.process_and_send(output_path)
    
    return redirect(url_for('index'))

@app.route('/admin/parse', methods=['GET'])
def admin_parse():
    output_dir = os.path.join(app.root_path, 'algorithm')
    file_path = os.path.join(output_dir, 'output.txt')
    parsed_file = os.path.join(output_dir, 'parsed.txt')

    with open(file_path, 'r') as file:
        content = file.read()
        
    rounds = content.split('Round')
    seating_plan = defaultdict(list)
    table_numbers = {
    "Hybrid Credit": 1,
    "Omnia Biosystems": 2,
    "HIT Coach": 3,
    "Convey Guru": 4,
    "Neutrally": 5,
    "ROMA": 6,
    "MATRX": 7,
    "Fluen.io": 8,
    "Guliva": 9,
    "Presales.ai": 10,
    "PropX": 11,
    "EKAI": 12
    }

    
    # Skip the first split since it's before "Round 1"
    for round_details in rounds[1:]: 
        round_number = round_details.split(':')[0].strip()
        tables = round_details.split('\n')[1:]  # Skip the first element since it's "Round X"
        for table in tables:
            if table:  # Check if table string is not empty
                # Extract table name and emails
                table_name = re.search(r'(.*) \(Table Size: \d+\):', table).group(1).strip()
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', table)
                for email in emails:
                     
                    seating_plan[email].append((round_number, table_numbers[table_name]))
    
    # Write parsed seating plan to file
    with open(parsed_file, 'w') as out_file:
        for email, tables in seating_plan.items():
            out_file.write(f'{email}\n')
            for round_number, table_name in tables:
                out_file.write(f'{round_number}, {table_name}\n')
            out_file.write('\n')
        add_plan_to_db()
    return redirect(url_for('admin'))
    
@app.route('/admin/present', methods=['GET'])
def add_plan_to_db():
    output_dir = os.path.join(app.root_path, 'algorithm')
    # file_path = os.path.join(output_dir, 'output.txt')
    parsed_file = os.path.join(output_dir, 'parsed.txt')
    with open(parsed_file, 'r') as file:
        lines = file.readlines()

    # Process the file
    email = None
    for line in lines:
        # If the line contains an email, it's a new user
        if '@' in line.strip():
            email = line.strip()
        else:
            # Otherwise, it's the round and table information
            round_info = line.strip().split(', ')
            if len(round_info) == 2:
                round_number, table_number = round_info
                table_number = int(table_number)  # Convert table number to integer
                
                # Retrieve the user and update the correct round
                user = User.query.filter_by(email=email).first()
                if user:
                    if round_number == '1':
                        user.round_1 = table_number
                    elif round_number == '2':
                        user.round_2 = table_number
                    elif round_number == '3':
                        user.round_3 = table_number
                    else:
                        print(f"Invalid round number {round_number} for user {email}")
                else:
                    print(f"User with email {email} not found")

    # Commit the changes to the database after processing all users
    db.session.commit()




    
    return redirect(url_for('admin'))


@app.route('/admin/edit_file', methods=['POST'])
def admin_edit_file():
    file_content = request.form.get('file_content')
    output_dir = os.path.join(app.root_path, 'algorithm')
    file_path = os.path.join(output_dir, 'parsed.txt')
    # Update to your file's path

    # Save the updated content back to the file
    try:
        with open(file_path, 'w') as file:
            file.write(file_content)
            add_plan_to_db()
        flash('File saved successfully.')
    except Exception as e:
        flash('An error occurred while saving the file.')
        app.logger.error('File save error: %s', e)

    return redirect(url_for('admin'))

@app.route('/admin/clear_table', methods=['POST'])
def admin_clear_table():
    try:
        # Delete all records in the User table
        db.session.query(User).delete()
        db.session.commit()
        flash('All data has been cleared.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing data: {e}', 'error')
        app.logger.error('Error clearing table: %s', e)

    return redirect(url_for('admin'))

