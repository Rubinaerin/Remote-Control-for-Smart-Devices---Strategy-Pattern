# ============================================================
# CONCRETE STRATEGY — AC (Air Conditioner)
# ============================================================
# Role in the Pattern: Concrete Strategy
#
# Implements the same interface as TV but with different behavior:
#   - increase_volume() → increases fan speed (not audio!)
#   - mute() → activates silent/night mode (not audio mute)
#   - Extra: temperature control (increase_temp / decrease_temp)
#
# This demonstrates the power of the Strategy Pattern:
# The same method name (increase_volume) performs a completely
# different operation depending on the concrete strategy in use.
# ============================================================

from strategy import DeviceStrategy

class AC(DeviceStrategy):
    """
    AC (Air Conditioner) class — Concrete Strategy

    RemoteControl sees this class as a DeviceStrategy.
    This means the remote never asks "is this a TV or AC?"
    It just says "control this". This is POLYMORPHISM.
    """

    def __init__(self, name: str = "Air Conditioner"):
        self.name = name
        self.is_on = False
        self.volume = 10      # Here volume = fan speed (%)
        self.is_muted = False # Here mute = silent/night mode
        self.temperature = 22 # Starting temperature (°C)
        self.mode = "Cool"    # Operating mode

    def turn_on(self) -> str:
        self.is_on = True
        return f"❄️ {self.name} turned ON"

    def turn_off(self) -> str:
        self.is_on = False
        return f"❄️ {self.name} turned OFF"

    def increase_volume(self) -> str:
        # In AC, "volume" = fan speed
        # Same method name, different meaning → Polymorphism example
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        if self.is_muted:
            # Fan speed cannot be changed in silent mode
            return f"❄️ {self.name} is in silent mode. Disable first."
        self.volume = min(100, self.volume + 10)
        return f"❄️ {self.name} fan speed increased to {self.volume}%"

    def decrease_volume(self) -> str:
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        if self.is_muted:
            return f"❄️ {self.name} is in silent mode. Disable first."
        self.volume = max(0, self.volume - 10)
        return f"❄️ {self.name} fan speed decreased to {self.volume}%"

    def mute(self) -> str:
        # BONUS FEATURE — For AC, mute = silent mode
        # Blocks fan noise for nighttime use
        # Carries a DIFFERENT meaning than TV/Speaker mute
        # but uses the SAME method name → Strategy Pattern advantage
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        self.is_muted = True
        return f"❄️ {self.name} is now in SILENT MODE 🔇"

    def unmute(self) -> str:
        # BONUS FEATURE — Disable silent mode
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        self.is_muted = False
        return f"❄️ {self.name} silent mode disabled 🔊"

    def increase_temp(self) -> str:
        # AC-specific extra feature — increase temperature
        # Maximum temperature capped at 30°C
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        self.temperature = min(30, self.temperature + 1)
        return f"❄️ {self.name} temperature set to {self.temperature}°C"

    def decrease_temp(self) -> str:
        # Minimum temperature capped at 16°C
        if not self.is_on:
            return f"❄️ {self.name} is OFF"
        self.temperature = max(16, self.temperature - 1)
        return f"❄️ {self.name} temperature set to {self.temperature}°C"

    def get_status(self) -> dict:
        return {
            "device": self.name,
            "type": "AC",
            "power": "ON" if self.is_on else "OFF",
            "fan_speed": f"{self.volume}%",  # Displayed as fan_speed for AC
            "silent_mode": self.is_muted,
            "temperature": f"{self.temperature}°C",
            "mode": self.mode
        }