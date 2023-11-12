from wtforms import StringField, validators, IntegerField
from flask_wtf import FlaskForm

class EmailForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    fullname = StringField('Full Name', [validators.DataRequired()])

class ScoringForm(FlaskForm):
    convey_guru = IntegerField('Convey Guru', default=0)
    ekai = IntegerField('EKAI', default=0)
    fluenio = IntegerField('Fluen.io', default=0)
    guliva = IntegerField('Guliva', default=0)
    hitcoach = IntegerField('HIT Coach', default=0)
    hybridcredit = IntegerField('Hybrid Credit', default=0)
    matrx = IntegerField('MATRX', default=0)
    neutrally = IntegerField('Neutrally', default=0)
    omniabiosystems = IntegerField('Omnia Biosystems', default=0)
    presalesai = IntegerField('Presales.ai', default=0)
    propx = IntegerField('PropX', default=0)
    roma = IntegerField('ROMA', default=0)