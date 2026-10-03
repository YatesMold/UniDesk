"""Loads UniDesk's Qt stylesheets and assets from the styles package."""

import atexit
from contextlib import ExitStack
from functools import cache
from importlib.resources import as_file, files

# Keeps extracted asset files alive for the whole process (needed when the
# package is imported from a zipped wheel); cleaned up on interpreter exit.
_asset_stack = ExitStack()
atexit.register(_asset_stack.close)


@cache
def load_qss(filename):
    """Return the raw contents of <filename> from the styles package."""
    return files("unidesk.styles").joinpath(filename).read_text(encoding="utf-8")


@cache
def resolve_asset_path(filename):
    """Return a real filesystem path for <filename> from the styles package."""
    return _asset_stack.enter_context(
        as_file(files("unidesk.styles").joinpath(filename))
    )
