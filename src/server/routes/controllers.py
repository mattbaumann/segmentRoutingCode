import json
import os
import subprocess
from pathlib import Path

from flask import Flask, Blueprint, render_template, request, abort, jsonify

from src.server.extension.db_connection import db, Policy, CandidatePath, SegmentList, LabelList
from src.server.utils.http_status import BAD_REQUEST, OK

app = Flask(__name__)
app.config.from_object('config')

routes = Blueprint('index', __name__, template_folder='templates')

command = OK
command_operation = ''

raw_json = '[{"name": "P1", "color": 1, "paths": [{"preference": 10, "hops": [{"name": "Plist-1", "labels": [{"label": 16009, "type": "mpls-label"},{"label": 16004, "type": "mpls-label"},{"label": 16005, "type": "mpls-label"}]}]}]}, {"name": "P2", "color": 1, "paths": [{"preference": 10, "hops": [{"name": "Plist-1", "labels": [{"label": 16009, "type": "mpls-label"},{"label": 16004, "type": "mpls-label"},{"label": 16005, "type": "mpls-label"}]}]}]}]'


@routes.route('/')
def home():
    return render_template('static/index.html')


@routes.route('/about')
def about():
    return render_template('/static/about.html')


@routes.route('/testpolicy')
def testpolicy():
    test_policy = Policy('Policy_1', 111, 222, 333, 444)
    test_candidate_path = CandidatePath(555)
    test_segment_list = SegmentList('Segment List 1')
    test_label_list = LabelList(8888)
    test_label_list2 = LabelList(9999)

    test_policy.candidate_path.append(test_candidate_path)
    test_candidate_path.segment_list.append(test_segment_list)
    test_segment_list.label_list.append(test_label_list)
    test_segment_list.label_list.append(test_label_list2)

    db.session.add(test_policy)
    db.session.add(test_candidate_path)
    db.session.add(test_segment_list)
    db.session.add(test_label_list)
    db.session.add(test_label_list2)
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
    label_list = LabelList.query.join(SegmentList, SegmentList.id == LabelList.segment_list_id).filter(LabelList.id == segment_list_id).all()
    for item in label_list:
        print(item.label)
    return render_template('show/segment_list.html',
                           name=name,
                           candidate_path=candidate_path_id,
                           segment_list=segment_list,
                           label_list=label_list)


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
@routes.route('/command', methods=['GET', 'POST'])
def command():
    # TODO db auslesen und in json schreiben
    policy_query = Policy.query.all()

    return jsonify(json_list=[i.serialize for i in policy_query])

    # for policy in policy_query:
    #    for candidate_path in policy.candidate_path:
    #        return '{"name": "%s", "color": %d, "paths": %s' % (policy.name, self.color, "[" + ",".join(path.json() for path in self.paths) + "]}")
    #         print(candidate_path.preference)
    #         for segment_list in candidate_path.segment_list:
    #             print(segment_list.labels)
    # return "200 OK"

    # TODO
    # return '', NO_CONTENT
    # if status_code == OK:
    #     return 'write config'
    # elif status_code == NO_CONTENT:
    #     return 'update config'

    # return '', NO_CONTENT


@routes.route('/execute/<command>', methods=['POST'])
def execute(command):
    if command == 'read':
        script_path = Path(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = Path(script_path, "../../backend/backend.py").absolute()
        args = ["/usr/bin/python3", absolute_path, "-s " + request.url_root]
        subprocess.Popen(args)
        return render_template('update/inprogress.html')
    elif command == 'write':
        script_path = Path(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = Path(script_path, "../../backend/backend.py").absolute()
        args = ["/usr/bin/python3", absolute_path, "-s " + request.url_root]
        subprocess.Popen(args)
        return render_template('update/inprogress.html')
