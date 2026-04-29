# ============================================================
# STRATEGY PATTERN — ABSTRACT BASE CLASS
# ============================================================
# What is the Strategy Pattern?
# When there are multiple ways to perform an operation,
# we encapsulate each way in a separate class.
# We decide which one to use at runtime.
#
# In this project: TV, AC, and Speaker are different devices
# but all can be controlled by the same remote control.
# This is possible because all of them sign the same
# "contract" (interface) defined here.
# ============================================================

from abc import ABC, abstractmethod
# ABC = Abstract Base Class
# abstractmethod = Methods that MUST be implemented by subclasses

class DeviceStrategy(ABC):
    """
    STRATEGY INTERFACE

    This class is a template / contract.
    All devices (TV, AC, Speaker) inherit from this class.
    Each device re-implements (overrides) these methods
    in its own specific way.

    Why use an abstract class?
    → RemoteControl only knows this class, not TV/AC/Speaker.
    → To add a new device, just subclass this class.
    → This follows the OCP (Open/Closed Principle):
      "Open for extension, closed for modification."
    """

    @abstractmethod
    def turn_on(self) -> str:
        # Turns the device on — each device implements this differently
        pass

    @abstractmethod
    def turn_off(self) -> str:
        # Turns the device off
        pass

    @abstractmethod
    def increase_volume(self) -> str:
        # Increases volume/speed (TV→volume, AC→fan speed, Speaker→volume)
        pass

    @abstractmethod
    def decrease_volume(self) -> str:
        # Decreases volume/speed
        pass

    @abstractmethod
    def mute(self) -> str:
        # BONUS FEATURE: Silences the device
        # TV/Speaker → mute audio
        # AC → silent (night) mode
        pass

    @abstractmethod
    def unmute(self) -> str:
        # BONUS FEATURE: Removes the silence/mute
        pass

    @abstractmethod
    def get_status(self) -> dict:
        # Returns the current state of the device as a dictionary
        # (on/off, volume level, mute status, etc.)
        pass