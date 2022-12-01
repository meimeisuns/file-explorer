#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return "Hello, World!"
