import time
from logging.handlers import TimedRotatingFileHandler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from application.utils.chat_minds_log_formatter import ChatMindsLogFormatter
from flask import Flask
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate(db)


def load_blueprints(app):
    from application.userland.controllers.user_controller import mod_userland as user_module
    app.register_blueprint(user_module)


def create_app(config_file_location=None):
    app = Flask(__name__, template_folder="templates")
    CORS(app)
    if config_file_location:
        app.config.from_pyfile(config_file_location, silent=False)
    else:
        app.config.from_pyfile('../config/dev.cfg', silent=True)
        app.config.from_pyfile('../config/prp.cfg', silent=True)
        app.config.from_pyfile('../config/prod.cfg', silent=False)

    from application.core.db_models import Users
    db.init_app(app)
    migrate.init_app(app, db)
    log_format = (
        "[%(asctime)s] %(levelname)s %(remote_addr)s %(request_type)s %(http_version)s %(url)s %(pathname)s rt:%(response_time)s %(message)s")
    log_formatter = ChatMindsLogFormatter(log_format)
    log_file = app.config['LOG_FILE_PATH']
    log_timed_rotating_handler = TimedRotatingFileHandler(log_file, when="midnight")
    log_timed_rotating_handler.setFormatter(log_formatter)
    log_timed_rotating_handler.setLevel(app.config['LOG_LEVEL'])
    app.static_folder = 'static'
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(log_timed_rotating_handler)
    load_blueprints(app)


    @app.template_filter('ctime')
    def epoch_to_datetime(s):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s)))

    return app
