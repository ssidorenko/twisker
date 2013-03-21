from twisker import app
from flask import render_template

import api


@app.route('/')
def index():
    return render_template("index.html")
