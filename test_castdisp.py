import pytest
import os
from src import castdisp

def test_display_detection_paths():
    # Verify environment string outputs cleanly fallback to boolean states
    assert isinstance(castdisp.is_wayland(), bool)

def test_require_gtk_reports_install_command(monkeypatch):
    monkeypatch.setattr(castdisp, "Gtk", None)

    with pytest.raises(RuntimeError, match="sudo apt install python3-gi gir1.2-gtk-3.0"):
        castdisp.require_gtk()