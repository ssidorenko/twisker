from twisker import app
from models import Twisk
from flask import render_template

@app.route('/twisks')
def list_twisks():
    twisks = Twisk.all()
    return "stub"

