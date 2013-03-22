from google.appengine.ext import ndb

from twisker import app
from flask import render_template
from flask_login import login_required, current_user
from models import Twisk, TwiskUser

import api


@app.route('/')
@login_required
def index():
    """Shows all the twisks from the logged-in user feed"""
    twisks = current_user.get_feed()
    return render_template("index.html", twisks=twisks)


@app.route('/user/<string:username>')
@login_required
def show_user(username):
    """Shows all the twisks posted by a given user"""
    twisks = Twisk.gql("WHERE author = :1 ORDER BY when DESC LIMIT 50",
                       ndb.Key(TwiskUser, username))
    return render_template("index.html", twisks=twisks)


@app.route('/tag/<string:tag>')
@login_required
def show_tag(tag):
    """Shows all the twisks tagged with the given tag"""
    twisks = Twisk.get_tag_feed(tag)
    return render_template("index.html", twisks=twisks,
                           no_twisks_message="No twisks with this tag !")
