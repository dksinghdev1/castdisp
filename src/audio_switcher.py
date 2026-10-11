#!/usr/bin/env python3
import subprocess

def route_audio_to_hdmi():
    """Automatically scans for an active HDMI output sound profile and routes current streams to it."""
    print("[Audio Engine] Scanning PulseAudio/PipeWire hardware sound channels...")
    try:
        sinks_output = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode("utf-8")
        hdmi_sink = None
        for line in sinks_output.splitlines():
            if "hdmi" in line.lower() or "hdsp" in line.lower():
                hdmi_sink = line.split()[1]
                break
        
        if hdmi_sink:
            print(f"[Audio Engine] Activating HDMI sound destination target channel: {hdmi_sink}")
            subprocess.run(["pactl", "set-default-sink", hdmi_sink], check=False)
            inputs_output = subprocess.check_output(["pactl", "list", "short", "sink-inputs"]).decode("utf-8")
            for line in inputs_output.splitlines():
                if line:
                    stream_id = line.split()[0]
                    subprocess.run(["pactl", "move-sink-input", stream_id, hdmi_sink], check=False)
        else:
            print("[Audio Engine] Active external HDMI sound targets were not resolved.")
    except Exception as e:
        print(f"[Audio Engine] Command routing exception: {e}")