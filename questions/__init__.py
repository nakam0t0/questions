from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('questions.config')

db = SQLAlchemy(app)

import questions.views
