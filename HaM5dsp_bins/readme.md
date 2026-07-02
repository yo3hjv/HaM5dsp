# M5DSP Flashing & Firmware Update Guide ( from v1.2.0)

This guide describes how to program the firmware onto your M5Stack Core2 device, either for the first time (blank chip) or when updating an existing installation.

---

## 1. Firmware Update Methods

There are three ways to flash or update the M5DSP firmware:

1. **In-Application UART OTA (Recommended for Updates)**: Update directly from a companion app (mobile/desktop) over the standard serial connection while the device is running. Safe, preserves all settings, and is brick-proof.
2. **Web Serial Flasher (Chrome Browser)**: Flash using online tools (like ESP Web Flasher) using the ESP32 hardware ROM bootloader.
3. **Arduino IDE / Command Line**: Compile and flash directly from source code.

---

## 2. In-Application UART OTA (Brick-Safe & Preserves Settings)

Introduced in **v1.2.0**, this method allows updating the device over the USB-Serial cable without putting the ESP32 into bootloader mode. The running app receives the firmware block-by-block and writes it to the inactive flash partition.

* **License Requirement**: Requires a **FULL Tier7** active license (`DSP+MP3+APP`).
* **Preservation**: 100% of your NVS configurations, callsign licenses, and battery health calibrations are preserved.
* **Brick Protection**: If the cable is disconnected during transfer, the device continues running the old firmware normally.

### Serial Protocol via USB Cable (APP Mode)
Connect the Core2 to Android Phone via USB-C cable.
Select Update Firmware, choose FW ''.ino.bin'' file and press UPLOAD.

---

## 3. Flashing with Web Serial Flashers (Chrome Browser)

You can use browser-based tools such as the [ESP Web Flasher](https://espressif.github.io/esptool-js/) to program the device. 

### A. Performing a Standard Update (Preserves Settings)
If your device already has the bootloader and partition table flashed (just updating FW), you only need to update the application itself.

1. Connect your M5Stack Core2 to your PC via USB.
2. Open the Web Serial Flasher in Google Chrome.
3. Select the baud rate (e.g., `115200` or `921600`) and click **Connect**.
4. Choose the compiled application binary (e.g., `M5DSP.ino.bin` or `M5DSP.bin` - size is approx. 1.4 MB).
5. Set the offset address to **`0x10000`** (Hexadecimal).
   > [!CAUTION]
   > Do **NOT** flash the app binary at `0x0`. Doing so will overwrite the bootloader and crash the device.
6. Click **Program / Flash**. This will update the application code but leave the NVS partition (which stores user configurations) untouched.

---

### B. First-Time Installation (Blank / Erased Chip)
If you have a brand new M5Stack Core2 or have performed a full chip erase, you need to write the system structures (Bootloader, Partition Table, and App). You can do this in two ways:

#### Option 1: Using the Full 16MB Flash Image (easiest)
Write the complete 16 MB binary dump (exactly `16,777,216` bytes) which contains the bootloader, partition table, empty NVS space, and the app all-in-one.
* **File**: `M5DSP_Full_16MB.bin`
* **Flashing Offset**: **`0x0`**
* *Note: This will overwrite everything, resetting NVS settings to factory defaults.*

#### Option 2: Using Individual Binaries (standard)
If you compile from source, you will have three separate files in your build directory. Load them into the Web Flasher at the following exact offsets:

| Binary File | Offset Address | Description |
| :--- | :--- | :--- |
| `bootloader.bin` | **`0x1000`** | System boot code |
| `partitions.bin` (or `partition-table.bin`) | **`0x8000`** | Partition boundaries |
| `M5DSP.ino.bin` (or `M5DSP.bin`) | **`0x10000`** | Main Application code |

Click **Program** to write all three files to the device. Once flashed, future updates can be done by simply writing `M5DSP.ino.bin` at `0x10000`.
