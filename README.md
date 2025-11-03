# 🚀 Auto Key Clicker - Modern Edition

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)

A sleek, modern Python-based auto key clicker with a beautiful dark-themed GUI and full system tray support.

</div>

---

## ✨ Features

- 🎨 **Modern Dark Theme UI** - Beautiful, minimalist interface designed for ease of use
- ⌨️ **Flexible Key Support** - Regular keys and special keys (enter, space, arrows, function keys, etc.)
- ⚡ **Customizable Timing** - Set intervals from 0.01 seconds with precision
- 🔥 **Global Hotkey** - Toggle start/stop from anywhere (default: F6)
- 📊 **Press Counter** - Real-time tracking with reset functionality
- 🎯 **Press Limits** - Set maximum number of presses (0 for unlimited)
- 🖥️ **System Tray** - Minimize to tray with full control access
- 🔒 **Safety Features** - Built-in protections against system flooding
- 🌐 **Cross-Platform** - Works on Windows and Linux

---

## 📋 Requirements

- **Python 3.7 or higher**
- Required packages (automatically installed via `requirements.txt`):
  - `pynput` - Keyboard input simulation
  - `Pillow` - Image processing for tray icon
  - `pystray` - System tray integration
  - `pyinstaller` - For building standalone executables (optional)

---

## 🚀 Installation

### Option 1: Standalone Executable (Recommended)

1. Download the latest `AutoKeyClicker.exe` from the [releases](../../releases) page
2. Double-click to run - no installation required!

### Option 2: From Source

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd KeyClicker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python key_clicker.py
   ```

---

## 🔧 Building the Executable

To create your own executable:

1. **Install all requirements** (including PyInstaller)
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**
   ```bash
   python build.py
   ```

3. **Find your executable** in the `dist/` folder

---

## 📖 Usage Guide

### Basic Usage

1. **Launch the application** (executable or Python script)

2. **Configure your settings:**
   - **Key Selection**: Choose between regular keys or special keys
     - Regular: Type any character (e.g., "a", "1", "z")
     - Special: Select from dropdown (enter, space, arrows, function keys, etc.)
   
   - **Interval**: Set delay between presses in seconds (minimum: 0.01s)
   
   - **Hotkey**: Choose a function key (F1-F12) to toggle start/stop globally
   
   - **Press Limit**: Set maximum presses (0 = unlimited)

3. **Start clicking:**
   - Click the **"▶ Start"** button, or
   - Press your configured **hotkey** (default: F6)

4. **Monitor progress:**
   - Watch the real-time counter
   - Use **"Reset"** to zero the counter anytime

5. **Stop clicking:**
   - Click the **"■ Stop"** button, or
   - Press your hotkey again, or
   - Use the system tray menu

### System Tray

The application runs in your system tray when minimized:

- **Show/Hide Window** - Toggle main window visibility
- **Start/Stop** - Control clicking from tray
- **Reset Counter** - Reset the press counter
- **Exit** - Close the application

---

## ⌨️ Supported Special Keys

The application supports the following special keys:

**Navigation:**
- `enter`, `space`, `tab`, `backspace`, `delete`, `esc`

**Modifiers:**
- `shift`, `ctrl`, `alt`

**Arrow Keys:**
- `up`, `down`, `left`, `right`

**Function Keys:**
- `f1` through `f12`

---

## 🛡️ Safety Features

- ✅ Minimum interval enforcement (0.01s) prevents system flooding
- ✅ Easy stop mechanisms (button, hotkey, tray menu)
- ✅ Input validation for all settings
- ✅ Thread-safe implementation
- ✅ Real-time activity monitoring via counter
- ✅ Graceful error handling

---

## ⚙️ Configuration

### Default Settings

- **Hotkey**: F6
- **Interval**: 1.0 seconds
- **Press Limit**: 0 (unlimited)
- **Theme**: Dark mode

### Customization

All settings can be changed directly in the GUI. The hotkey can be changed from the dropdown menu and will take effect immediately.

---

## 📝 Notes & Warnings

⚠️ **Important Considerations:**

- **Permissions**: The application requires appropriate permissions to simulate keyboard input
- **Application Blocking**: Some applications may block simulated key presses (e.g., games with anti-cheat)
- **Administrator Rights**: On Windows, you may need to run as administrator for some applications
- **Responsible Use**: Use this tool responsibly and in accordance with the terms of service of applications you're using it with

💡 **Tips:**

- Use the hotkey for quick toggling while gaming or working
- Set a press limit for batch operations
- Monitor the counter to track progress
- The system tray keeps the app accessible while hidden

---

## 🏗️ Project Structure

```
KeyClicker/
├── key_clicker.py      # Main application (modern GUI)
├── build.py           # Executable build script
├── requirements.txt   # Python dependencies
├── README.md         # This file
├── .gitignore        # Git ignore patterns
├── dist/             # Generated executables (ignored)
│   └── AutoKeyClicker.exe
└── build/            # Build artifacts (ignored)
```

---

## 🐛 Troubleshooting

### Issue: Hotkey not working
- **Solution**: Try a different function key or restart the application
- On Linux, you may need additional permissions for global hotkeys

### Issue: Keys not being registered in an application
- **Solution**: Run as administrator (Windows) or check application settings
- Some applications block simulated inputs for security

### Issue: Import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Tray icon not showing
- **Solution**: Check system tray settings in your OS
- Some Linux desktop environments require additional packages

---

## 📄 License

This project is provided as-is for educational and personal use.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

## 🎯 Roadmap

Future enhancements may include:
- Light theme option
- Preset configurations
- Macro recording
- Multiple key sequences
- Scheduled automation

---

<div align="center">

**Made with ❤️ for automation enthusiasts**

⭐ Star this repo if you find it useful!

</div>


