import subprocess
import sys

from flask import render_template
from flask.views import View

from .backend import backend


class IndexView(View):

    def __init__(self, config):
        self.config = config

    def dispatch_request(self):
        return render_template('index.html', config=self.config)


class LoadConfigView(View):

    def __init__(self, config):
        self.config = config

    def dispatch_request(self):
        print("test")
        # p = subprocess.Popen(["/home/matt/YDK-Test-Project/src/server/backend/backend.py"], stdout=sys.stdout, stderr=sys.stderr)
        p = subprocess.Popen(["/home/matt/YDK-Test-Project/src/server/backend/backend.py"])
        return render_template('index.html', config=self.config, policies=None)
