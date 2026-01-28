# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# app.py


from flask import Flask
from routes.auth import auth_bp     # Import the auth blueprint

def create_app():
    app = Flask(__name__)

    # Needed if we want to use session later
    app.secret_key = "dev-secret-key"

    # Register the auth blueprint
    app.register_blueprint(auth_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # start the Flask dev server