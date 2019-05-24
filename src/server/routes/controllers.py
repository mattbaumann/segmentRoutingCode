import json
import os
import subprocess
import sys
from pathlib import Path

from flask import Flask, Blueprint, render_template, request, abort

from src.server.extension.db_connection import db, Policy, CandidatePath, SegmentList
from src.server.utils.http_status import BAD_REQUEST, OK, NO_CONTENT

app = Flask(__name__)
app.config.from_object('config')

routes = Blueprint('index', __name__, template_folder='templates')

command = OK

raw_json = '[{"name": "P1", "color": 1, "paths": [{"preference": 10, "hops": [{"name": "Plist-1", "labels": [{"label": 16009, "type": "mpls-label"},{"label": 16004, "type": "mpls-label"},{"label": 16005, "type": "mpls-label"}]}]}]}, {"name": "P2", "color": 1, "paths": [{"preference": 10, "hops": [{"name": "Plist-1", "labels": [{"label": 16009, "type": "mpls-label"},{"label": 16004, "type": "mpls-label"},{"label": 16005, "type": "mpls-label"}]}]}]}]'


@routes.route('/')
def home():
    return render_template('static/index.html')


@routes.route('/about')
def about():


    return render_template('/static/about.html')


@routes.route('/testpolicy')
def testpolicy():
    test_policy = Policy('Policy_2', 123, 123, 123, 123)
    test_candidate_path = CandidatePath(123)
    test_segment_list = SegmentList('ItFinallyWorks')

    test_policy.candidate_path.append(test_candidate_path)
    test_candidate_path.segment_list.append(test_segment_list)

    db.session.add(test_policy)
    db.session.add(test_candidate_path)
    db.session.add(test_segment_list)
    db.session.commit()

    return 'insert policy into db'


@routes.route('/show/policy/')
def show_config():
    policy = Policy.query.all()
    return render_template('show/policy.html',
                           policy=policy)


@routes.route('/show/policy/<name>/candidatepath/<candidate_path_id>')
def show_candidate_path(name, candidate_path_id):
    candidate_path = CandidatePath.query.join(Policy, Policy.id == CandidatePath.policy_id).filter(CandidatePath.id == candidate_path_id).all()
    return render_template('show/candidate_path.html',
                           name=name,
                           candidate_path=candidate_path,
                           candidate_path_id=candidate_path_id)


@routes.route('/show/policy/<name>/candidatepath/<candidate_path_id>/segmentlist/<segment_list_id>')
def show_segment_list(name, candidate_path_id, segment_list_id):
    segment_list = SegmentList.query.join(CandidatePath, CandidatePath.id == SegmentList.candidate_path_id).filter(SegmentList.id == segment_list_id).all()
    print(segment_list)
    return render_template('show/segment_list.html',
                           name=name,
                           candidate_path=candidate_path_id,
                           segment_list=segment_list)


@routes.route('/update', methods=['POST'])
def update():
    # nice_json = json.loads(raw_json)
    if request.json is None:
        return "", BAD_REQUEST

    nice_json = json.loads(request.json)
    if json is None:
        abort(BAD_REQUEST)
    for policy in nice_json:
        insert_into_policy = Policy(str(policy['name']), str(policy['color']), '', '', '')
        db.session.add(insert_into_policy)

        for candidate_path in policy['paths']:
            insert_into_candidate_path = CandidatePath(str(candidate_path['preference']))
            insert_into_policy.candidate_path.append(insert_into_candidate_path)
            db.session.add(insert_into_candidate_path)

            for hop in candidate_path['hops']:
                insert_into_segment_list = SegmentList(str(hop['name']), str(hop['labels']))
                insert_into_candidate_path.segment_list.append(insert_into_segment_list)
                db.session.add(insert_into_segment_list)

        db.session.commit()
    return "", OK

# 200 OK, wenn config auf router geschrieben wird
# 204 NO_CONTENT, wenn auf dem router die config auf dem router gelesen
@routes.route('/command', methods=['POST'])
def command():
    # if status_code == OK:
    #     return 'write config'
    # elif status_code == NO_CONTENT:
    #     return 'update config'

    return '', NO_CONTENT


@routes.route('/execute', methods=['GET', 'POST'])
def execute():
    script_path = Path(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = Path(script_path, "../../backend/backend.py").absolute()
    args = [sys.executable, absolute_path, "-s " + request.url_root]
    subprocess.Popen(args)
    return render_template('update/inprogress.html')

