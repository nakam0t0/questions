from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('questions.config')

db = SQLAlchemy(app)

import questions.views
