import os

from unidesk.helpers import autostart


def test_enabled_by_default():
    assert not autostart.is_autostart_disabled()


def test_disable_writes_hidden_override():
    autostart.set_autostart(False)
    assert os.path.exists(autostart.AUTOSTART_PATH)
    with open(autostart.AUTOSTART_PATH, encoding="utf-8") as f:
        content = f.read()
    assert "Hidden=true" in content
    assert "Exec=unidesk" in content
    assert autostart.is_autostart_disabled()


def test_enable_removes_override():
    autostart.set_autostart(False)
    autostart.set_autostart(True)
    assert not os.path.exists(autostart.AUTOSTART_PATH)
    assert not autostart.is_autostart_disabled()


def test_enable_without_override_is_noop():
    autostart.set_autostart(True)
    assert not os.path.exists(autostart.AUTOSTART_PATH)


def test_user_entry_without_hidden_counts_as_enabled():
    os.makedirs(os.path.dirname(autostart.AUTOSTART_PATH), exist_ok=True)
    with open(autostart.AUTOSTART_PATH, "w", encoding="utf-8") as f:
        f.write("[Desktop Entry]\nType=Application\nExec=unidesk\n")
    assert not autostart.is_autostart_disabled()
