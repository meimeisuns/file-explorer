#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify, Response
from markupsafe import escape
from pathlib import Path

import explorer.utils as utils

default_path = app.config["DEFAULT_PATH"]


def _validate_post_request(path: Path, request_body):
    if path.is_file():
        abort(
            400,
            description=f"Unable to create new directory or file in file {path}. Please use the path for a directory.",
        )
    if not path.is_dir():
        abort(400, description="Please use the path for an existing directory.")
    request_body = request.json
    type = request_body.get("type")
    if not type or type not in ["dir", "file"]:
        abort(400, description="Please specify type as dir or file.")
    name = request_body.get("name")
    if not name:
        abort(400, description="Please provide name of directory or file to create.")


def _get(path: Path):
    if path.is_dir():
        return jsonify(utils.list_dir(path))
    elif path.is_file():
        return jsonify(utils.get_file_contents(path))
    else:
        abort(404)


def _post(str_path: str, request_body):
    path = Path(str_path)
    _validate_post_request(path, request_body)
    type = request_body.get("type")
    name = request_body.get("name")
    if type == "dir":
        try:
            new_path = Path(str_path + escape(name))
            new_path.mkdir()
            return Response(
                f"Directory {name}/ successfully created in {str_path}.",
                status=200,
            )
        except (FileExistsError, FileNotFoundError) as e:
            error = str(e)
            abort(400, description=f"Failed to create: {error}")
    elif type == "file":
        contents = request_body.get("contents")
        if contents is None:
            abort(400, description="Please provide contents for file.")
        new_path = Path(str_path + escape(name))
        with new_path.open("w", encoding="utf-8") as f:
            if contents != "":
                f.write(contents)
        return Response(
            f"File {name} successfully created in {str_path}.",
            status=200,
        )


@app.route("/", defaults={"subpath": None}, methods=["GET", "POST"])
@app.route("/<path:subpath>", methods=["GET", "POST"])
def home(subpath):
    str_curr_path = default_path + escape(subpath) if subpath else default_path
    curr_path = Path(str_curr_path)

    if request.method == "GET":
        return _get(curr_path)
    elif request.method == "POST":
        if not request.json:
            abort(400)
        if not str_curr_path.endswith("/"):
            str_curr_path += "/"
        request_body = request.json
        return _post(str_curr_path, request_body)
    else:
        abort(400)
