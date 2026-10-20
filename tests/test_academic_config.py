import json

import pytest

from unidesk.helpers import academic_config as ac

EMPTY = {"universityName": "", "departmentName": ""}


def _write(raw):
    import os

    os.makedirs(ac.CONFIG_DIR, exist_ok=True)
    with open(ac.CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(raw)


def test_missing_file_returns_empty():
    assert ac.load_academic_config() == EMPTY


def test_save_then_load_roundtrip():
    ac.save_academic_config("University of Macedonia", "Applied Informatics")
    assert ac.load_academic_config() == {
        "universityName": "University of Macedonia",
        "departmentName": "Applied Informatics",
    }


def test_save_creates_dir_and_uses_shared_key_names():
    # UniBackpack reads this file: key names are a cross-app contract.
    ac.save_academic_config("U", "D")
    with open(ac.CONFIG_PATH, encoding="utf-8") as f:
        data = json.load(f)
    assert set(data) == {"universityName", "departmentName"}


def test_save_keeps_greek_text():
    ac.save_academic_config("Πανεπιστήμιο Μακεδονίας", "Εφαρμοσμένη Πληροφορική")
    assert ac.load_academic_config()["universityName"] == "Πανεπιστήμιο Μακεδονίας"


@pytest.mark.parametrize(
    "raw",
    ["", "{not json", "[]", '"string"', "42", "null"],
    ids=["empty", "corrupt", "list", "string", "number", "null"],
)
def test_bad_content_returns_empty(raw):
    _write(raw)
    assert ac.load_academic_config() == EMPTY


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"universityName": "U"}, {"universityName": "U", "departmentName": ""}),
        ({"universityName": None, "departmentName": "D"},
         {"universityName": "", "departmentName": "D"}),
        ({"universityName": "U", "departmentName": "D", "extra": 1},
         {"universityName": "U", "departmentName": "D"}),
    ],
    ids=["partial", "null-value", "extra-key"],
)
def test_partial_or_noisy_content(data, expected):
    _write(json.dumps(data))
    assert ac.load_academic_config() == expected
