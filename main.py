from flask import Flask
from google.auth.transport import requests
from google.cloud import datastore

import feedapp.base as base
import feedapp.stat as stat
import feedapp.privacy as privacy
import feedapp.utils as utils

firebase_request_adapter = requests.Request()

datastore_client = datastore.Client()

app = Flask(__name__)

app.register_blueprint(base.bp)

app.register_blueprint(stat.bp)

app.register_blueprint(privacy.bp)

app.secret_key = '1781231hansddcxlzknz'

app.jinja_env.globals.update(get_name_for_month=utils.get_name_for_month)
