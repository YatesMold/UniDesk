"""Validate the bundled JSON so a bad edit fails CI instead of crashing at startup."""

import re
from importlib.resources import files
from pathlib import Path

import pytest

from unidesk.helpers import text_data

JSON_NAMES = sorted(
    p.name.removesuffix(".json")
    for p in files("unidesk.assets.text_data").iterdir()
    if p.name.endswith(".json")
)
SRC = Path(text_data.__file__).resolve().parents[1]


@pytest.mark.parametrize("name", JSON_NAMES)
def test_json_parses(name):
    assert text_data.load(name)


def test_every_nav_entry_has_a_page():
    ui = text_data.load("ui_strings")
    nav = text_data.load("navigation")
    known = set(text_data.pages()) | {ui["credits_page_title"], ui["links_page_title"]}
    missing = [k for k in nav["nav_left"] + nav["nav_right"] if k not in known]
    assert not missing, f"nav entries without a page: {missing}"


def test_pages_resolve_to_non_empty_bodies():
    for key, page in text_data.pages().items():
        assert page["body"].strip(), key


def test_faq_body_format():
    entries = text_data.load("faq")["entries"]
    body = text_data.faq_body()
    assert body.count("Q: ") == len(entries)
    assert body.count("A: ") == len(entries)


def test_ui_string_keys_used_in_code_exist():
    ui = text_data.load("ui_strings")
    used = set()
    for py in SRC.rglob("*.py"):
        used |= set(re.findall(r'UI\["([^"]+)"\]', py.read_text(encoding="utf-8")))
    missing = sorted(used - set(ui))
    assert not missing, f"ui_strings.json is missing: {missing}"


def test_saved_template_placeholders():
    tpl = text_data.load("ui_strings")["academic_saved_template"]
    assert tpl.format(university="U", department="D")


def _urls():
    nav = text_data.load("navigation")["footer_links"]
    links = text_data.load("links")["links"]
    return [(e["label"], e["url"]) for e in nav + links]


@pytest.mark.parametrize("label, url", _urls())
def test_links_are_https(label, url):
    assert label.strip()
    assert url.startswith("https://"), url


def test_credits_shape():
    for person in text_data.load("credits")["people"]:
        assert person["name"].strip()
        assert person["role"].strip()
        assert isinstance(person.get("projects", []), list)


def test_academic_institutions_shape():
    unis = text_data.load("academic_institutions")["universities"]
    assert unis
    for uni, departments in unis.items():
        assert uni.strip()
        assert departments, f"{uni} has no departments"
        assert len(departments) == len(set(departments)), f"duplicate dept in {uni}"
