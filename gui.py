# ============================================================
# GUI.PY — Tkinter Graphical Interface
# ============================================================
# This file is the visual interface of the project.
# Uses the Strategy Pattern infrastructure (TV, AC, Speaker,
# RemoteControl) to provide a button-based remote simulation.
#
# Tkinter: Python's built-in GUI library
# No extra installation required!
#
# Design decisions:
#   - Dark theme → modern appearance
#   - Separate color per device (TV=blue, AC=cyan, Speaker=orange)
#   - Real-time status panel (device screen)
#   - Log area → records every button press
# ============================================================

import tkinter as tk
from tkinter import font as tkfont
import sys
import os

# Add devices/ folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'devices'))

from devices.tv import TV
from devices.ac import AC
from devices.speaker import Speaker
from remote_control import RemoteControl

# ============================================================
# COLOR PALETTE — Colors used throughout the interface
# ============================================================
COLORS = {
    "bg_dark":      "#0d0d0d",   # Main background (very dark)
    "bg_panel":     "#1a1a2e",   # Panel background (dark navy)
    "bg_card":      "#16213e",   # Card background
    "bg_display":   "#0f0f23",   # Screen/display background

    "tv_color":     "#4fc3f7",   # TV color (light blue)
    "ac_color":     "#80cbc4",   # AC color (mint/cyan)
    "spk_color":    "#ffb74d",   # Speaker color (orange)

    "btn_active":   "#1565c0",   # Active button color
    "btn_hover":    "#1976d2",   # Hover color
    "btn_danger":   "#c62828",   # Red button (power off)
    "btn_success":  "#2e7d32",   # Green button (power on)
    "btn_mute":     "#6a1b9a",   # Purple button (mute)
    "btn_unmute":   "#4a148c",   # Dark purple (unmute)
    "btn_neutral":  "#37474f",   # Gray button

    "text_white":   "#ffffff",
    "text_light":   "#e0e0e0",
    "text_dim":     "#9e9e9e",
    "text_green":   "#69f0ae",   # Green → ON status
    "text_red":     "#ff5252",   # Red → OFF status
    "text_yellow":  "#ffd740",   # Yellow → MUTED status

    "border":       "#263238",   # Border color
    "log_bg":       "#050510",   # Log area background
}

class RemoteControlApp:
    """
    Main application class.

    Creates all GUI components and connects them
    to the Strategy Pattern objects.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎮 Universal Remote Control — Strategy Pattern Demo")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)

        # Center the window on screen
        self._center_window(980, 700)

        # ── Strategy Pattern objects ─────────────────────────
        # Concrete Strategies (devices)
        self.tv      = TV("Samsung Smart TV")
        self.ac      = AC("Daikin AC")
        self.speaker = Speaker("JBL Speaker")

        # Context (remote control)
        self.remote  = RemoteControl()

        # Track the active device (for GUI purposes)
        self.active_device_name = tk.StringVar(value="None")
        self.devices = {
            "📺  TV":       self.tv,
            "❄️  AC":       self.ac,
            "🔊  Speaker":  self.speaker,
        }
        self.device_colors = {
            "📺  TV":       COLORS["tv_color"],
            "❄️  AC":       COLORS["ac_color"],
            "🔊  Speaker":  COLORS["spk_color"],
        }

        # Build the interface
        self._build_ui()

    def _center_window(self, w: int, h: int):
        """Places the window at the center of the screen."""
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ============================================================
    # UI BUILD — Main structure
    # ============================================================
    def _build_ui(self):
        """Creates all interface components."""

        # ── Header ──────────────────────────────────────────
        self._build_header()

        # ── Main content (left + right) ──────────────────────
        content = tk.Frame(self.root, bg=COLORS["bg_dark"])
        content.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Left panel: Device selector + Buttons
        left = tk.Frame(content, bg=COLORS["bg_dark"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Right panel: Status display + Log
        right = tk.Frame(content, bg=COLORS["bg_dark"])
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self._build_device_selector(left)
        self._build_control_buttons(left)
        self._build_status_panel(right)
        self._build_log_panel(right)

    def _build_header(self):
        """Top header area."""
        header = tk.Frame(self.root, bg=COLORS["bg_panel"], height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Left: Icon + title
        left_frame = tk.Frame(header, bg=COLORS["bg_panel"])
        left_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            left_frame,
            text="🎮  UNIVERSAL REMOTE CONTROL",
            font=("Courier New", 16, "bold"),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_white"]
        ).pack(side="left")

        # Right: Pattern label
        tk.Label(
            header,
            text="Strategy Pattern  •  Python OOP",
            font=("Courier New", 9),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_dim"]
        ).pack(side="right", padx=20)

        # Bottom border line
        tk.Frame(self.root, bg="#1565c0", height=2).pack(fill="x")

    # ============================================================
    # DEVICE SELECTOR
    # ============================================================
    def _build_device_selector(self, parent):
        """
        Device selection buttons.
        Simulates the set_device() call.
        Clicking each button = remote.set_device(device)
        """
        card = self._make_card(parent, "🔌  SELECT DEVICE")

        btn_frame = tk.Frame(card, bg=COLORS["bg_card"])
        btn_frame.pack(fill="x", pady=5)

        self.device_buttons = {}
        for i, (label, device) in enumerate(self.devices.items()):
            color = self.device_colors[label]
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Courier New", 11, "bold"),
                bg=COLORS["btn_neutral"],
                fg=COLORS["text_light"],
                activebackground=color,
                activeforeground=COLORS["bg_dark"],
                relief="flat",
                bd=0,
                padx=10,
                pady=8,
                cursor="hand2",
                command=lambda l=label, d=device: self._select_device(l, d)
            )
            btn.pack(side="left", expand=True, fill="x", padx=4)
            self.device_buttons[label] = btn

    def _select_device(self, label: str, device):
        """
        Device selection process.
        Strategy Pattern: set_device() call happens here.
        """
        result = self.remote.set_device(device, label.replace("📺  ", "")
                                                       .replace("❄️  ", "")
                                                       .replace("🔊  ", ""))
        self.active_device_name.set(label)

        # Update button colors to highlight the active device
        for lbl, btn in self.device_buttons.items():
            if lbl == label:
                btn.configure(bg=self.device_colors[lbl], fg=COLORS["bg_dark"])
            else:
                btn.configure(bg=COLORS["btn_neutral"], fg=COLORS["text_light"])

        self._log(result, "info")
        self._update_status()

    # ============================================================
    # CONTROL BUTTONS
    # ============================================================
    def _build_control_buttons(self, parent):
        """
        Remote control buttons.
        Each button = a method in RemoteControl
        """
        card = self._make_card(parent, "🕹️  REMOTE BUTTONS")

        # ── Power buttons ────────────────────────────────────
        power_row = tk.Frame(card, bg=COLORS["bg_card"])
        power_row.pack(fill="x", pady=(5, 3))

        self._make_button(power_row, "⏻  POWER ON",
                          COLORS["btn_success"], self._power_on).pack(
                          side="left", expand=True, fill="x", padx=(0, 3))

        self._make_button(power_row, "⏼  POWER OFF",
                          COLORS["btn_danger"], self._power_off).pack(
                          side="right", expand=True, fill="x", padx=(3, 0))

        # ── Volume buttons ───────────────────────────────────
        vol_row = tk.Frame(card, bg=COLORS["bg_card"])
        vol_row.pack(fill="x", pady=3)

        self._make_button(vol_row, "🔼  VOL UP",
                          COLORS["btn_active"], self._vol_up).pack(
                          side="left", expand=True, fill="x", padx=(0, 3))

        self._make_button(vol_row, "🔽  VOL DOWN",
                          COLORS["btn_active"], self._vol_down).pack(
                          side="right", expand=True, fill="x", padx=(3, 0))

        # ── Mute/Unmute buttons (BONUS FEATURE) ─────────────
        mute_row = tk.Frame(card, bg=COLORS["bg_card"])
        mute_row.pack(fill="x", pady=3)

        self._make_button(mute_row, "🔇  MUTE",
                          COLORS["btn_mute"], self._mute).pack(
                          side="left", expand=True, fill="x", padx=(0, 3))

        self._make_button(mute_row, "🔊  UNMUTE",
                          COLORS["btn_unmute"], self._unmute).pack(
                          side="right", expand=True, fill="x", padx=(3, 0))

        # ── Device-specific buttons ──────────────────────────
        special_label = tk.Label(
            card,
            text="— Device Specific Controls —",
            font=("Courier New", 8),
            bg=COLORS["bg_card"],
            fg=COLORS["text_dim"]
        )
        special_label.pack(pady=(8, 3))

        special_row = tk.Frame(card, bg=COLORS["bg_card"])
        special_row.pack(fill="x", pady=3)

        # CH+ / CH- → only meaningful on TV
        self._make_button(special_row, "📺 CH+",
                          COLORS["btn_neutral"], self._channel_up).pack(
                          side="left", expand=True, fill="x", padx=(0, 2))

        self._make_button(special_row, "📺 CH-",
                          COLORS["btn_neutral"], self._channel_down).pack(
                          side="left", expand=True, fill="x", padx=2)

        # TEMP+ / TEMP- → only meaningful on AC
        self._make_button(special_row, "❄️ TEMP+",
                          COLORS["btn_neutral"], self._temp_up).pack(
                          side="left", expand=True, fill="x", padx=2)

        self._make_button(special_row, "❄️ TEMP-",
                          COLORS["btn_neutral"], self._temp_down).pack(
                          side="right", expand=True, fill="x", padx=(2, 0))

        # PLAY → only meaningful on Speaker
        play_row = tk.Frame(card, bg=COLORS["bg_card"])
        play_row.pack(fill="x", pady=(3, 5))

        self._make_button(play_row, "🎵  PLAY — Bohemian Rhapsody",
                          COLORS["btn_neutral"], self._play_music).pack(
                          fill="x")

    # ============================================================
    # STATUS PANEL
    # ============================================================
    def _build_status_panel(self, parent):
        """
        Displays the device's current state.
        Visualizes the result of the get_status() method.
        """
        card = self._make_card(parent, "📊  DEVICE STATUS")

        # Frame for status rows
        self.status_frame = tk.Frame(card, bg=COLORS["bg_display"],
                                     padx=12, pady=10)
        self.status_frame.pack(fill="both", expand=True)

        # Initial placeholder message
        self.status_placeholder = tk.Label(
            self.status_frame,
            text="Select a device to view status...",
            font=("Courier New", 10),
            bg=COLORS["bg_display"],
            fg=COLORS["text_dim"]
        )
        self.status_placeholder.pack(expand=True)

        self.status_labels = {}

    def _update_status(self):
        """Refreshes the status panel."""
        # Clear old content
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        self.status_labels = {}

        status = self.remote.show_status()
        if "error" in status:
            tk.Label(self.status_frame,
                     text=status["error"],
                     font=("Courier New", 10),
                     bg=COLORS["bg_display"],
                     fg=COLORS["text_dim"]).pack(expand=True)
            return

        active = self.active_device_name.get()
        accent = self.device_colors.get(active, COLORS["text_white"])

        # Device name heading
        tk.Label(
            self.status_frame,
            text=status.get("device", "Unknown"),
            font=("Courier New", 13, "bold"),
            bg=COLORS["bg_display"],
            fg=accent
        ).pack(anchor="w", pady=(0, 8))

        # Create each status row
        for key, value in status.items():
            if key == "device":
                continue

            row = tk.Frame(self.status_frame, bg=COLORS["bg_display"])
            row.pack(fill="x", pady=2)

            # Key label
            tk.Label(
                row,
                text=f"{key.upper():15}",
                font=("Courier New", 9),
                bg=COLORS["bg_display"],
                fg=COLORS["text_dim"],
                width=15,
                anchor="w"
            ).pack(side="left")

            # Value label — color based on status
            val_str = str(value)
            if val_str == "ON":
                color = COLORS["text_green"]
            elif val_str == "OFF":
                color = COLORS["text_red"]
            elif val_str == "True":
                color = COLORS["text_yellow"]
            elif val_str == "False":
                color = COLORS["text_green"]
            else:
                color = COLORS["text_white"]

            lbl = tk.Label(
                row,
                text=val_str,
                font=("Courier New", 9, "bold"),
                bg=COLORS["bg_display"],
                fg=color,
                anchor="w"
            )
            lbl.pack(side="left")
            self.status_labels[key] = lbl

    # ============================================================
    # LOG PANEL
    # ============================================================
    def _build_log_panel(self, parent):
        """
        Records all operations in real time.
        Ideal for showing which method returned what during presentation.
        """
        card = self._make_card(parent, "📋  ACTION LOG")

        self.log_text = tk.Text(
            card,
            font=("Courier New", 9),
            bg=COLORS["log_bg"],
            fg=COLORS["text_light"],
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            state="disabled",
            height=10,
            wrap="word",
            cursor="arrow"
        )
        self.log_text.pack(fill="both", expand=True)

        # Color tags for different log types
        self.log_text.tag_configure("info",    foreground="#4fc3f7")
        self.log_text.tag_configure("success", foreground="#69f0ae")
        self.log_text.tag_configure("warning", foreground="#ffd740")
        self.log_text.tag_configure("error",   foreground="#ff5252")

        # Scrollbar
        scrollbar = tk.Scrollbar(card, command=self.log_text.yview,
                                 bg=COLORS["bg_card"])
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self._log("Remote Control ready. Select a device.", "info")

    def _log(self, message: str, tag: str = "success"):
        """Adds a new line to the log area."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"▶  {message}\n", tag)
        self.log_text.see("end")   # Auto-scroll to bottom
        self.log_text.configure(state="disabled")

    # ============================================================
    # HELPER METHODS
    # ============================================================
    def _make_card(self, parent, title: str) -> tk.Frame:
        """Creates a titled card component."""
        outer = tk.Frame(parent, bg=COLORS["bg_card"],
                         highlightbackground=COLORS["border"],
                         highlightthickness=1)
        outer.pack(fill="both", expand=True, pady=5)

        # Card title
        tk.Label(
            outer,
            text=title,
            font=("Courier New", 9, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_dim"],
            anchor="w",
            padx=12,
            pady=6
        ).pack(fill="x")

        # Thin divider line
        tk.Frame(outer, bg=COLORS["border"], height=1).pack(fill="x")

        # Content area
        inner = tk.Frame(outer, bg=COLORS["bg_card"], padx=12, pady=10)
        inner.pack(fill="both", expand=True)

        return inner

    def _make_button(self, parent, text: str, color: str,
                     command) -> tk.Button:
        """Creates a styled button."""
        btn = tk.Button(
            parent,
            text=text,
            font=("Courier New", 10, "bold"),
            bg=color,
            fg=COLORS["text_white"],
            activebackground=COLORS["btn_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            bd=0,
            padx=8,
            pady=9,
            cursor="hand2",
            command=command
        )
        # Hover effect
        btn.bind("<Enter>", lambda e, b=btn, c=color:
                 b.configure(bg=self._lighten(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=color:
                 b.configure(bg=c))
        return btn

    def _lighten(self, hex_color: str) -> str:
        """Lightens a color slightly (for hover effect)."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    def _get_tag(self, message: str) -> str:
        """Determines the log color based on message content."""
        msg_lower = message.lower()
        if "off" in msg_lower or "error" in msg_lower or "⚠" in msg_lower:
            return "error"
        if "muted" in msg_lower or "silent" in msg_lower:
            return "warning"
        return "success"

    # ============================================================
    # BUTTON COMMANDS — Connected to RemoteControl methods
    # ============================================================
    def _power_on(self):
        result = self.remote.press_power_on()
        self._log(result, self._get_tag(result))
        self._update_status()

    def _power_off(self):
        result = self.remote.press_power_off()
        self._log(result, "error")
        self._update_status()

    def _vol_up(self):
        result = self.remote.press_volume_up()
        self._log(result, self._get_tag(result))
        self._update_status()

    def _vol_down(self):
        result = self.remote.press_volume_down()
        self._log(result, self._get_tag(result))
        self._update_status()

    def _mute(self):
        # BONUS FEATURE: Mute button
        result = self.remote.press_mute()
        self._log(result, "warning")
        self._update_status()

    def _unmute(self):
        # BONUS FEATURE: Unmute button
        result = self.remote.press_unmute()
        self._log(result, "success")
        self._update_status()

    def _channel_up(self):
        # TV-specific — prevented for other devices with AttributeError guard
        device = self.remote._device
        if hasattr(device, 'channel_up'):
            result = device.channel_up()
        else:
            result = "⚠️  CH+ only works on TV"
        self._log(result, self._get_tag(result))
        self._update_status()

    def _channel_down(self):
        device = self.remote._device
        if hasattr(device, 'channel_down'):
            result = device.channel_down()
        else:
            result = "⚠️  CH- only works on TV"
        self._log(result, self._get_tag(result))
        self._update_status()

    def _temp_up(self):
        # AC-specific — increase temperature
        device = self.remote._device
        if hasattr(device, 'increase_temp'):
            result = device.increase_temp()
        else:
            result = "⚠️  TEMP+ only works on AC"
        self._log(result, self._get_tag(result))
        self._update_status()

    def _temp_down(self):
        device = self.remote._device
        if hasattr(device, 'decrease_temp'):
            result = device.decrease_temp()
        else:
            result = "⚠️  TEMP- only works on AC"
        self._log(result, self._get_tag(result))
        self._update_status()

    def _play_music(self):
        # Speaker-specific — play music
        device = self.remote._device
        if hasattr(device, 'play'):
            result = device.play("Bohemian Rhapsody — Queen")
        else:
            result = "⚠️  PLAY only works on Speaker"
        self._log(result, self._get_tag(result))
        self._update_status()


# ============================================================
# LAUNCH THE APPLICATION
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()

    # Application icon (if available)
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass

    app = RemoteControlApp(root)

    # Clean exit when window is closed
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Start the main loop (Tkinter event loop)
    root.mainloop()