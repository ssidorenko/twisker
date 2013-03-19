from flask import Flask

import settings

from make_json_app import make_json_app

app = make_json_app('twisker')
app.config.from_object('twisker.settings')

import views
