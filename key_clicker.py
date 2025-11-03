#!/usr/bin/env python3
"""
Modern Auto Key Clicker
A sleek Python-based auto key clicker with modern GUI and system tray support.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import sys
import platform
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import queue


class ModernKeyClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Key Clicker")
        self.root.geometry("550x750")
        self.root.resizable(True, True)
        self.root.minsize(500, 700)
        
        # Dark mode color scheme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.secondary_bg = "#2d2d2d"
        self.button_hover = "#3d3d3d"
        self.success_color = "#28a745"
        self.danger_color = "#dc3545"
        
        # Apply dark theme
        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Dark.TFrame', background=self.bg_color)
        style.configure('Dark.TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('Dark.TButton', background=self.secondary_bg, foreground=self.fg_color)
        style.map('Dark.TButton',
                  background=[('active', self.button_hover), ('pressed', self.accent_color)])
        
        # Configure Combobox styling (limited on Windows)
        try:
            style.configure('TCombobox',
                            fieldbackground=self.secondary_bg,
                            background=self.secondary_bg,
                            foreground=self.fg_color)
        except:
            pass
        
        # State variables
        self.is_running = False
        self.click_thread = None
        self.stop_event = threading.Event()
        self.press_count = 0
        self.keyboard_controller = Controller()
        self.hotkey_listener = None
        self.hotkey_key = Key.f6
        self.show_tray_notification = True  # Flag to show notification on first close
        
        # Special keys mapping
        self.special_keys = {
            'enter': Key.enter,
            'space': Key.space,
            'tab': Key.tab,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'esc': Key.esc,
            'shift': Key.shift,
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'f1': Key.f1,
            'f2': Key.f2,
            'f3': Key.f3,
            'f4': Key.f4,
            'f5': Key.f5,
            'f6': Key.f6,
            'f7': Key.f7,
            'f8': Key.f8,
            'f9': Key.f9,
            'f10': Key.f10,
            'f11': Key.f11,
            'f12': Key.f12,
        }
        
        # Hotkey options
        self.hotkey_options = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # Create GUI
        self.create_gui()
        
        # Start hotkey listener
        self.setup_hotkey_listener()
        
        # Create system tray
        self.setup_system_tray()
        
        # Check for messages from other threads
        self.root.after(100, self.check_queue)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_gui(self):
        """Create the modern GUI interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Auto Key Clicker",
            font=font.Font(family="Segoe UI", size=22, weight="bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(15, 5))
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Key selection section
        key_frame = self.create_section(main_container, "Key Selection")
        
        self.key_mode = tk.StringVar(value="regular")
        
        key_mode_frame = tk.Frame(key_frame, bg=self.secondary_bg, relief=tk.FLAT)
        key_mode_frame.pack(fill=tk.X, pady=(0, 12))
        
        regular_radio = tk.Radiobutton(
            key_mode_frame,
            text="Regular Key",
            variable=self.key_mode,
            value="regular",
            bg=self.secondary_bg,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.secondary_bg,
            activeforeground=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            command=self.on_key_mode_change
        )
        regular_radio.pack(side=tk.LEFT, padx=20, pady=12)
        
        special_radio = tk.Radiobutton(
            key_mode_frame,
            text="Special Key",
            variable=self.key_mode,
            value="special",
            bg=self.secondary_bg,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.secondary_bg,
            activeforeground=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            command=self.on_key_mode_change
        )
        special_radio.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Regular key input
        self.regular_key_frame = tk.Frame(key_frame, bg=self.secondary_bg)
        self.regular_key_frame.pack(fill=tk.X, pady=(0, 12))
        
        regular_label = tk.Label(
            self.regular_key_frame,
            text="Key:",
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            width=12,
            anchor="w"
        )
        regular_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.regular_key_entry = tk.Entry(
            self.regular_key_frame,
            bg=self.secondary_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=font.Font(family="Segoe UI", size=11),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.secondary_bg,
            highlightcolor=self.accent_color,
            width=15,
            borderwidth=0
        )
        self.regular_key_entry.pack(side=tk.LEFT, padx=(0, 15), pady=12)
        self.regular_key_entry.insert(0, "a")
        
        # Special key dropdown
        self.special_key_frame = tk.Frame(key_frame, bg=self.secondary_bg)
        
        special_label = tk.Label(
            self.special_key_frame,
            text="Special Key:",
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            width=12,
            anchor="w"
        )
        special_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.special_key_var = tk.StringVar(value="enter")
        special_key_dropdown = self.create_dropdown(
            self.special_key_frame,
            self.special_key_var,
            list(self.special_keys.keys()),
            width=18
        )
        special_key_dropdown.pack(side=tk.LEFT, padx=(0, 15), pady=12)
        
        # Interval section
        interval_frame = self.create_section(main_container, "Timing Settings")
        
        interval_inner = tk.Frame(interval_frame, bg=self.secondary_bg)
        interval_inner.pack(fill=tk.X, pady=(0, 12))
        
        interval_label = tk.Label(
            interval_inner,
            text="Interval (seconds):",
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            width=18,
            anchor="w"
        )
        interval_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.interval_entry = tk.Entry(
            interval_inner,
            bg=self.secondary_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=font.Font(family="Segoe UI", size=11),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.secondary_bg,
            highlightcolor=self.accent_color,
            width=15,
            borderwidth=0
        )
        self.interval_entry.pack(side=tk.LEFT, padx=(0, 15), pady=12)
        self.interval_entry.insert(0, "1.0")
        
        # Hotkey section
        hotkey_inner = tk.Frame(interval_frame, bg=self.secondary_bg)
        hotkey_inner.pack(fill=tk.X, pady=(0, 12))
        
        hotkey_label = tk.Label(
            hotkey_inner,
            text="Toggle Hotkey:",
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            width=18,
            anchor="w"
        )
        hotkey_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.hotkey_var = tk.StringVar(value="F6")
        hotkey_dropdown = self.create_dropdown(
            hotkey_inner,
            self.hotkey_var,
            self.hotkey_options,
            width=18,
            callback=lambda v: self.on_hotkey_change()
        )
        hotkey_dropdown.pack(side=tk.LEFT, padx=(0, 15), pady=12)
        
        # Press limit section
        limit_inner = tk.Frame(interval_frame, bg=self.secondary_bg)
        limit_inner.pack(fill=tk.X)
        
        limit_label = tk.Label(
            limit_inner,
            text="Press Limit (0=∞):",
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            width=18,
            anchor="w"
        )
        limit_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.limit_entry = tk.Entry(
            limit_inner,
            bg=self.secondary_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=font.Font(family="Segoe UI", size=11),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.secondary_bg,
            highlightcolor=self.accent_color,
            width=15,
            borderwidth=0
        )
        self.limit_entry.pack(side=tk.LEFT, padx=(0, 15), pady=12)
        self.limit_entry.insert(0, "0")
        
        # Counter section
        counter_frame = self.create_section(main_container, "Press Counter")
        
        counter_inner = tk.Frame(counter_frame, bg=self.secondary_bg)
        counter_inner.pack(fill=tk.X)
        
        self.counter_label = tk.Label(
            counter_inner,
            text="0",
            bg=self.secondary_bg,
            fg=self.accent_color,
            font=font.Font(family="Segoe UI", size=28, weight="bold"),
            width=10
        )
        self.counter_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        reset_btn = self.create_modern_button(
            counter_inner,
            "Reset",
            self.reset_counter,
            bg_color=self.danger_color,
            hover_color="#c82333"
        )
        reset_btn.pack(side=tk.RIGHT, padx=15, pady=12)
        
        # Control buttons
        control_frame = tk.Frame(main_container, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(15, 10))
        
        self.start_btn = self.create_modern_button(
            control_frame,
            "▶ Start",
            self.toggle_clicking,
            bg_color=self.success_color,
            hover_color="#218838",
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = self.create_modern_button(
            control_frame,
            "■ Stop",
            self.toggle_clicking,
            bg_color=self.danger_color,
            hover_color="#c82333",
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.stop_btn.config(state=tk.DISABLED)
        
        status_btn = self.create_modern_button(
            control_frame,
            "ℹ Info",
            self.show_info,
            bg_color=self.accent_color,
            hover_color="#005a9e",
            width=15
        )
        status_btn.pack(side=tk.LEFT)
        
        # Initial key mode
        self.on_key_mode_change()
    
    def create_section(self, parent, title):
        """Create a section with title"""
        section = tk.Frame(parent, bg=self.bg_color)
        section.pack(fill=tk.X, pady=(0, 12))
        
        title_label = tk.Label(
            section,
            text=title,
            bg=self.bg_color,
            fg="#888888",
            font=font.Font(family="Segoe UI", size=9, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill=tk.X, pady=(0, 6))
        
        return section
    
    def create_modern_button(self, parent, text, command, bg_color=None, hover_color=None, width=None):
        """Create a modern styled button"""
        if bg_color is None:
            bg_color = self.accent_color
        if hover_color is None:
            hover_color = "#005a9e"
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10, weight="bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=width,
            pady=10
        )
        
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_dropdown(self, parent, variable, values, width=18, callback=None):
        """Create a custom dropdown with dark theme"""
        # Create frame to hold the menubutton and arrow
        dropdown_frame = tk.Frame(parent, bg=self.secondary_bg)
        
        # Create the menubutton
        mb = tk.Menubutton(
            dropdown_frame,
            textvariable=variable,
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.secondary_bg,
            highlightcolor=self.accent_color,
            width=width,
            anchor="w",
            cursor="hand2"
        )
        
        # Create the menu
        menu = tk.Menu(
            mb,
            tearoff=0,
            bg=self.secondary_bg,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            bd=0,
            activebackground=self.button_hover,
            activeforeground=self.fg_color,
            font=font.Font(family="Segoe UI", size=10)
        )
        
        # Add values to menu
        for value in values:
            menu.add_radiobutton(
                label=value,
                variable=variable,
                command=lambda v=value: (variable.set(v), callback(v) if callback else None)
            )
        
        mb.config(menu=menu)
        mb.pack(side=tk.LEFT)
        
        # Configure Windows menu colors
        if platform.system() == "Windows":
            try:
                # Set dark mode for the menu
                self._configure_windows_menu_colors(mb, menu)
            except:
                pass
        
        return dropdown_frame
    
    def _configure_windows_menu_colors(self, menubutton, menu):
        """Configure Windows menu to use dark theme"""
        try:
            # Try to use dark mode API for Windows 10/11
            import ctypes
            ctypes.windll.uxtheme.SetWindowTheme(menubutton.winfo_id(), "DarkMode_Explorer", None)
        except:
            # Menu colors are configured via Menu widget settings above
            pass
    
    def on_key_mode_change(self):
        """Handle key mode change"""
        if self.key_mode.get() == "regular":
            self.regular_key_frame.pack(fill=tk.X, pady=(0, 15))
            self.special_key_frame.pack_forget()
        else:
            self.special_key_frame.pack(fill=tk.X, pady=(0, 15))
            self.regular_key_frame.pack_forget()
    
    def on_hotkey_change(self, event=None):
        """Handle hotkey change"""
        hotkey_name = self.hotkey_var.get()
        try:
            self.hotkey_key = getattr(Key, hotkey_name.lower())
            self.setup_hotkey_listener()
        except AttributeError:
            self.show_error_dialog("Error", f"Invalid hotkey: {hotkey_name}")
    
    def get_target_key(self):
        """Get the target key to press"""
        if self.key_mode.get() == "regular":
            key_str = self.regular_key_entry.get().strip()
            if not key_str:
                raise ValueError("Please enter a key")
            return key_str
        else:
            special_key_name = self.special_key_var.get()
            return self.special_keys.get(special_key_name)
    
    def toggle_clicking(self):
        """Start or stop the key clicking"""
        if not self.is_running:
            self.start_clicking()
        else:
            self.stop_clicking()
    
    def start_clicking(self):
        """Start clicking keys"""
        try:
            # Validate inputs
            interval = float(self.interval_entry.get())
            if interval < 0.01:
                self.show_error_dialog("Error", "Interval must be at least 0.01 seconds")
                return
            
            limit = int(self.limit_entry.get())
            if limit < 0:
                self.show_error_dialog("Error", "Press limit must be 0 or positive")
                return
            
            # Get target key
            target_key = self.get_target_key()
            
            # Update UI
            self.is_running = True
            self.stop_event.clear()
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Start clicking thread
            self.click_thread = threading.Thread(
                target=self.click_worker,
                args=(target_key, interval, limit),
                daemon=True
            )
            self.click_thread.start()
            
        except ValueError as e:
            self.show_error_dialog("Error", str(e))
        except Exception as e:
            self.show_error_dialog("Error", f"Failed to start: {str(e)}")
    
    def stop_clicking(self):
        """Stop clicking keys"""
        self.is_running = False
        self.stop_event.set()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def click_worker(self, target_key, interval, limit):
        """Worker thread for clicking keys"""
        count = 0
        
        while not self.stop_event.is_set():
            try:
                # Check limit
                if limit > 0 and count >= limit:
                    self.message_queue.put(("stop", None))
                    break
                
                # Press key
                if isinstance(target_key, Key):
                    self.keyboard_controller.press(target_key)
                    self.keyboard_controller.release(target_key)
                else:
                    self.keyboard_controller.press(target_key)
                    self.keyboard_controller.release(target_key)
                
                count += 1
                self.message_queue.put(("update_counter", count))
                
                # Wait for interval
                if self.stop_event.wait(interval):
                    break
                    
            except Exception as e:
                self.message_queue.put(("error", str(e)))
                break
    
    def reset_counter(self):
        """Reset the press counter"""
        self.press_count = 0
        self.counter_label.config(text="0")
    
    def update_counter(self, count):
        """Update the counter display"""
        self.press_count = count
        self.counter_label.config(text=str(count))
    
    def check_queue(self):
        """Check for messages from worker threads"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                if msg_type == "update_counter":
                    self.update_counter(data)
                elif msg_type == "stop":
                    self.stop_clicking()
                elif msg_type == "error":
                    self.show_error_dialog("Error", data)
                    self.stop_clicking()
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_queue)
    
    def setup_hotkey_listener(self):
        """Setup global hotkey listener"""
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        def on_press(key):
            try:
                if key == self.hotkey_key:
                    self.root.after(0, self.toggle_clicking)
            except AttributeError:
                pass
        
        try:
            self.hotkey_listener = keyboard.Listener(on_press=on_press)
            self.hotkey_listener.start()
        except Exception as e:
            print(f"Warning: Could not setup hotkey listener: {e}")
    
    def create_tray_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='#007acc')
        draw = ImageDraw.Draw(image)
        draw.ellipse([16, 16, 48, 48], fill='white')
        draw.text((28, 28), "K", fill='#007acc', anchor="mm")
        
        return image
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        menu = pystray.Menu(
            item('Show Window', self.show_window),
            item('Hide Window', self.hide_window),
            pystray.Menu.SEPARATOR,
            item('Start/Stop', self.toggle_clicking),
            item('Reset Counter', self.reset_counter),
            pystray.Menu.SEPARATOR,
            item('Exit', self.quit_application)
        )
        
        icon = pystray.Icon(
            "AutoKeyClicker",
            self.create_tray_icon(),
            "Auto Key Clicker",
            menu
        )
        
        # Run tray in separate thread
        self.tray_thread = threading.Thread(target=icon.run, daemon=True)
        self.tray_thread.start()
        self.tray_icon = icon
    
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)
        self.root.after(0, self.root.focus_force)
    
    def hide_window(self, icon=None, item=None):
        """Hide the main window"""
        self.root.after(0, self.root.withdraw)
    
    def quit_application(self, icon=None, item=None):
        """Quit the application"""
        self.stop_clicking()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.quit)
        self.root.after(0, self.root.destroy)
    
    def on_closing(self):
        """Handle window close event"""
        # Show notification on first close (before hiding window)
        if self.show_tray_notification:
            self.show_tray_notification_message()
            self.show_tray_notification = False  # Only show once per session
        
        self.hide_window()
    
    def show_tray_notification_message(self):
        """Show notification that app is still running in tray"""
        self.show_custom_dialog(
            "Auto Key Clicker",
            "The application is still running in the system tray.\n\n"
            "You can access it by clicking the tray icon, or\n"
            "use the hotkey to control key clicking.\n\n"
            "To fully exit, use 'Exit' from the tray menu.",
            dialog_type="info"
        )
    
    def show_info(self):
        """Show information dialog"""
        info_text = """Auto Key Clicker v2.0

A modern keyboard automation tool.

Features:
• Regular and special key support
• Customizable intervals
• Global hotkey toggle
• Press limit option
• System tray integration
• Real-time counter

Press the hotkey or use the tray icon
to start/stop clicking.

Use responsibly and in accordance with
application terms of service."""
        
        self.show_custom_dialog("About Auto Key Clicker", info_text, dialog_type="info")
    
    def show_custom_dialog(self, title, message, dialog_type="info"):
        """Show a custom dark-themed dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.bg_color)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Icon color based on dialog type
        icon_color = self.accent_color if dialog_type == "info" else self.danger_color
        
        # Header frame
        header_frame = tk.Frame(dialog, bg=self.secondary_bg, height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=title,
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=14, weight="bold"),
            anchor="w"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Icon indicator
        icon_label = tk.Label(
            header_frame,
            text="ℹ" if dialog_type == "info" else "⚠",
            bg=self.secondary_bg,
            fg=icon_color,
            font=font.Font(family="Segoe UI", size=20),
            width=3
        )
        icon_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Message frame with scrollbar for long messages
        message_container = tk.Frame(dialog, bg=self.bg_color)
        message_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Text widget for scrollable content
        text_widget = tk.Text(
            message_container,
            bg=self.bg_color,
            fg=self.fg_color,
            font=font.Font(family="Segoe UI", size=10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            width=50,
            height=10
        )
        text_widget.insert('1.0', message)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(message_container, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # OK button
        ok_btn = self.create_modern_button(
            button_frame,
            "OK",
            lambda: dialog.destroy(),
            bg_color=icon_color,
            hover_color="#005a9e" if dialog_type == "info" else "#c82333",
            width=12
        )
        ok_btn.pack(side=tk.RIGHT)
        
        # Calculate optimal size based on content
        dialog.update_idletasks()
        
        # Estimate height needed (base height + text height)
        lines = len(message.split('\n'))
        estimated_height = min(70 + 50 + (lines * 18) + 60, 600)  # Max 600px
        estimated_height = max(estimated_height, 250)  # Min 250px
        
        # Center dialog on screen
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (estimated_height // 2)
        dialog.geometry(f'450x{estimated_height}+{x}+{y}')
        dialog.resizable(False, False)
        
        # Focus on OK button
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.focus_set()
        ok_btn.focus_set()
    
    def show_error_dialog(self, title, message):
        """Show a custom dark-themed error dialog"""
        self.show_custom_dialog(title, message, dialog_type="error")


def main():
    root = tk.Tk()
    app = ModernKeyClicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()


