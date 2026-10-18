"""Shared widget builders used by the main window and its pages."""

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


def qlabel(text, role="body", wrap=False):
    """Return a QLabel styled by its semantic role."""
    lbl = QLabel(text)
    lbl.setProperty("role", role)
    lbl.setStyleSheet(load_qss("widgets/labels.qss"))
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def divider():
    """Return a 1px horizontal separator line."""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setProperty("layout", "divider")
    line.setStyleSheet(load_qss("widgets/layout.qss"))
    return line


def back_bar(title, on_back):
    """Return the top bar of a subpage: a Back button and a centred title."""
    bar_widget = QWidget()
    bar_widget.setFixedHeight(40)
    bar_widget.setProperty("layout", "bar")
    bar_widget.setStyleSheet(load_qss("widgets/layout.qss"))
    layout = QHBoxLayout(bar_widget)
    layout.setContentsMargins(12, 0, 12, 0)

    btn = QPushButton(UI["back_button"])
    btn.setFixedWidth(70)
    btn.setProperty("button", "back")
    btn.setStyleSheet(load_qss("widgets/controls.qss"))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.clicked.connect(on_back)
    layout.addWidget(btn)

    lbl = qlabel(title, role="card-title")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(lbl, stretch=1)
    layout.addSpacing(70)
    return bar_widget


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
    scroll.setProperty("layout", "scroll")
    scroll.setStyleSheet(load_qss("widgets/layout.qss"))
    outer.addWidget(scroll)

    content = QWidget()
    content.setProperty("layout", "transparent")
    content.setStyleSheet(load_qss("widgets/layout.qss"))
    scroll.setWidget(content)

    cl = QVBoxLayout(content)
    cl.setContentsMargins(24, 20, 24, 20)
    cl.setSpacing(10)

    outer.addWidget(divider())
    outer.addWidget(footer())

    return widget, cl


def card(spacing):
    """Returns (frame, layout) for a bordered content card."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    frame.setProperty("layout", "card")
    frame.setStyleSheet(load_qss("widgets/layout.qss"))
    fl = QVBoxLayout(frame)
    fl.setContentsMargins(14, 10, 14, 10)
    fl.setSpacing(spacing)
    return frame, fl


def footer(on_configure=None):
    """Return the footer bar with the copyright notice and external links."""
    footer_widget = QWidget()
    footer_widget.setFixedHeight(40)
    footer_widget.setProperty("layout", "bar")
    footer_widget.setStyleSheet(load_qss("widgets/layout.qss"))
    ft = QHBoxLayout(footer_widget)
    ft.setContentsMargins(14, 0, 14, 0)
    ft.addWidget(qlabel(UI["footer_copyright"], role="footer"))
    ft.addStretch()

    if on_configure is not None:
        cfg = QPushButton(UI["configure_button"])
        cfg.setProperty("button", "footer-link")
        cfg.setStyleSheet(load_qss("widgets/controls.qss"))
        cfg.setCursor(Qt.CursorShape.PointingHandCursor)
        cfg.clicked.connect(lambda _: on_configure())
        ft.addWidget(cfg)

    for link in FOOTER_LINKS:
        b = QPushButton(link["label"])
        b.setProperty("button", "footer-link")
        b.setStyleSheet(load_qss("widgets/controls.qss"))
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(lambda _, u=link["url"]: QDesktopServices.openUrl(QUrl(u)))
        ft.addWidget(b)
    return footer_widget


class NavButton(QPushButton):
    """Large button on the main page that opens a subpage."""

    def __init__(self, label):
        super().__init__(label)
        self.setFixedHeight(38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setProperty("button", "nav")
        self.setStyleSheet(load_qss("widgets/controls.qss"))
