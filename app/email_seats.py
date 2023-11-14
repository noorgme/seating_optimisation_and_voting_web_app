import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
from .emailconfig import *

# Replace with your actual email and SMTP details
SMTP_SERVER = cSMTP_SERVER
SMTP_PORT = cPORT
SMTP_USERNAME = cSMTP_USERNAME
SMTP_PASSWORD = cSMTP_PASSWORD
FROM_EMAIL = cFROM_EMAIL
FROM_NAME = cFROM_NAME

# Function to parse the seating plan and return a dictionary of email to rounds
def parse_seating_plan(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    seating_plan = defaultdict(list)
    current_round = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('Round'):
            current_round = line.split(':')[0]
        elif line.endswith(')'):
            emails = line.split(': ')[-1].split(' ')
            for email in emails:
                seating_plan[email].append((current_round, line.split(' (')[0]))
    print(seating_plan)
    
    return seating_plan

# Function to send emails
def send_emails(seating_plan):
    # Set up the SMTP server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    
    for email, rounds in seating_plan.items():
        # Construct the email message
        body = "Hello from the Forge Team!\n\nYour seating plan for today is:\n"
        for round_info in rounds:
            body += f"{round_info[0]}: {round_info[1]}\n"
        body += "\nIf you have any questions, please ask the forge team members!"
        
        msg = MIMEText(body)
        msg['Subject'] = 'Your Seating Plan for Today'
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = email
        
        # Send the email
        server.send_message(msg)
    
    # Quit the server
    server.quit()

# Main function to process the seating plan and send emails
def process_and_send(file_path):
    seating_plan = parse_seating_plan(file_path)
    send_emails(seating_plan)
    print('Emails have been sent to all participants.')
