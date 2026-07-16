# M5DSP Flashing & Firmware Update Guide (from v1.5.13)

This guide describes how to program the firmware onto your M5Stack Core2 device, either for the first time (blank chip) or when updating an existing installation.

## *Please read the following information carefully before proceeding with the firmware upload to your device!*
---

## A: FIRST TIME INSTALLATION / Full Recovery (Factory Flash)

Use this method for:

* Brand new M5Stack Core2 devices.
* Devices with erased or corrupted flash memory.
* Factory recovery.
* Migration from **MP3Player** firmware to **HaM5DSP** firmware.

> [!IMPORTANT]
> Migration from **MP3Player** to **HaM5DSP** must **ALWAYS** be performed using a **FULL** image (`M5DSP_Full_[VER].bin`).>
> Do **NOT** use an `HAM5DSP_upd_[VER].bin` file for migration from MP3Player, as the required bootloader, partition layout, and system structures may differ.
	
### How to upload the full firmware using online programming tool (Chrome Browser) or Espressif Flash Tool:
1. Connect your M5Stack Core2 to your PC via USB.
2. Open the Web Serial Flasher in Google Chrome https://www.espboards.dev/tools/program/
3. Select the baud rate (e.g. `115200` or `921600`) and click **Connect**.
4. Choose the complete flash image `M5DSP_Full_[VER].bin`.
5. Set the offset address to **`0x00`** (Hexadecimal).
6. Click **Program / Flash** and wait until the process completes.

	**Full Image Details**
	* **File:** `M5DSP_Full_[VER].bin`
	* **Size:** exactly `16,777,216` bytes (16 MB)
	* **Flashing Offset:** `0x0`

> [!NOTE]
> Flashing a FULL image overwrites the entire device flash memory and resets all settings to factory defaults.
> You will need to re-enter the License Key via Serial Terminal.

---

## B: FIRMWARE UPDATES

There are 3 ways to update the M5DSP firmware:

1. **Web Serial Flasher (Chrome Browser)**: Flash using online tools (like ESP Web Flasher) using the ESP32 hardware ROM bootloader.

2. **In-Application UART OTA (Recommended for Updates)**: Update directly from a companion app (mobile/desktop) over the standard serial connection while the device is running. Safe, preserves all settings, and is brick-proof.

3. **SDcard Update (Coming Feature)**: Update using updates stored on SD card. 
---

### 1. Via **Web Serial Flasher (Chrome Browser)**: ###
1. Connect your M5Stack Core2 to your PC via USB.
2. Open the Web Serial Flasher in Google Chrome https://www.espboards.dev/tools/program/
3. Select the baud rate (e.g. `115200` or `921600`) and click **Connect**.
4. Choose the **update flash image** `M5DSP_upd_[VER].bin`.
5. Set the offset address to **`0x10000`(ten thousands)** (Hexadecimal).
6. Click **Program / Flash** and wait until the process completes.

	**Full Image Details**

	* **File:** `M5DSP_upd_[VER].bin`
	* **Size:** around  1,4b MB 
	* **Flashing Offset:** `0x10000`(ten thousands)

### 2. Not yet released. ###

### 3. Detailed instruction after implementation. ###


[Last update: July 16, 2026]
