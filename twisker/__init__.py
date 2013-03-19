from flask import Flask
import settings

app = Flask('twisker')
app.config.from_object('twisker.settings')

import views
