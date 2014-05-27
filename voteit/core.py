from urlparse import urlparse

from flask import Flask, url_for as _url_for
from pymongo import MongoClient

from voteit import default_settings


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('VOTEIT_SETTINGS', silent=True)

mongo_uri = urlparse(app.config.get('MONGODB_URI'))
conn = MongoClient(host=mongo_uri.hostname, port=mongo_uri.port)
db = conn[mongo_uri.path.replace('/', '')]

motions = db['motions']
vote_events = db['vote_events']
vote_counts = db['vote_counts']
votes = db['votes']


def url_for(*a, **kw):
    try:
        return _url_for(*a, _external=True, **kw)
    except RuntimeError:
        return None
