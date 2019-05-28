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

    @property
    def serialize(self):
        if self.candidate_path:
            candidate_path_serialize = [i.serialize for i in self.candidate_path]

        return {
            'name':     self.name,
            'color':    self.color,
            'paths':    candidate_path_serialize
        }


class CandidatePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.Text, nullable=False)
    # Foreign Key
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'))
    # Defince One To Many relashionship with SegmentList
    segment_list = db.relationship('SegmentList')

    def __init__(self, preference):
        self.preference = preference

    @property
    def serialize(self):
        if self.segment_list:
            segment_list_serialize = [i.serialize for i in self.segment_list]
        return {
            'preference':   self.preference,
            'hops':         segment_list_serialize
        }


class SegmentList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # Foreign Key
    candidate_path_id = db.Column(db.Integer, db.ForeignKey('candidate_path.id'))
    # Defince One To Many relashionship with LabelList
    label_list = db.relationship('LabelList')

    def __init__(self, name):
        self.name = name

    @property
    def serialize(self):
        if self.label_list:
            label_list_serialize = [i.serialize for i in self.label_list]

        return {
            'name': self.name,
            'labels': label_list_serialize
        }


class LabelList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer, nullable=False)
    # Foreign Key
    segment_list_id = db.Column(db.Integer, db.ForeignKey('segment_list.id'))

    def __init__(self, label):
        self.label = label

    @property
    def serialize(self):
        return {
            'label': self.label
        }


db.create_all()
db.session.commit()
