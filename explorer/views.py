#!/usr/bin/env python3

from explorer import app
from flask import abort, request, jsonify, Response
from markupsafe import escape
from pathlib import Path

default_path = app.config["DEFAULT_PATH"]


def _get_basic_attr(path: Path):
    return {
        "name": f"{path.name}/" if path.is_dir() else path.name,
        "owner": path.owner(),
        "size_bytes": path.stat().st_size,
        "permissions": path.stat().st_mode,
    }


def _list_dir(path: Path):
    listing = []
    for entry in path.iterdir():
        listing.append(_get_basic_attr(entry))
    return listing


def _get_file_contents(file: Path):
    attrs = _get_basic_attr(file)
    attrs["text"] = file.read_text()
    return attrs


@app.route("/", defaults={"subpath": None}, methods=["GET", "POST"])
@app.route("/<path:subpath>", methods=["GET", "POST"])
def home(subpath):
    str_curr_path = default_path + escape(subpath) if subpath else default_path
    curr_path = Path(str_curr_path)

    if request.method == "GET":
        if curr_path.is_dir():
            return jsonify(_list_dir(curr_path))
        elif curr_path.is_file():
            return jsonify(_get_file_contents(curr_path))
        else:
            abort(404)
    elif request.method == "POST":
        if not request.json:
            return abort(400)
        request_body = request.json
        type = request_body.get("type")
        if not type or type not in ["dir", "file"]:
            abort(400, description="Please specify type as dir or file.")
        name = request_body.get("name")
        contents = request_body.get("contents")
        if type == "dir":
            try:
                if not type or not name:
                    abort(
                        400, description="Please provide name of directory to create."
                    )
                if curr_path.is_file():
                    abort(
                        400,
                        description=f"Unable to create folder in file {curr_path}. Please use the path for a folder.",
                    )
                new_path = Path(str_curr_path + escape(name))
                new_path.mkdir()
                return Response(
                    f"Directory {name}/ successfully created in {str_curr_path}.",
                    status=200,
                )
            except (FileExistsError, FileNotFoundError) as e:
                error = str(e)
                abort(400, description=f"Failed to create: {error}")
    else:
        abort(400)
