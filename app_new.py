from app import create_app
from extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Grenada Athletics application...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
