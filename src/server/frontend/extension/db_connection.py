from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class SRConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.Text, nullable=False)

    def __init__(self, config):
        self.config = config


db.create_all()
db.session.commit()
