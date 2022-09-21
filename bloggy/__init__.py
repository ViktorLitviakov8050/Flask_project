from flask import Flask
from bloggy.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bloggy import routes, models


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

