# PLANNED IN vB.0.5
--------------------------------------------------------------------------------
- [UI/UX][POWER][SERIAL] Add Device setup item to compensate End of Charge Voltage due to variations in AXP192; add commands in Serial Protocols.
- [UI/UX] Add "NR Lev" on slider carousel.
- [UI/UX] Add function to revert to "Vol" on long press on btnB in Main Viewport.
- [UI/UX] Adjust Battery Icon Charging action appeareance for higher contrast.
- [UI/UX] Reorganise the items in Setup pages & subpages
- [MP3 List] - Add wrap-around (circular) navigation in Tapes and Tracks lists
- [POWER] - SOH (State of Health) for battery: Implement complex determination instead of simple Coulomb Counting.
- [BUGFIX][RTC][I2C_Manager] - Loss of sync at recover from BATT PROTECTION SHUTDOWN
- [BUGFIX][UI/UX] When Screensaver is activated, clock and date are superimposed over the Main Viewport items. When Screensaver is device activated, all OK. 
- [BUGFIX] - other bugs from feedback...


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
