#!/usr/bin/env python3
import os
import sys
import argparse
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
from audio_switcher import route_audio_to_hdmi

class CastDispApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="CastDisp Switcher")
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(15)
        self.set_default_size(500, 100)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.1, 0.1, 0.1, 0.95))
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        title = Gtk.Label()
        title.set_markup("<span foreground='white' size='large'><b>CastDisp | Choose Display Mode</b></span>")
        vbox.pack_start(title, False, False, 0)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.pack_start(hbox, True, True, 0)
        
        for mode in ["Internal Only", "Mirror", "Extend", "External Only"]:
            btn = Gtk.Button(label=mode)
            btn.connect("clicked", self.on_mode_selected, mode.lower())
            hbox.pack_start(btn, True, True, 0)
            
        dismiss = Gtk.Button(label="Dismiss")
        dismiss.connect("clicked", lambda w: Gtk.main_quit())
        vbox.pack_start(dismiss, False, False, 0)
        
    def on_mode_selected(self, widget, mode):
        apply_display_topology(mode)
        Gtk.main_quit()

def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE") == "wayland"

def apply_display_topology(mode):
    if is_wayland():
        print(f"[Wayland Target] Changing topology over DBus interface: {mode}")
        if mode in ["mirror", "extend", "external"]:
            route_audio_to_hdmi()
    else:
        print(f"[X11 Target] Executing xrandr pipeline: {mode}")
        if mode == "extend":
            os.system("xrandr --auto")
            route_audio_to_hdmi()

def main():
    parser = argparse.ArgumentParser(description="CastDisp Framework Daemon CLI")
    parser.add_argument('--mode', choices=['internal', 'mirror', 'extend', 'external'])
    args = parser.parse_args()
    if args.mode:
        apply_display_topology(args.mode)
    else:
        win = CastDispApp()
        win.show_all()
        Gtk.main_run()

if __name__ == "__main__":
    main()