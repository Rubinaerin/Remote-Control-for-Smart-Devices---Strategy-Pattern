# ============================================================
# CONCRETE STRATEGY — TV (Television)
# ============================================================
# Role in the Pattern: Concrete Strategy
#
# Inherits from DeviceStrategy and implements all abstract
# methods with TV-specific behavior.
#
# TV-specific extra features:
#   - Channel switching (channel_up / channel_down)
#   - Volume control is blocked while muted
# ============================================================

from strategy import DeviceStrategy

class TV(DeviceStrategy):
    """
    TV class — Concrete Strategy

    Inherits from DeviceStrategy, meaning RemoteControl
    does not directly recognize this class; it only knows
    it as a DeviceStrategy type.
    This gives us Loosely Coupled architecture.
    """

    def __init__(self, name: str = "Smart TV"):
        # __init__: Runs when the object is first created
        self.name = name          # Device name (e.g., "Samsung Smart TV")
        self.is_on = False        # Off by default
        self.volume = 20          # Starting volume level (0-100)
        self.is_muted = False     # Not muted by default
        self.channel = 1          # Starting channel

    def turn_on(self) -> str:
        # Turns the device on and updates state
        self.is_on = True
        return f"📺 {self.name} turned ON"

    def turn_off(self) -> str:
        # Turns the device off
        self.is_on = False
        return f"📺 {self.name} turned OFF"

    def increase_volume(self) -> str:
        # Guard Clause:
        # If the device is off or muted, no action is taken
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        if self.is_muted:
            return f"📺 {self.name} is muted. Unmute first."
        # min(100, ...) → volume never exceeds 100
        self.volume = min(100, self.volume + 5)
        return f"📺 {self.name} volume increased to {self.volume}"

    def decrease_volume(self) -> str:
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        if self.is_muted:
            return f"📺 {self.name} is muted. Unmute first."
        # max(0, ...) → volume never goes below 0
        self.volume = max(0, self.volume - 5)
        return f"📺 {self.name} volume decreased to {self.volume}"

    def mute(self) -> str:
        # BONUS FEATURE — Mute
        # Sets is_muted flag to True
        # This flag blocks volume increase/decrease operations
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        self.is_muted = True
        return f"📺 {self.name} is now MUTED 🔇"

    def unmute(self) -> str:
        # BONUS FEATURE — Unmute
        # Sets is_muted flag to False, re-enables volume control
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        self.is_muted = False
        return f"📺 {self.name} is now UNMUTED 🔊"

    def channel_up(self) -> str:
        # TV-specific extra feature — not in Strategy interface
        # Only available on TV objects
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        self.channel += 1
        return f"📺 {self.name} channel changed to {self.channel}"

    def channel_down(self) -> str:
        if not self.is_on:
            return f"📺 {self.name} is OFF"
        # max(1, ...) → channel never drops below 1
        self.channel = max(1, self.channel - 1)
        return f"📺 {self.name} channel changed to {self.channel}"

    def get_status(self) -> dict:
        # Returns the device's current state as a dictionary
        # RemoteControl or GUI can use this to display information
        return {
            "device": self.name,
            "type": "TV",
            "power": "ON" if self.is_on else "OFF",
            "volume": self.volume,
            "muted": self.is_muted,
            "channel": self.channel
        }