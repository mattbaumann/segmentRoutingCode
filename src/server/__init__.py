from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from src.server.routes.controllers import routes as mod_routes
from server.routes.controllers import routes as mod_routes

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(mod_routes)
