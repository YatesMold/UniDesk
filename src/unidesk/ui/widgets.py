from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..helpers.text_data import load
from ..styles.loader import load_qss

UI = load("ui_strings")
FOOTER_LINKS = load("navigation")["footer_links"]


def qlabel(text, size=12, color="#cdd6f4", bold=False, wrap=False):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"background: transparent; border: none; color: {color}; "
        f"font-size: {size}px; font-weight: {'bold' if bold else 'normal'};"
    )
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def divider():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet(load_qss("widgets/divider.qss"))
    return line


def back_bar(title, on_back):
    bar = QWidget()
    bar.setFixedHeight(40)
    bar.setStyleSheet(load_qss("widgets/dark_bar.qss"))
    layout = QHBoxLayout(bar)
    layout.setContentsMargins(12, 0, 12, 0)

    btn = QPushButton(UI["back_button"])
    btn.setFixedWidth(70)
    btn.setStyleSheet(load_qss("widgets/back_button.qss"))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.clicked.connect(on_back)
    layout.addWidget(btn)

    lbl = QLabel(title)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet(load_qss("widgets/back_title.qss"))
    layout.addWidget(lbl, stretch=1)
    layout.addSpacing(70)
    return bar


def scroll_page(on_back, title):
    """Returns (outer_widget, content_layout) with back bar already added."""
    widget = QWidget()
    outer = QVBoxLayout(widget)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    outer.addWidget(back_bar(title, on_back))
    outer.addWidget(divider())

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setStyleSheet(load_qss("widgets/scroll_area.qss"))
    outer.addWidget(scroll)

    content = QWidget()
    content.setStyleSheet(load_qss("widgets/transparent.qss"))
    scroll.setWidget(content)

    cl = QVBoxLayout(content)
    cl.setContentsMargins(24, 20, 24, 20)
    cl.setSpacing(10)

    outer.addWidget(divider())
    outer.addWidget(footer())

    return widget, cl


def footer(on_configure=None):
    footer = QWidget()
    footer.setFixedHeight(40)
    footer.setStyleSheet(load_qss("widgets/dark_bar.qss"))
    ft = QHBoxLayout(footer)
    ft.setContentsMargins(14, 0, 14, 0)
    ft.addWidget(qlabel(UI["footer_copyright"], size=11, color="#585b70"))
    ft.addStretch()

    if on_configure is not None:
        cfg = QPushButton(UI["configure_button"])
        cfg.setStyleSheet(load_qss("widgets/footer_link.qss"))
        cfg.setCursor(Qt.CursorShape.PointingHandCursor)
        cfg.clicked.connect(lambda _: on_configure())
        ft.addWidget(cfg)

    for link in FOOTER_LINKS:
        b = QPushButton(link["label"])
        b.setStyleSheet(load_qss("widgets/footer_link.qss"))
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(lambda _, u=link["url"]: QDesktopServices.openUrl(QUrl(u)))
        ft.addWidget(b)
    return footer


class NavButton(QPushButton):
    def __init__(self, label):
        super().__init__(label)
        self.setFixedHeight(38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(load_qss("widgets/nav_button.qss"))
