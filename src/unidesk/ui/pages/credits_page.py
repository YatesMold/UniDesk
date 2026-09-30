from PyQt6.QtWidgets import QFrame, QVBoxLayout

from ...helpers.text_data import load
from ...styles.loader import load_qss
from ..widgets import qlabel, scroll_page

CREDITS = load("credits")["people"]
UI = load("ui_strings")


def build_credits_page(on_back):
    widget, cl = scroll_page(on_back, UI["credits_page_title"])

    for person in CREDITS:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(load_qss("pages/card_frame.qss"))
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(14, 10, 14, 10)
        fl.setSpacing(2)

        name = qlabel(person["name"], size=13, color="#cdd6f4", bold=True)
        name.setStyleSheet(
            name.styleSheet() + " background: transparent; border: none;"
        )
        fl.addWidget(name)

        role = qlabel(person["role"], size=11, color="#a6adc8")
        role.setStyleSheet(
            role.styleSheet() + " background: transparent; border: none;"
        )
        fl.addWidget(role)

        if person.get("projects"):
            proj = qlabel(
                UI["projects_prefix"] + ", ".join(person["projects"]),
                size=11,
                color="#8b5897",
            )
            proj.setStyleSheet(
                proj.styleSheet() + " background: transparent; border: none;"
            )
            fl.addWidget(proj)

        cl.addWidget(frame)

    cl.addStretch()
    return widget
