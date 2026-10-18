"""Useful links page."""

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QPushButton

from ...helpers.text_data import load
from ...styles.loader import load_qss
from ..widgets import card, qlabel, scroll_page

LINKS = load("links")["links"]
UI = load("ui_strings")


def build_links_page(on_back):
    """Return the links page, with one card and Open button per link."""
    widget, cl = scroll_page(on_back, UI["links_page_title"])

    for link in LINKS:
        frame, fl = card(spacing=6)

        name = qlabel(link["label"], role="card-title")
        fl.addWidget(name)

        btn = QPushButton(UI["open_link_button"])
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("button", "link")
        btn.setStyleSheet(load_qss("widgets/controls.qss"))
        btn.clicked.connect(lambda _, u=link["url"]: QDesktopServices.openUrl(QUrl(u)))
        fl.addWidget(btn)

        cl.addWidget(frame)

    cl.addStretch()
    return widget
