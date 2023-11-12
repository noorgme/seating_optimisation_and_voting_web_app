from faker import Faker
import random
from app import app, db
from app.models import User

# Initialize the Faker library
fake = Faker()

# Initialise flask app context

with app.app_context():
        
    # Clear the User table
    try:
        num_rows_deleted = db.session.query(User).delete()
        db.session.commit()
        print(f"Cleared {num_rows_deleted} existing users.")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing the database: {e}")
        exit(1)  # Exit if cannot clear the database
    # Define the number of users
    NUM_USERS = 60

    # Define a list of your startup names as they appear in your model
    startup_names = [
        'convey_guru', 'ekai', 'fluenio', 'guliva', 'hitcoach',
        'hybridcredit', 'matrx', 'neutrally', 'omniabiosystems',
        'presalesai', 'propx', 'roma'
    ]

    # Generate random users
    for _ in range(NUM_USERS):
        # Create a new user with a random name and email
        name = fake.name()
        email = fake.email()

        # Create a new User object
        new_user = User(email=email, name=name)

        # Assign random scores between 1 and 10 for each startup
        for startup in startup_names:
            setattr(new_user, startup, random.randint(1, 10))

        # Add the new user to the session and commit to the database
        db.session.add(new_user)

    # Commit all new users to the database
    db.session.commit()

    print(f"Added {NUM_USERS} new users with random votes to the database.")
