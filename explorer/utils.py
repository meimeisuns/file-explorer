from pathlib import Path


def get_basic_attr(path: Path):
    return {
        "name": f"{path.name}/" if path.is_dir() else path.name,
        "owner": path.owner(),
        "size_bytes": path.stat().st_size,
        "permissions": path.stat().st_mode,
    }


def list_dir(path: Path):
    listing = []
    for entry in path.iterdir():
        listing.append(get_basic_attr(entry))
    return listing


def get_file_contents(file: Path):
    attrs = get_basic_attr(file)
    attrs["text"] = file.read_text()
    return attrs
