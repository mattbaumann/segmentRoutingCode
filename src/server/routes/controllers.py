import os
import subprocess
from pathlib import Path

from flask import Flask, Blueprint, render_template, request, abort

from src.server.extension.db_connection import db, Policy, CandidatePath, SegmentList
from src.server.utils.http_status import BAD_REQUEST

app = Flask(__name__)
app.config.from_object('config')

routes = Blueprint('index', __name__, template_folder='templates')


@routes.route('/')
def home():
    return render_template('static/index.html')


@routes.route('/about')
def about():
    return render_template('/static/about.html')


@routes.route('/testpolicy')
def testpolicy():
    name = 'Policy_1'
    color = 42
    bandwidth = 10000
    latency = 4
    availability = 1
    test_policy = Policy(name, color, bandwidth, latency, availability)
    db.session.add(test_policy)
    db.session.commit()

    return 'insert policy into db'


@routes.route('/testcandidatepath')
def testcandidatepath():
    preference = 13
    test_candidate_path = CandidatePath(preference)
    db.session.add(test_candidate_path)
    db.session.commit()

    return 'insert candidate path into db'


@routes.route('/testsegmentlist')
def testsegmentlist():
    name = 'MyAwesomeList'
    test_segment_list = SegmentList(name)
    db.session.add(test_segment_list)
    db.session.commit()

    return 'insert segment list into db'


@routes.route('/show/policy/<name>/')
def show_config(name):
    # TODO load config from database
    policy = Policy.query.filter_by(name=name).first()
    return render_template('show/policy.html', policy=policy)


@routes.route('/show/policy/<name>/candidatepath/<candidate_path_id>')
def show_candidate_path(name, candidate_path_id):
    candidate_path = CandidatePath.query.filter_by(id=candidate_path_id).first()
    return render_template('show/candidate_path.html', name=name, candidate_path=candidate_path)


@routes.route('/show/policy/<name>/candidatepath/<candidate_path_id>/segmentlist/<segment_list_id>')
def show_segment_list(name, candidate_path_id, segment_list_id):
    segment_list = SegmentList.query.filter_by(id=segment_list_id).first()
    return render_template('show/segment_list.html', name=name, candidate_path=candidate_path_id, segment_list=segment_list)


@routes.route('/update', methods=['POST'])
def update():
    json = request.json
    if json is None:
        abort(BAD_REQUEST)
    # TODO: Add data update handler


@routes.route('/execute', methods=['GET', 'POST'])
def execute():
    script_path = Path(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = Path(script_path, "../../backend/backend.py").absolute()
    args = ["/usr/bin/python3", "/home/matt/YDK-Test-Project/src/backend/backend.py", "-s " + request.url_root]
    subprocess.Popen(args)
    return render_template('update/inprogress.html')
