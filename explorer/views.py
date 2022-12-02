#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify
import os
from pathlib import Path

current_path = Path(app.config["DEFAULT_PATH"])


def _list_dir(path: Path):
    listing = []
    for entry in path.iterdir():
        entry_info = {
            "name": entry.name if entry.is_file() else f"{entry.name}/",
            "owner": entry.owner(),
            "size": entry.stat().st_size,
            # TODO convert to MB GB
            "permissions": entry.stat().st_mode,
        }
        listing.append(entry_info)
    return listing


def _open_file(path: Path):
    # TODO must make sure you have permissions
    # if entry.is_file():
    #    entry_info["contents"] = entry.read_text()
    pass


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        # TODO if path specified in url, add to current path
        # if valid dir:
        return jsonify(_list_dir(current_path))
        # else abort
