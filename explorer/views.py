#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify
from markupsafe import escape
from pathlib import Path

default_path = app.config["DEFAULT_PATH"]


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


@app.route("/", defaults={"subpath": None}, methods=["GET"])
@app.route("/<path:subpath>", methods=["GET"])
def home(subpath):
    if request.method == "GET":
        path = Path(default_path + subpath) if subpath else Path(default_path)
        if path.is_dir():
            return jsonify(_list_dir(path))
        # if valid file:
        #   open file
        else:
            abort(404)
