from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from ...helpers.text_data import load
from ..widgets import qlabel, scroll_page

LINKS = load("links")["links"]
UI = load("ui_strings")


def build_links_page(on_back):
    widget, cl = scroll_page(on_back, UI["links_page_title"])

    for link in LINKS:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            "QFrame { background-color: #2d1f3d; border: 1px solid #8b5897; border-radius: 5px; }"
        )
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(14, 10, 14, 10)
        fl.setSpacing(6)

        name = qlabel(link["label"], size=13, color="#cdd6f4", bold=True)
        name.setStyleSheet(
            name.styleSheet() + " background: transparent; border: none;"
        )
        fl.addWidget(name)

        btn = QPushButton(UI["open_link_button"])
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            "QPushButton { background-color: #89b4fa; color: #1e1e2e; font-weight: bold; "
            "border: none; border-radius: 4px; padding: 5px 10px; font-size: 11px; }"
            "QPushButton:hover { background-color: #b4befe; }"
        )
        btn.clicked.connect(lambda _, u=link["url"]: QDesktopServices.openUrl(QUrl(u)))
        fl.addWidget(btn)

        cl.addWidget(frame)

    cl.addStretch()
    return widget
