from app import app, db

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
