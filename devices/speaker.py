# ============================================================
# CONCRETE STRATEGY — Speaker (Smart Speaker)
# ============================================================
# Role in the Pattern: Concrete Strategy
#
# The most "audio-focused" of the three devices.
# Mute/Unmute carries its most natural meaning here.
# Extra feature: music playback (play method)
#
# Important Note:
# TV, AC, and Speaker are COMPLETELY INDEPENDENT classes.
# But RemoteControl controls all of them the same way.
# This is possible because all inherit from DeviceStrategy.
# ============================================================

from strategy import DeviceStrategy

class Speaker(DeviceStrategy):
    """
    Speaker class — Concrete Strategy

    Has a music playback feature that distinguishes it
    from other devices. Mute here is true audio silencing.
    """

    def __init__(self, name: str = "Smart Speaker"):
        self.name = name
        self.is_on = False
        self.volume = 30               # Starting volume level
        self.is_muted = False          # Mute status
        self.track = "No track playing"  # Currently playing track
        self.bass = 50                 # Bass level (0-100)

    def turn_on(self) -> str:
        self.is_on = True
        return f"🔊 {self.name} turned ON"

    def turn_off(self) -> str:
        self.is_on = False
        return f"🔊 {self.name} turned OFF"

    def increase_volume(self) -> str:
        # Mute check: volume cannot be increased while muted
        # This ensures a consistent user experience
        if not self.is_on:
            return f"🔊 {self.name} is OFF"
        if self.is_muted:
            return f"🔊 {self.name} is muted. Unmute first."
        self.volume = min(100, self.volume + 5)
        return f"🔊 {self.name} volume increased to {self.volume}"

    def decrease_volume(self) -> str:
        if not self.is_on:
            return f"🔊 {self.name} is OFF"
        if self.is_muted:
            return f"🔊 {self.name} is muted. Unmute first."
        self.volume = max(0, self.volume - 5)
        return f"🔊 {self.name} volume decreased to {self.volume}"

    def mute(self) -> str:
        # BONUS FEATURE — Mute
        # Classic mute usage for a speaker
        # Example scenario: quickly silence when phone rings
        if not self.is_on:
            return f"🔊 {self.name} is OFF"
        self.is_muted = True
        return f"🔊 {self.name} is now MUTED 🔇"

    def unmute(self) -> str:
        # BONUS FEATURE — Unmute
        # Resume music after the phone call ends
        if not self.is_on:
            return f"🔊 {self.name} is OFF"
        self.is_muted = False
        return f"🔊 {self.name} is now UNMUTED 🔊"

    def play(self, track: str = "Unknown Track") -> str:
        # Speaker-specific extra feature
        # Not defined in the Strategy interface
        # Can only be called directly on Speaker objects
        if not self.is_on:
            return f"🔊 {self.name} is OFF"
        self.track = track
        return f"🔊 {self.name} now playing: {track} 🎵"

    def get_status(self) -> dict:
        return {
            "device": self.name,
            "type": "Speaker",
            "power": "ON" if self.is_on else "OFF",
            "volume": self.volume,
            "muted": self.is_muted,
            "track": self.track,
            "bass": self.bass
        }