import os
from flask import Flask
from dotenv import load_dotenv

# Load .env from backend/.env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

from app.extensions import db, jwt
from app.config import Config

# Import blueprints
from app.api.auth import auth
from app.api.petitions import petitions
from app.api.departments import departments
from app.api.analytics import analytics
from app.api.notifications import notifications


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # ✅ Auto-create all tables when app starts (no python shell needed)
    with app.app_context():
        db.create_all()

    # Register routes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(petitions, url_prefix="/petitions")
    app.register_blueprint(departments, url_prefix="/departments")
    app.register_blueprint(analytics, url_prefix="/analytics")
    app.register_blueprint(notifications, url_prefix="/notifications")

    @app.route("/")
    def home():
        return {"status": "online", "message": "🔥 API Ready!"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






