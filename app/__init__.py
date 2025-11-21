import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_bp
    from .users import users_bp
    from .products import products_bp
    from .posts import posts_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(posts_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app
