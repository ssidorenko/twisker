from google.appengine.ext import ndb

from twisker import app
from flask import request, render_template, flash
from flask_login import login_required, current_user
from models import Twisk, TwiskUser, Tag

import api


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Shows all the twisks from the logged-in user feed"""
    twisks = []
    if request.method == "POST":
        twisk = Twisk(
            author=current_user.key,
            content=request.form['content']
        )
        twisk.put()

        # Append the twisk to the feed because the DB probably won't have
        # finished to apply the changes by the time this function has finished
        # executing
        twisks.append(twisk)

        flash("Twisk successfully posted !")

    twisks.extend(current_user.get_feed())
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
