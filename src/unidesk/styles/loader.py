"""Loads UniDesk's Qt stylesheets from the bundled .qss files."""

from functools import cache
from importlib.resources import files


@cache
def load_qss(filename):
    """Return the raw contents of <filename> from the styles package."""
    return files("unidesk.styles").joinpath(filename).read_text(encoding="utf-8")
