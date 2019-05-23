from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.Text, nullable=False)
    bandwidth = db.Column(db.Text, nullable=False)
    latency = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Text, nullable=False)
    # Defince One To Many relashionship with CandidatePath
    candidate_path = db.relationship('CandidatePath')

    def __init__(self, name, color, bandwidth, latency, availability):
        self.name = name
        self.color = color
        self.bandwidth = bandwidth
        self.latency = latency
        self.availability = availability


class CandidatePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.Text, nullable=False)
    # Foreign Key
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'))
    # Defince One To Many relashionship with SegmentList
    segment_list = db.relationship('SegmentList')

    def __init__(self, preference):
        self.preference = preference


class SegmentList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    labels = db.Column(db.Text, nullable=False)
    # Foreign Key
    candidate_path_id = db.Column(db.Integer, db.ForeignKey('candidate_path.id'))

    def __init__(self, name, labels):
        self.name = name
        self.labels = labels


db.create_all()
db.session.commit()
