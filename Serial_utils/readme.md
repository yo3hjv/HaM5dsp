===========================================================
# 1. HaM5dsp_serial_utility.py - M5DSP Preset & License Programmer

This utility script is designed to program some predefined values into Voice and CW DSP presets (as a starting point)  as well as license validation keys onto the **HaM5dsp** (M5Stack Core2) device via a serial (USB) link.

## Features

- **Port Autodetection & Auto-retry**: Automatically lists all active COM/serial ports. If a connection fails (e.g., if the port is busy or locked by the Arduino IDE Serial Monitor), it notifies you and lets you select again without crashing.
- **Protocol Handshake**: Automatically establish serial protocol link.
- **Dot-Based Progress Indicator**: Displays a clean, compact progress indicator (`.`) as presets are programmed.
- **Fail-Safe Aborts**: Aborts immediately if a transmission fails or times out.
- **License Registration**: Validates and registers your licensing parameters (`AUTH:CALL$TIER*KEY`) in NVS, triggering an automatic reboot of the device upon successful completion to apply your new features.

---

## Requirements

1. **Python 3.x** installed on your system.
2. **PySerial** module. You can install it via pip:
   ```bash
   pip install pyserial
   ```

---

## How to Use

1. Connect your **M5Stack Core2** (HaM5dsp) to your computer using a USB Type-C cable.
2. Close any programs that might lock the serial connection (such as the Arduino Serial Monitor).
3. Open a terminal/command prompt, navigate to the script's directory, and run:
   ```bash
   python HaM5dsp_serial_utility.py
   ```

### Step 1: Port Selection
Upon startup, the script scans and lists your system's active COM ports.
- Enter the number corresponding to your device's port (e.g., `1` for `COM5`).
- If your port isn't detected, select **Manual entry** to type the port name directly.

### Step 2: Programming Menu
Once a connection is established, the script displays the menu:
```text
==================================================
                 M5DSP PROGRAMMER MENU
==================================================
  1. Program presets only
  2. Program presets & license key
  3. Program license key only
  4. Exit
==================================================
```
Select the option matching your requirements.
### NOTE: If you have a DSP+MP3 License, you can use Option 3 only as the Companion App protocol is not available.


### Step 3: Enter License Key (Options 2 & 3 only)
If you are programming a license key, the script will request it. 
* Note: The key must start with `AUTH:, just like it was received via email or othera means. (e.g., `AUTH:HAMTEST$7*8F8AB278D6C855E0`).

---

## Console Outputs

### Preset Programming
```text
[!] Establish Serial Link... Link Established

[!] Programming 56 presets: ................................................ [OK]
[📊] SUMMARY: Successfully programmed all 48 presets.
```

### Abort on Failure/Timeout
If a transmission issue occurs, the script stops immediately to prevent writing corrupt/incomplete profiles:
```text
[!] Programming 48 presets: .......... [TIMEOUT]

[-] ERROR: Command 'C0BW500' failed. Response: TIMEOUT (Last response: )
[-] Programming aborted.
```

### Successful License Key Application
```text
[!] Programming license key: AUTH:HAMTEST$7*8F8AB278D6C855E0 [OK]
[+] License key accepted!

[+] Serial port closed.
HaM5dsp will reboot now.
```

---

## Troubleshooting

- **PermissionError: Access is denied**: This means the port is already in use by another software (Arduino IDE, Cura, Putty, etc.). Close the other application, and the script will let you re-select the port to retry.
- **TIMEOUT Errors**: Make sure your M5DSP firmware is running and responsive. Ensure you are using the correct baud rate (default: `115200`).


===========================================================
# 2. Simple_serial.py -  Simple Serial Terminal
This utility script is a simple terminal to send commands in Human protocol to **HaM5dsp** (M5Stack Core2) device via seria port.

## Requirements

1. **Python 3.x** installed on your system.
2. **PySerial** module. You can install it via pip:
   ```bash
   pip install pyserial
   ```
## How to Use

1. Connect your **M5Stack Core2** (HaM5dsp) to your computer using a USB Type-C cable.
2. Close any programs that might lock the serial connection (such as the Arduino Serial Monitor).
3. Open a terminal/command prompt, navigate to the script's directory, and run:
   ```bash
   python Simple_serial.py
   ```
