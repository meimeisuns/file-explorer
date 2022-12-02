from flask import Flask
import os

app = Flask(__name__)
app.config['DEFAULT_PATH'] = os.environ.get("DIR") or "/"

import explorer.views
