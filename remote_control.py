# ============================================================
# CONTEXT — RemoteControl
# ============================================================
# Role in the Pattern: Context
#
# In the Strategy Pattern, the Context class:
#   - Knows which strategy (device) to use
#   - Does NOT know the details of that strategy
#   - Strategy is changed at runtime via set_device()
#
# This class ONLY recognizes DeviceStrategy type.
# It does not care whether it is a TV, AC, or Speaker.
# This is the LOOSE COUPLING principle.
#
# Real-life analogy:
#   One physical remote controlling TV, AC, Speaker —
#   the remote stays the same, only the device changes.
# ============================================================

from strategy import DeviceStrategy

class RemoteControl:
    """
    CONTEXT class — The heart of the Strategy Pattern

    RemoteControl does not import any device class (TV, AC, Speaker).
    It only knows the abstract DeviceStrategy interface.

    When a new device is added, RemoteControl never changes!
    Only a new Concrete Strategy class is written.
    → Open/Closed Principle (OCP) in action
    """

    def __init__(self):
        # _device: The currently controlled device (none at start)
        # The _ prefix is a Python convention for "private" variable
        self._device: DeviceStrategy = None
        self._device_name: str = "None"

    def set_device(self, device: DeviceStrategy, name: str = ""):
        """
        SWITCH THE STRATEGY — This is the heart of the Strategy Pattern!

        Determines which device will be controlled at runtime.
        Switching from TV to AC requires only this method call.
        """
        self._device = device
        self._device_name = name or device.__class__.__name__
        return f"🎮 Remote switched to: {self._device_name}"

    def press_power_on(self) -> str:
        """Power ON button was pressed."""
        if not self._device:
            return "⚠️ No device connected to remote!"
        # We don't know if self._device is a TV or AC
        # We only know the turn_on method exists
        # Polymorphism takes over here
        return self._device.turn_on()

    def press_power_off(self) -> str:
        """Power OFF button was pressed."""
        if not self._device:
            return "⚠️ No device connected to remote!"
        return self._device.turn_off()

    def press_volume_up(self) -> str:
        """Volume/speed increase button was pressed."""
        if not self._device:
            return "⚠️ No device connected to remote!"
        # TV → volume increases
        # AC → fan speed increases
        # Speaker → volume increases
        # Same call, different behavior → Polymorphism!
        return self._device.increase_volume()

    def press_volume_down(self) -> str:
        """Volume/speed decrease button was pressed."""
        if not self._device:
            return "⚠️ No device connected to remote!"
        return self._device.decrease_volume()

    def press_mute(self) -> str:
        """
        BONUS FEATURE — Mute button

        TV → silent mode
        AC → silent/night mode
        Speaker → audio cut
        Each device applies its own mute behavior.
        The remote does not need to know this difference.
        """
        if not self._device:
            return "⚠️ No device connected to remote!"
        return self._device.mute()

    def press_unmute(self) -> str:
        """BONUS FEATURE — Unmute button"""
        if not self._device:
            return "⚠️ No device connected to remote!"
        return self._device.unmute()

    def show_status(self) -> dict:
        """Displays the current status of the connected device."""
        if not self._device:
            return {"error": "No device connected!"}
        return self._device.get_status()

    def get_current_device(self) -> str:
        """Returns the name of the currently controlled device."""
        return self._device_name if self._device else "None"