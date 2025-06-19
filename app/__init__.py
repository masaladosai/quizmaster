from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] ='pizza'

    db.init_app(app)

    with app.app_context():
        from . import models  # ✅ Import AFTER `db.init_app(app)`
        db.create_all()       # ✅ Initialize database only ONCE
    from app.routes import register_blueprints
    register_blueprints(app)
    return app
