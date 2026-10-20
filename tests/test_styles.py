import os
from importlib.resources import files

import pytest

from unidesk.styles import loader

QSS = sorted(
    f"widgets/{p.name}"
    for p in files("unidesk.styles").joinpath("widgets").iterdir()
    if p.name.endswith(".qss")
)


@pytest.mark.parametrize("name", QSS)
def test_qss_loads_with_tokens_resolved(name):
    qss = loader.load_qss(name)
    assert qss.strip()
    assert "__CHECK_SVG__" not in qss


def test_check_svg_resolves_to_real_file():
    assert os.path.isfile(loader.resolve_asset_path("check.svg"))
