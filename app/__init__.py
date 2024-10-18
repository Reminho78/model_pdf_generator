from flask import Flask
from flask_migrate import Migrate
from app.extensions import db  # Importe db depuis extensions.py

migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Configure l'URI de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://remidubenard:ricketmorty@localhost/facoto_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialiser l'instance SQLAlchemy avec l'application Flask
    db.init_app(app)
    migrate.init_app(app, db)

    # Importer les blueprints ou les routes
    from app.routes import main
    app.register_blueprint(main)

    return app