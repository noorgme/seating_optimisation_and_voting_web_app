from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.email

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            return 'Email added!'
    return render_template_string('''
        <form method="POST">
            Email: <input type="email" name="email">
            <input type="submit">
        </form>
    ''')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
