from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from opensearchpy import OpenSearch
from redis import Redis
import rq

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()


login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

moment = Moment()
babel = Babel()


from app import models


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.opensearch = OpenSearch([app.config['OPENSEARCH_URL']]) \
        if app.config['OPENSEARCH_URL'] else None

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)
    dir_ = app.config['POSTS_JSON_DIR']
    if not os.path.exists(dir_):
        os.mkdir(dir_)

    from app.errors import errors_blueprint
    from app.auth import auth_blueprint
    from app.main import main_blueprint
    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


# from app.main import routes

@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(application.config['LANGUAGES'])
    return "uk"



