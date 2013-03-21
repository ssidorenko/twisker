from google.appengine.ext import ndb

from twisker import app
from flask import render_template
from flask_login import login_required, current_user
from models import Twisk, TwiskUser

import api


@app.route('/')
@login_required
def index():
    twisks = current_user.get_feed()
    return render_template("index.html", twisks=twisks)


@app.route('/user/<string:username>')
@login_required
def show_user(username):
    twisks = Twisk.gql("WHERE author = :1 ORDER BY when DESC LIMIT 50", ndb.Key(TwiskUser, username))
    return render_template("index.html", twisks=twisks)
