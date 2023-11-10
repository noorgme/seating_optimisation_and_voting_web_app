from wtforms import Form, StringField, validators

class EmailForm(Form):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    firstname = StringField('First Name', [validators.DataRequired()])
    lastname = StringField('Last Name', [validators.DataRequired()])
