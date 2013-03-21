from flask_login import LoginManager
from make_json_app import make_json_app

app = make_json_app('twisker')
app.config.from_object('twisker.settings')

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.setup_app(app)


import views
import login
