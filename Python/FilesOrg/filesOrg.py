import json
import shutil
from pathlib import Path


def read_config() -> dict:
    config_text = Path("config.json").read_text(encoding="utf-8")
    return json.loads(config_text)


def get_node(keys, tree) -> dict | list:
    new_tree = tree
    if isinstance(keys, list):
        for i in keys:
            new_tree = new_tree[i]
    return new_tree


def get_keys(directories) -> dict:
    keys = {}
    for directory in directories:
        if directories[directory] is None:
            continue
        for extension in directories[directory]:
            keys[extension] = directory
    return keys


def get_directories(keys_path, tree) -> dict:
    new_tree = get_node(keys_path, tree)
    extensions_by_path = {}
    for nodes in new_tree:
        new_keys_path = keys_path + [nodes]
        path = Path(*new_keys_path)
        if isinstance(new_tree[nodes], list):
            extensions_by_path[path] = new_tree[nodes]
        elif isinstance(new_tree[nodes], dict):
            extensions_by_path[path] = None
            extensions_by_path.update(get_directories(new_keys_path, tree))
    return extensions_by_path


def make_directories(directories, location) -> None:
    for directory in list(directories):
        Path(location, directory).mkdir(parents=True, exist_ok=True)


def move_directories(directories, location) -> None:
    extensions = get_keys(directories)
    items = list(Path(location).iterdir())
    for item in items:
        if item.is_dir():
            continue
        suffix = item.suffix.lower()
        if suffix in extensions:
            shutil.move(item, Path(location, extensions[suffix]))
            continue
        for directory in list(directories):
            if directories[directory] == []:
                shutil.move(item, Path(location, directory))


def copy_files(location) -> None:
    items = list(Path(location).iterdir())
    for item in items:
        if item.is_dir():
            continue
        shutil.copy(item, location / "CopySecurity")


def update(config) -> None:
    TREE_ABSOLUTE = config["Extension"]
    LOCATION = config["Path-Directory"]
    COPY_SECURITY = config["Copy-Security"]
    if COPY_SECURITY:
        Path(LOCATION, "CopySecurity").mkdir(parents=True, exist_ok=True)
        copy_files(Path(LOCATION))
    directories = get_directories([], TREE_ABSOLUTE)
    make_directories(directories, LOCATION)
    move_directories(directories, LOCATION)


if __name__ == "__main__":
    update(read_config())

# Comandos para ruff
#   ruff check --fix .
#   ruff format .
#   ruff check --fix . & ruff format .
