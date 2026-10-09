import pytest
import os
from src.castdisp import is_wayland

def test_display_detection_paths():
    # Verify environment string outputs cleanly fallback to boolean states
    assert isinstance(is_wayland(), bool)