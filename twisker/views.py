from twisker import app
from models import Twisk
from flask import render_template

@app.route('/twisks')
def list_twisks():
    twisks = Twisk.all()
    return ";".join([t.content for t in twisks])

@app.route('/twisk/<int:id>')
def get_twisk(id):
    Twisk.get_by_id(id).content
