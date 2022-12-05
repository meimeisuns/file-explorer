#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify
from markupsafe import escape
from pathlib import Path

default_path = app.config["DEFAULT_PATH"]


def _get_basic_attr(path: Path):
    return {
        "name": path.name,
        "owner": path.owner(),
        "size": path.stat().st_size,
        # TODO convert to MB GB
        "permissions": path.stat().st_mode,
    }


def _list_dir(path: Path):
    listing = []
    for entry in path.iterdir():
        listing.append(_get_basic_attr(entry))
    return listing


def _get_file_contents(file: Path):
    # TODO must make sure you have permissions
    attrs = _get_basic_attr(file)
    attrs["text"] = file.read_text()
    return attrs


@app.route("/", defaults={"subpath": None}, methods=["GET"])
@app.route("/<path:subpath>", methods=["GET"])
def home(subpath):
    if request.method == "GET":
        path = Path(default_path + escape(subpath)) if subpath else Path(default_path)
        if path.is_dir():
            return jsonify(_list_dir(path))
        elif path.is_file():
            return jsonify(_get_file_contents(path))
        else:
            abort(404)
