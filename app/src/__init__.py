from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_backup.db'
    db.init_app(app)

    
    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()
        

    return app
