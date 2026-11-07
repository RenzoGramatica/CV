from pathlib import Path

from filesOrg import get_directories, get_node


def test_get_node():
    assert get_node(["a", "b"], {"a": {"b": 1}}) == 1


def test_get_directories():
    CONFIG_TEST = {
        "a": [1],
        "b": {"c": [2, 3], "d": [4, 5]},
        "e": {"f": [6, 7, 8], "g": [9, 10, 11], "h": [12, 13, 14]},
    }
    DIRECTORIES_TEST = {
        Path("a"): [1],
        Path("b"): None,
        Path("b", "c"): [2, 3],
        Path("b", "d"): [4, 5],
        Path("e"): None,
        Path("e", "f"): [6, 7, 8],
        Path("e", "g"): [9, 10, 11],
        Path("e", "h"): [12, 13, 14],
    }
    assert get_directories([], CONFIG_TEST) == DIRECTORIES_TEST


# .\.venv\Scripts\python.exe -m pytest -v
