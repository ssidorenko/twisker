#!/usr/bin/env python
from flask_login import LoginManager
from make_json_app import make_json_app


app = make_json_app('twisker')

app.config.from_object('twisker.settings')


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.setup_app(app)

from api import api
app.register_blueprint(api, url_prefix='/api')

import twisker.views
import twisker.login