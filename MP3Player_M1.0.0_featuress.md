# HaM5dsp - MP3Player Release (M1.0.0 "Free Use")
**User Guide & Features Overview**

---

## 1. Introductory Summary

**Hardware Requirements:**
To run this firmware, the following hardware configuration is mandatory:
* Main Controller: **M5Stack Core2** (v1.0 or v1.3) or **Core2 for AWS**
* Audio Interface: **M144 ES8388 Audio Module**
* Base Expansion: **Bottom2**

The **HaM5dsp-MP3Player ("Free Version M1.0.0")** transforms the HaM5dsp device into a dedicated, premium, standalone audio player designed for high-fidelity playback of MP3 files from an SD card. This version has been decoupled from any licensing requirements and boots directly and exclusively into the music player interface.

The interface offers an extremely fluid user experience, combining hierarchical navigation (the "Cassette" system), precise touch control assisted by a native haptic engine, and an adaptive "Dual InfoZone" display. The user experience is complex and highly interactive: users are encouraged to explore the functionalities by executing short and long touches on various UI elements across the screen (for example, a long press on the battery icon reveals hidden power management details).

Furthermore, the device highlights an impressive visual VU-meter on the lateral LED strips, extended support for high-capacity memory cards (exFAT), and the ability to manipulate playback seamlessly with features like *Continuous Seek* or *Smart Shuffle*.

---

## 2. Detailed Features Overview

### SD Card note:
*	Must be formatted as exFat!
*	Folders must start with "mp3-" to be reconised as valid mp3 containers.

### 2.1. Navigation and "Cassette System" Organization
The player uses an elegant approach for the media library, treating folders like "Audio Cassettes":
* **TAPES:** Max. 50 Tapes. Each root folder on the SD card containing audio files is considered an independent Tape.
* **TRACKS:** Max.50 tracks in each Folder. The files inside a folder represent the tracks of that specific tape.
* **ALL TRACKS:** Offers the possibility to gather absolutely all tracks from the SD card into one massive playlist.

**How to navigate:**
A touch on the screen in the List area allows you to scroll through the tracks. To change the "Tape" and return to the previous menu, touch the **top bar (Header)** of the screen, or alternatively, perform a **Long Press** on the **left hardware button** (BtnA). The system includes native circular support (when you reach the last track and press 'DOWN', the list automatically wraps around to the first track).

### 2.2. Dual InfoZone & Progress Bar
The upper part of the screen ("InfoZone") hides two different display modes, which you can toggle at any time with a simple tap:
* **Page 0 (Active/Scrolling Mode):** Dynamically displays the currently playing track name with a horizontal scrolling effect, followed by the next track in the list.
* **Page 1 (Analytical Mode):** Displays a static, highly readable (enlarged font) view containing the current title, encoding type (CBR/VBR), Bitrate (e.g., 320kbps), Remaining Time, and an extremely clean **Progress Bar** that fills up as the track advances.

### 2.3. Continuous Seek Feature
If you want to seek through a specific song to listen to a certain fragment, there is no need for an imprecise touch navigation bar. Simply **Long Press** the virtual `Prev` or `Next` buttons on the screen. The song will make repeated and fluid "jumps" through time, directly proportional to the duration of the hold, helping you reach the exact desired second.

### 2.4. Visual Customization (Themes and Haptics)
The user experience gains a "premium" weight thanks to the Haptic feedback. Any intentional interaction with the screen generates a micro-vibration, confirming the touch command.
At the same time, the visuals can adapt to your environment: you have full chromatic themes available such as **Dark**, **Light**, **Military**, or the retro **Amber** theme, which you can select from the general configuration menu (*DevSet* -> *Device* tab).

### 2.5. Extended Hardware Support and SD Removal Protection
Do not worry about modern SD cards. The player natively reads high-capacity **exFAT** formatted cards (64GB, 128GB, etc.). Furthermore, if you accidentally extract the physical card during playback, the device features an advanced *SD Removal Protection* system—it will automatically and gracefully halt playback, displaying an error, without freezing or crashing the screen.

---

## 3. Lateral VU-meter: Visual Dynamics

One of the most attractive features of the device is the **Illuminated VU-meter**, implemented on the LED strip (SK6812) located on the sides of the **M5Stack Bottom2** casing.

**How it works and how to configure it:**
For the VU-meter to come to life, the system requires a minimal hardware configuration, because the external LED strips need a dedicated 5V power supply.
1. **Power Supply (5V OUT):** Navigate to the Settings Menu (**Setup / DevSet** -> `Device` tab) and ensure that the `Perif. 5V` option is set to **OUT**. This setting routes power from the battery to the lateral bus to light up the LEDs. (Note: changing this requires rebooting the device to apply at the hardware level).
2. **Software Activation:** Navigate to the `MP3set` tab and ensure that the `MP3 LEDs` function is toggled to **ON**.

Once these two conditions are met (5V bus activated outwards and the VU-meter function turned on), the SK6812 LEDs will pulse from bottom to top, reacting spectacularly and dynamically based on the actual intensity of the played music. During moments of complete silence or when pressing *PAUSE*, the LEDs gracefully turn off thanks to an integrated noise gate.

---

## 4. Note regarding the "DevSet" (Setup) Menu
Because this firmware version (M1.0.0) was intentionally isolated as an **exclusive free MP3Player application** ("Free Use"), a significant part of the advanced modules present in the baseline HaM5dsp architecture have been disconnected.

When entering the **Setup (DevSet)** menu, you will notice the presence of options, tabs, or functions intended for telecommunications mode or digital radio signal processing (e.g., DSP, vocal filters, CW decoders, Noise Reduction - NR, Serial or Bluetooth commands).

> **Important:** These technical options (DSP) act upon functions that are inactive in the "Free" version. Although they can be pressed, adjusted, or scrolled inside the menu, modifying them will have absolutely no effect on the device or the quality of the MP3 playback. They have been kept strictly as the structural operating skeleton of the unified system. The relevant menus for you remain the general `Device` tab (for Date, UTC Time, Theme, Brightness, Haptics, 5V Bus etc) and the specific `MP3set` tab.
