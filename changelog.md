## Note: The updates are cumulative; just update to the latest. The changelog keeps track also on unreleased versions!

# v1.2.0 - MAJOR UPDATE. UART OTA Update & Security Gating (2026-06-30)
--------------------------------------------------------------------------------
- [OTA][UART] Implementation of the "in-application" firmware update system over serial cable (UART OTA) using the native ESP-IDF A/B partition APIs.
- [OTA][SECURITY] Restriction of firmware update execution exclusively to devices with a APP license. 
- [OTA][UI/UX] Added visual feedback during updates: the Info area is overlaid with a light red background and black `"FIRMWARE UPDATING"` text displayed on two lines, while also applying a hardware mute at the codec level.
- [OTA][STABILITY] Implementation of a dedicated 10 KB heap buffer and a 15-second inactivity timeout for automatic recovery from errors or accidental cable disconnections.
- [NVS] Implementation of the full backward compatibility across firmware version changes. Since this version on.
- [MP3][UI/UX] Action execution moved to release (Touch-Up) with Cancel-on-Slide protection support for all MP3 module keys.
- [SYSTEM][HARDWARE] Implementation of a global mutex for serializing access to the shared SPI bus. This prevents concurrent direct writes to SPI hardware registers, eliminating Guru Meditation errors and audio sample stuttering/duplication during intensive GUI interaction.
- [BUGFIX][SD_Manager] Automatic and safe locking of all SD card read, write, seek, and directory listing operations.
- [DEBUG] Added granular debugging configuration options `NVS_DEBUG_LOGS_ENABLED` and `SD_DEBUG_LOGS_ENABLED` in `config.h` to make NVS and SD_Manager debug messages fully conditional and configurable.
- [BUGFIX][MP3][UI/UX] Fixed smooth scrolling for the "Current Track" row.
- [MP3][UI/UX] Added display of the folder/tape name in square brackets `[FolderName]` for both rows (current track and next track) in the Info area. Folder details are extracted from the full file path stored on the SD card.


# v1.1.0 - MP3 Player PSRAM Optimization & SD Index Refactor (2026-06-27)
## NOTE: This update doesn not require ERASE FLASH and recovers previous user settings
--------------------------------------------------------------------------------
- [MP3][MEMORY] Refactored code. Moved track indexing structures from internal DRAM to external PSRAM (SPIRAM).
  → Frees 250+ KB DRAM at boot; prevents black screen and system freezes when scanning large exFAT cards (~2500 tracks).
- [MP3][UI/UX] GFX processes moved in PSRAM to free space in internal SRAM.
- [BUGFIX][MP3] Fixing the FFW/REW function (Long Press on Prev/Next) crash.
- [HW][POWER] Fine tuned lower threshold for Battery Capacity measurement due to wide tolerances in Core2 PMIC HW components.


# v1.0.10 - UI/UX Refinements & PEK Config (2026-06-22)
--------------------------------------------------------------------------------
## NOTE: This update doesn not require ERASE FLASH and recovers previous user settings
- [BUGFIX][UI/UX] Filtering of I2C errors (read timeouts / Wire failures) on the FT6336U bus. This eliminates unwanted phantom auto-jumps in the MP3Player module's List menu.
- [UI/UX] Removal of the redundant "Balance" setting from the MP3set tab in the Setup menu (DevSet), as the function is already present in the general Device tab (DevSet).
- [UI/UX] Moving the "HP Std" setting from the VSet submenu (Voice Settings) to the general Device tab (DevSet), because the audio jack standard for headphones (ground/mic pins) is a global hardware property.
- [UI/UX] Renaming the option labels for the headphone standard from "American" and "National" to the more user-friendly modern forms "CTIA (New)" and "OMTP (Old)", respectively.
- [POWER][COMPILATION] Moving the configuration for the physical Power button (AXP192 PEK - Reg 0x36) into the global `config.h` file under the constant `AXP192_PEK_REG_CONFIG` for quick access and modification of power on/off timings, automatically applied during the boot sequence.
- [BUGFIX][SERIAL] Fixed parsing of haptic durations from Human Protocol. The `haptshortdur` and `haptlongdur` commands are now correctly recognized and configured in NVS.
- [DOCUMENTATION] Alignment of the `Human_serial.txt` documentation by replacing the old `haptshortx` / `haptlongx` parameters with `haptshortdur` and `haptlongdur`.
- [DUMP] Added display of the `haptshortdur` and `haptlongdur` parameters in the `dump` diagnostic output (`dspDumpAll`).


# v1.0.8 – CW 3D Linear Panning & FFT Info Zone (2026-06-17)
--------------------------------------------------------------------------------
## NOTE: This update doesn not require ERASE FLASH and recovers previous user settings
- [UI/UX] FFT Info Zone: In CW mode now dynamically displays the current Center Frequency (CF) on the left and Bandwidth (BW) on the right. In Voice mode, displays Low Cut (LC) on the left and High Cut (HC) on the right. The previous Span display has been removed to make space for these critical parameters, with both modes benefiting from symmetrical protected background boxes.
- [UI/UX] Moved the "Bal." (Balance) parameter from the VSet (Voice Settings) submenu to the Device tab, last position, right after the 1 kHz test tone. It can now be reset directly from the Device menu.
- [DSP] Implemented a Hybrid Linear model for 3D CW spatialization. Frequencies outside the filter are now clamped at maximum phase (180°) and maximum left/right width, creating absolute physical separation (rear positioning) of low-frequency interference (left) and high-frequency interference (right), leaving the desired signal (inside the filter) clean in the center. The default value for Alpha 3D is 6.
- [FEATURE][SERIAL] Addition of the FW Version Query in Human Protocol and in Machine Protocol commands to report the installed firmware version to the console or Companion App.


# v1.0.7 - NVS SOH Sync Fixes & UI Refinements (2026-06-15)
--------------------------------------------------------------------------------
## NOTE: This update requires an ERASE FLASH before updating and re-entering the License Key.
- [BUGFIX][POWER] Fixed a critical RAM–NVS sync issue that reset the battery’s real capacity (SOH) to `0.0 mAh` on every reboot. The correct measured value now persists reliably across restarts.
- [BUGFIX][POWER] Ensured the measured battery capacity is properly saved when users change battery capacity or reset the device from DevSet → BATT_CAP.
- [BUGFIX][UI/UX] Fixed a refresh issue in *Power Diagnostics* where the first smart redraw could be skipped during scrolling.
- [FEATURE][SERIAL] Added `dumpnvs` command (Human Protocol) to inspect stored NVS data in read-only mode and quickly detect mismatches between flash storage and runtime configuration.
- [UI/UX][SLIDER] Improved frequency sliders (Lcut, Hcut, CF, BW) with quadratic scaling for much finer control in lower frequency ranges.
- [FEATURE][UI/UX] Added quick toggle for Date (EU ↔ US) and Time format (Local ↔ UTC) via long-press on the main screen clock/date area.
- [FEATURE][PERSISTENCE] Date/time format preference is now saved and persists across reboots.
- [FEATURE][SERIAL] Added Machine Protocol commands (`DATU`, `DATE`, `HLOC`, `HUTC`) for explicit format control, also included in async handshake responses.
- [FEATURE][DSP] Added selectable I2S input channel (Left/Right) for improved audio flexibility, enabling bypass of hardware filtering for cleaner Hi-Fi input.
- [FEATURE][UI/UX] Added `FFTspan` setting (DevSet → Voice Settings) to adjust FFT display range (4 kHz / 7 kHz / 10 kHz), with persistent storage.
  

# v1.0.6 - Haptic, Serial EQ & Bulletproof SD LFN Fallback (2026-06-14)
--------------------------------------------------------------------------------
- [FIX][HAPTIC] Haptic vibrations no longer get stuck during long track loading. Vibrations now stop correctly before playback begins.
- [FIX][EQ SYNC] EQ mode changes are now instantly reflected in the Companion app, ensuring accurate synchronization when switching modes.
- [IMPROVEMENT][SD] Significantly improved file opening reliability. Tracks now load correctly even if filenames contain special or uncommon characters.
- [NEW][EXPORT] Full preset export added. All saved Voice and CW configurations are now included during synchronization with external tools.
- [FIX][PLAYBACK] Improved playback stability. Eliminated random track skips and file read errors from the SD card.
- [FIX][FILE NAMES] Tracks with special characters in their names now load correctly without requiring manual renaming.
- [IMPROVEMENT][TOUCH] DSP sliders now respond instantly, with no lag when adjusting settings.
- [FIX][PLAYBACK START] Fixed rare playback startup issues that could prematurely stop tracks.
- [IMPROVEMENT][AUDIO] More reliable handling of corrupted audio data, resulting in smoother playback.
- [TEST] Internal testing tools updated for better haptic feature coverage.

# v1.0.0 Release Version (2026-06-13)
________________________________________________________________________________

# v0.35.0 to v0.36.7 - Features & Bug Fixes Summary (2026-06-13)
--------------------------------------------------------------------------------
- [POWER] Refined battery capacity measurement (Coulomb Counting) by automatically detecting charge completion and starting tracking only when discharging below the 4.12V maximum reference voltage.
- [POWER] Saved the real capacity value under a dedicated persistent internal storage key to survive firmware upgrades and global setting resets.
- [POWER] Disabled VBUS at startup to prevent current loops and back-feeding when operating on battery.
- [DSP] Replaced technical decay coefficient with a user-friendly millisecond parameter (default 150ms) for the LED signal level meter.
- [DSP] Implemented a dual-bar LED Signal Meter in DSP Mode (Left shows raw ADC input level, Right shows digitally attenuated level).
- [DSP] Restored the 1 KHz sinus test tone generator (selectable as OFF, Left channel, Right channel, or Both channels).
- [UI] Added a visual red overload warning ("OVL!") on the VOICE/CW selection button that highlights for 1 second when the audio input signal exceeds safe limits (clipping).
- [UI][MP3] Implemented dual-page screens in the top display Info Zone (Page 0 for scrolling track info, Page 1 for static title, bitrate, progress bar, and remaining playback time).
- [UI] Fixed live redraw issues on the DevSet settings page, ensuring configuration changes update immediately on screen.
- [MP3] Added proactive SD Card Hot-Swap protection to stop the engine and clean up file handles immediately if the SD card is removed during playback.
- [MP3] Implemented continuous track fast-forward/rewind (seeking) every 250ms when long-pressing the Next/Previous buttons.
- [MP3] Rebuilds the active playlist immediately in the background upon selecting tapes/cassettes without stopping the current track if it remains selected.
- [MP3] Fixed playback speeds by pre-scanning track sample rates and adjusting hardware clocks dynamically before starting playback.
- [MP3] Introduced an anti-stuck watchdog that automatically skips corrupt or incompatible MP3 files after 5 seconds of inactivity.
- [MP3] Linearized volume control (0-100%) for natural and predictable volume adjustments on both MP3 and DSP modes.
- [MP3] Fixed playlist navigation labels and tape checkbox toggling when long-pressing the select button.
- [AUDIO] Fixed unprocessed signal leakage into the right channel in Voice Mode (Left channel is now cleanly duplicated).
- [SERIAL] Streamlined status query responses by removing the ~ACK suffix, keeping it only for write commands and actions.
- [SERIAL] Added real-time status updates over the serial port whenever settings are adjusted manually on the screen menus or when page screens cycle.


# v0.35.0 (2026-06-08)  MP3 Progress Bar, Dual InfoZone & Continuous Seek 
--------------------------------------------------------------------------------
- [BUGFIX][UI/MP3] Progress Bar 0% Overwrite.
- [BUGFIX][MP3] SD Card Hot-Swap Detection: Added protection against SD card removal during playback. Read errors now trigger an immediate safe stop, buffer clear, and file closure.
- [SYSTEM][DEBUG] Wrapping Console Output: Persistent debug messages are now conditionally hidden, keeping the console clean in normal (Release) usage.
- [MP3][PROBE] Duration & Bitrate: Implemented full-file scanning with VBR/CBR support (ignoring metadata) with silent decoder. Provides accurate track duration and estimates for the next track.
- [UI][MP3] Dual InfoZone: The InfoZone now supports two switchable screens via Info Zone tap:
  - Page 0: Scrolling display (Current Track, Next Track).
  - Page 1: Static title (large), plus bitrate/type (CBR/VBR), progress bar, and remaining time.
- [UI][MP3] Smart Refresh: Optimized partial refresh to eliminate flickering by updating only the progress area each second while keeping the title unchanged.
- [MP3][SEEK] Continuous Seek on Long Press: Holding PREV/NEXT enables repeated seek forward/backward every 250ms. Includes full boundary protection (end of file triggers next track).
- [SYSTEM][RAM] PSRAM Allocation optimisation.
- [BUGFIX] Previous bugs FIXED.



# v0.34.0 (2026-06-07)
--------------------------------------------------------------------------------
- [UI/UX] - BT settings obfuscated. Stack limit exceeded: Mp3Task crashed due to a stack overflow (8 KB stack too small for minimp3 + EQ + DRC). Additionally, the memory required for proper Bluetooth operation prevents correct indexing of the desired number of tracks; for stability, the track count must be significantly reduced.
- I will continue to develop nonBT versions only.
  


# PLANNED IN vB.0.5
--------------------------------------------------------------------------------
- [UI/UX][POWER][SERIAL] Add Device setup item to compensate End of Charge Voltage due to variations in AXP192; add commands in Serial Protocols.
- [UI/UX] Add "NR Lev" on slider carousel.   FIXED in 0.34.0
- [UI/UX] Add function to revert to "Vol" on long press on btnB in Main Viewport.
- [UI/UX] Adjust Battery Icon Charging action appeareance for higher contrast. FIXED in B.0.4i
- [UI/UX] Reorganise the order of items in Setup pages & subpages. NOT YET FIXED, WAIT FOR FEEDBACK
- [MP3 List] - Add wrap-around (circular) navigation in Tapes and Tracks lists. FIXED in B.0.4o
- [POWER] - SOH (State of Health) for battery: Implement complex determination instead of simple Coulomb Counting. FIXED in B.0.4o
- [POWER][UI/UX] Represent SoC based on VBat AND Coulomb counting not only VBat. NOT FIXED - NOT NECESSARY, SEE ABOVE
- [BUGFIX][UI/UX] When Screensaver is activated via Serial, clock and date are superimposed over the Main Viewport items. FIXED in B.0.4o.
- [BUGFIX][UI/UX] Power Diagnostics page - Smart Refresh is needed. FIXED in B.0.4o
- [UI/UX] Power Diagnostics page - ADC indication no longer needed. FIXED in B.0.4o
- [BUGFIX][UI/UX] CWspdL/CWsdpH edit logic in CWsetup menu not corelated to btnA-btnC actions and labels. FIXED in B.0.4g
- [BUGFIX] - other bugs from feedback...
  

# vB.0.4f - Minor fixes (2026-06-05)
--------------------------------------------------------------------------------
- [UI/UX] Guard space added on nav buttons A, B, C.
  

# vB.0.4 - Setup Reorganization, BT Debounce Fix (2026-05-27)
--------------------------------------------------------------------------------
- [UI/UX] Relocating the InGain and InAtt items from the VSet (Voice Settings) submenu to the Device submenu, correctly reflecting their global nature as hardware/DSP settings applied across the entire audio pipeline, independent of the operating mode.
- [SYSTEM] Updating the Granular Reset logic: resetting InGain and InAtt values to their defaults is now performed from the Device submenu (RESET DEVSET DEFAULTS), not from VSet.
- [SYSTEM][UI/UX] Mode-dependent touch debounce: the 40 ms RF filter is enabled exclusively in MP3 Player mode with Bluetooth active. In DSP mode, touch inputs are validated immediately upon release, eliminating the artificial latency introduced by the Bluetooth filter in the absence of RF interference.


# vB.0.3 - Power Diagnostics & SOH System (2026-05-26)
-------------------------------------------------------------------------------
- [POWER] Implementation of SOH (State of Health) algorithm based on time integration (Coulomb Counting): the battery is continuously measured during discharge within safe thresholds (4.15V max, 3.30V minimum for capacity calculation, 3.15V cutoff threshold).
- [POWER] Integration of emergency Safe-Save into NVS memory for accumulated current upon reaching the critical threshold of 3.30V, protecting data against forced interruption.
- [POWER] Telemetry stabilization through temporal averaging (20 ADC samples accumulated over one second - 50ms), providing extremely stable voltage and current values.
- [POWER] Update of battery percentage estimation based on a linear model strictly confined within the real usable operating window (3.15V - 4.15V).
- [UI/UX] Architectural rewrite of the Power Diagnostics page (`pwr_page.cpp`) into a scrollable list-style Viewport, perfectly aligned visually with DevSet menus and MP3 List.
- [UI/UX] Full hardware support integration for Power Diagnostics: unified use of `footer_manager` enabling navigation via physical buttons BtnA (`</DN>`), BtnB (`UP`), and BtnC (`EXIT`).
- [SYSTEM] Default Battery Capacity adjusted from 1000mAh to 500mAh in GlobalConfig.
- [SYSTEM] Automatic SOH reset (clearing `batt_measured_cap`) when the user changes the declared value `batt_def_cap` from the system settings menu.


v0.32.2 - BT Audio Engine & UI Smart Refinements (2026-05-25)
-------------------------------------------------------------------------------

- [BT AUDIO] Implementation of exclusive BT-only mode: direct and clean boot of the MP3 engine combined with the ESP32-A2DP stack, completely bypassing missing ES8388 hardware dependencies (I2S/I2C).
- [UI/UX] Fix of graphical artifacts in the virtual keypad when exiting the Power Diagnostics screen by implementing viewport cleanup during page transitions.
- [UI/UX] Navigation consistency improvement: returning (BACK) from BT lists (Scan / Saved) is now handled consistently via long-press on BtnA, matching the rest of the application.
- [UI/UX] Alignment of scroll directions in MP3 List to match the new global standard (BtnA = Down, BtnC = Up), including footer update.
- [UI/UX] Extreme Smart Refresh optimization on the Power Diagnostics screen: battery icon redraw uses "fill + remainder" technique (no background erase), eliminating flicker completely.
- [UI/UX] Power Header improvement: if USB is disconnected, the system dynamically displays real battery current (negative, orange) instead of frozen USB values.
- [UI/UX] Boot with `Auto MP3 = ON` or in hardware `BT-Only` mode now directly shows the clean "MP3player" splash instead of keeping the user in the unnecessary "Choose" menu.
- [BUGFIX] Complete removal of I2C "NACK" and `Read failed 0x33` error flood in the serial console when entering DevSet settings without the physical audio module (bridge guards `g_has_audio_module` added on `getHPMode`).
- [BUGFIX] Fixed "UNLICENSED FEATURE" screen where the first line used incorrect font size (size 1 instead of size 2).
- [SYSTEM] Global Debounce engine rewritten for Touch and physical buttons interaction using a stable time-based filter (40ms), eliminating false double clicks caused by strong BT RF emissions.
