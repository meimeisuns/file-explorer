from flask import Flask
import os

app = Flask(__name__)

default_path = os.environ.get("DIR") or "/"
if not default_path.endswith("/"):
    default_path += "/"
app.config["DEFAULT_PATH"] = default_path

import explorer.views
