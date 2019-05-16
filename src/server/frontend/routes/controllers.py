from flask import Flask, Blueprint, render_template, request
from server.frontend.extension.db_connection import Policy, CandidatePath, SegmentList

app = Flask(__name__)
app.config.from_object('config')

routes = Blueprint('index', __name__, template_folder='templates')


@routes.route('/')
def home():
    return render_template('static/index.html')


@routes.route('/about')
def about():
    return render_template('/static/about.html')


@routes.route('/show')
def show_config():
    # TODO load config from database
    # sr_config = SRConfig.query.filter(config='test').first()
    # print(sr_config)
    return 'show config'


@routes.route('/execute', methods=['GET', 'POST'])
# TODO add config as argument
def execute():
    if request.method == 'POST':
        # TODO execute script and write result into database
        # sr_config = SRConfig(config)
        # db.session.add(sr_config)
        # db.session.commit()
        return 'render template for execute script POST method'

    return 'execute template for execute script GET method'
