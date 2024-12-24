from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register routes
    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app
