# ============================================================
# MAIN — Demo & Test File
# ============================================================
# This file demonstrates how the Strategy Pattern works.
#
# Flow:
#   1. Device objects are created (TV, AC, Speaker)
#   2. A single RemoteControl object is created
#   3. set_device() connects the remote to different devices
#   4. The same remote methods are called on different devices
#
# This flow illustrates the core of the Strategy Pattern:
#   → Single interface, multiple behaviors
# ============================================================

import sys
import os

# Tell Python where the devices/ folder is located
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'devices'))

# Concrete Strategy classes (the actual devices)
from devices.tv import TV
from devices.ac import AC
from devices.speaker import Speaker

# Context class (the remote control)
from remote_control import RemoteControl

def print_separator(title=""):
    """Helper function that splits output into readable sections."""
    print("\n" + "="*50)
    if title:
        print(f"  {title}")
        print("="*50)

def demo():
    # -------------------------------------------------------
    # STEP 1: Create Concrete Strategy objects
    # Since each device inherits from DeviceStrategy,
    # RemoteControl can use all of them the same way
    # -------------------------------------------------------
    tv      = TV("Samsung Smart TV")
    ac      = AC("Daikin AC")
    speaker = Speaker("JBL Speaker")

    # -------------------------------------------------------
    # STEP 2: Create the Context (RemoteControl)
    # Not connected to any device at the start
    # -------------------------------------------------------
    remote = RemoteControl()

    print_separator("🎮 UNIVERSAL REMOTE CONTROL DEMO")

    # -------------------------------------------------------
    # TV DEMO
    # set_device() → sets the strategy to TV
    # All button presses now go to the TV
    # -------------------------------------------------------
    print_separator("📺 Controlling TV")
    print(remote.set_device(tv, "Samsung Smart TV"))  # Strategy: TV
    print(remote.press_power_on())      # TV turns on
    print(remote.press_volume_up())     # Volume: 20 → 25
    print(remote.press_volume_up())     # Volume: 25 → 30
    print(remote.press_mute())          # MUTE activated 🔇
    print(remote.press_volume_up())     # Blocked! (muted)
    print(remote.press_unmute())        # UNMUTE 🔊
    print(remote.press_volume_up())     # Volume: 30 → 35 (works now)
    print("Status:", remote.show_status())

    # -------------------------------------------------------
    # AC DEMO
    # set_device() → switch strategy to AC
    # Same remote, now controlling the air conditioner
    # -------------------------------------------------------
    print_separator("❄️ Controlling AC")
    print(remote.set_device(ac, "Daikin AC"))  # Strategy changed: AC
    print(remote.press_power_on())       # AC turns on
    print(remote.press_volume_up())      # Fan speed: 10 → 20%
    print(remote.press_mute())           # Silent mode activated 🔇
    print(remote.press_volume_up())      # Blocked! (silent mode)
    print(remote.press_unmute())         # Silent mode disabled 🔊
    print("Status:", remote.show_status())

    # -------------------------------------------------------
    # SPEAKER DEMO
    # set_device() → switch strategy to Speaker
    # -------------------------------------------------------
    print_separator("🔊 Controlling Speaker")
    print(remote.set_device(speaker, "JBL Speaker"))  # Strategy: Speaker
    print(remote.press_power_on())           # Speaker turns on
    print(speaker.play("Bohemian Rhapsody")) # Music starts 🎵
    print(remote.press_volume_up())          # Volume: 30 → 35
    print(remote.press_volume_up())          # Volume: 35 → 40
    print(remote.press_mute())               # MUTE 🔇
    print(remote.press_unmute())             # UNMUTE 🔊
    print(remote.press_power_off())          # Speaker turns off
    print("Status:", remote.show_status())

    print_separator("✅ Demo Complete — Strategy Pattern Works!")

# This function runs when the file is executed directly.
# If imported from another file, it will not run. (Safe usage)
if __name__ == "__main__":
    demo()