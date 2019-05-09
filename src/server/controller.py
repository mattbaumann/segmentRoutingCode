import subprocess

from flask import render_template, redirect
from flask.views import View


class IndexView(View):
    methods = ['GET']

    def __init__(self, config):
        self.config = config

    def dispatch_request(self):
        # TODO: Load Config from Database
        return render_template('index.html', config=self.config)


class LoadConfigView(View):
    methods = ['GET']


    def __init__(self, config):
        self.config = config

    def dispatch_request(self):
        subprocess.Popen(["/home/matt/YDK-Test-Project/src/server/backend/backend.py"])
        return redirect("/")

class StoreConfigView(View):
    methods = ['POST']

    def __init__(self, config):
        self.config = config

    def dispatch_request(self):
        # TODO: Store Config -> Database