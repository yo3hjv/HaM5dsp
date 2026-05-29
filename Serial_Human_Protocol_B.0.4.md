# M5DSP – Serial Commands (Serial Commands Reference)

**Version:** M5DSP vB.0.4.d | **Last update:** 2026-05-29  
**Platform:** M5Stack Core2 + ModuleAudio (ES8388) DSP Pipeline  
**Baud rate:** 115200

---

## COMMAND LIST (Alphabetical Quick Reference)

```text
--------------------------------------------------------------------------------
Command         Min/Max Values      Short Description
--------------------------------------------------------------------------------
balance N       -100 - 100          Stereo balance DSP. ARG
batv            -                   Battery telemetry. ACTION
bypassoff       -                   Disable DSP bypass. ACTION
bypasson        -                   Enable full bypass. ACTION
cw              -                   Enable CW live mode. ACTION
cw2d N          1 - 25              Set CW 2D delay. ARG
cw2doff         -                   Disable CW 2D. ACTION
cw2don          -                   Enable CW 2D. ACTION
cw3d N          1 - 10              Set CW 3D depth. ARG
cw3doff         -                   Disable CW 3D. ACTION
cw3don          -                   Enable CW 3D. ACTION
cwagcoff        -                   Disable CW AGC. ACTION
cwagcon         -                   Enable CW AGC. ACTION
cwbw N          25 - 1000           Set CW BPF bandwidth. ARG
cwcenter        400 - 900           Set CW BPF center frequency. ARG
cwconfidence N   0 - 10              Adjust CW robust threshold. ARG
cwmaxwpm N      12 - 60             Set maximum CW speed. ARG
cwminwpm N      5 - 20              Set minimum CW speed. ARG
cwnoisefloor    -                   Show CW noise floor. ACTION
cwsamplesg1 N   64 - 512            Set Goertzel samples 1. ARG
cwsamplesg2 N   128 - 2048          Set Goertzel samples 2. ARG
displayspace N  0 / 1 / 2           Change Display Space page. ARG
dump            -                   Show DSP and NVS status. ACTION
dumpall         -                   Run all dumps. ACTION
dumpaxp         -                   Dump AXP192 registers. ACTION
dumpes          -                   Dump ES8388 registers. ACTION
fftfloor N      0.0 - 10.0          Set FFT floor level. ARG
fftrange N      0.1 - 10.0          Set FFT dynamic range. ARG
fftspanv N      500 - 8000          Set VOICE FFT span. ARG
hapton/off      -                   Haptic global ON/OFF. ON/OFF
haptlong        -                   Trigger long vibration. ACTION
haptlong N      10 - 2000           Set long vibration duration. ARG
haptshort       -                   Trigger short vibration. ACTION
haptshort N     10 - 1000           Set short vibration duration. ARG
help            -                   Show command list. ACTION
hicut N         1200 - 10500        Set VOICE Hi-cut filter. ARG
hpinfo N        -                   Show headphone jack status. ACTION
igain N         0 - 8               Set ADC gain. ARG
inatt N         0 - 100             Set DSP input attenuation. ARG
loadmcX         -                   Load CW preset X. ARG
loadmvX         -                   Load VOICE preset X. ARG
lowcut N        25 - 800            Set VOICE low-cut filter. ARG
mallsd          -                   Return number of tapes and tracks on SD card. ACTION
mcurtrack       -                   Show current track index and name. ACTION
mcX2d N         0 / 1 - 25          Set CW preset X 2D delay. ARG
mcX3d N         0 / 1 - 10          Set CW preset X 3D depth. ARG
mcXbw           25 - 1000           Set CW preset X BPF bandwidth. ARG
mcXcf           400 - 900           Set CW preset X BPF center frequency. ARG
mcXslope N      0 - 3               Set CW preset X filter slope. ARG
mode N          0, 1                Set VOICE/CW mode. ARG
mpbal N         -100 / 100          MP3 stereo balance. ARG
mpvol N         0 - 100             MP3 DAC volume. ARG
mute/unmute     -                   Mute/unmute audio. ON/OFF
mvXhicut N      1200 - 10500        Set VOICE preset X Hi-cut. ARG
mvXlowcut N     25 - 800            Set VOICE preset X low-cut. ARG
mvXnragres N    1.0 - 10.0          Set VOICE preset X NR aggressiveness. ARG
mvXnron/off     -                   VOICE preset X NR ON/OFF. ON/OFF
mvXslope N      0 - 3               Set VOICE preset X filter slope. ARG
mvXvas          0 / 1               VOICE preset X VAS. ON/OFF
next            -                   Go to next track in active list. ACTION
nr N            1.0 - 10.0          Set Noise Reduction aggressiveness. ARG
nron/nroff      -                   Noise Reduction live ON/OFF. ON/OFF
pause           -                   Pause/resume playback (Toggle). ACTION
play            -                   Play/resume current track. ACTION
prev            -                   Go to previous track in active list. ACTION
repeat N        0, 1, 2             Set repeat mode (0=OFF, 1=Track, 2=All). ARG
shuffle N       0, 1                Enable/disable shuffle playback. ON/OFF
stop            -                   Stop playback and reset position. ACTION
table           -                   Show number of tracks in active playlist. ACTION
savetomem N     1 - 3               Save current live settings. ARG
scrbr N         0 - 100             Set LCD brightness. ARG
setdate         dd.mm.yy            Set RTC date. ARG
settime         hh:mm:ss            Set RTC time. ARG
slope N         0, 1, 2, 3          Set VOICE live filter slope. ARG
theme N         0 / 1 / 3           Change theme. ARG
time            -                   Show local and UTC date/time. ACTION
timezone N      -12 - 14            Set UTC offset. ARG
tonetest M      off/l/r/both        Activate 1kHz test tone. ARG
usercw          -                   Return to manual CW live. ACTION
uservoice       -                   Return to manual VOICE live. ACTION
vashang N       50 - 2000           Set VAS hang time. ARG
vasoff          -                   Disable VAS live. ACTION
vason           -                   Enable VAS live. ACTION
vaswin N        0.001 - 0.5         Set VAS detection threshold. ARG
voice           -                   Enable VOICE live mode. ACTION
vol/gain N      0 - 100             Set unified audio volume. ARG
--------------------------------------------------------------------------------
```

## FUNCTIONAL DESCRIPTION BY SECTION (HUMAN PROTOCOL)

### OPERATING MODE & LIVE STATE (User mode)

```text
mode 0          Set VOICE mode (HPF + LPF voice filtering).
mode 1          Set CW mode (bandpass filter around CW frequency).
voice           Direct alias: activate VOICE mode (User live).
cw              Direct alias: activate CW mode (User live).
uservoice       Return to manual VOICE live control (User mode), leaving the active preset.
usercw          Return to manual CW live control (User mode), leaving the active preset.
When changing mode, live settings are automatically saved/loaded from NVS.
```

### VOICE FILTER (mode 0, User live)

```text
lowcut N        High-pass (Low-cut) live frequency in Hz. Range: 25 – 800 Hz.
hicut N         Low-pass (Hi-cut) live frequency in Hz. Range: 1200 – 10500 Hz.
slope N         Live filter slope: 0=Soft, 1=Medium (24dB), 2=Abrupt, 3=Bypass.
```

### CW & SPATIAL FILTER (mode 1, User live)

```text
cwcenter N      CW BPF center frequency live in Hz. Range: 400 – 900 Hz.
cwbw N          CW BPF bandwidth live in Hz. Range: 25 – 1000 Hz.
cw2don          Enable 2D spatial processing (Spatial Delay).
cw2doff         Disable 2D spatial processing.
cw2d N          Set 2D live delay in ms. Range: 1 – 25 ms.
cw3don          Enable 3D spatial processing (Spectral Depth).
cw3doff         Disable 3D spatial processing.
cw3d N          Set live 3D spectral coefficient. Range: 1 – 10 (Alpha factor).
cwagcon         Enable CW decoder local AGC.
cwagcoff        Disable CW decoder local AGC.
cwthr [N]       Set/show CW spectral detection threshold. Range: 1 – 100 (Default: 32).
                *Effect:* Determines decode sensitivity. Low values (10-20) increase
                sensitivity for weak signals but may produce noise artifacts. High values
                (50-70) decode only strong/clean signals and reduce noise errors.
cwdelta [N]     Set/show CW detection hysteresis margin. Range: 1 – 100 (Default: 32).
                *Physical effect & tuning guide:*
                - Optimal value (25-40): Enables smooth decoding. Keeps the tone "active"
                  through rapid fading (QSB) during a Dah, but returns quickly to "inactive"
                  in the gaps between characters.
                - Too low (1-15): The system becomes unstable on small signal oscillations,
                  fragmenting or "splitting" a continuous Dah into multiple short, unreadable Dits.
                - Too high (60-90): The system stays "hung" in the active state even after the
                  tone stops, merging letters and spaces into one long continuous tone.
```

### MP3 PLAYER CONTROLS & EFFECTS (v0.23.0+)

```text
mpvol N         MP3 DAC output volume in mode MP3 (0–100 %).
mpbal N         MP3 stereo balance (-100 = left only, 100 = right only).
mp3drc on/off   Enable/disable Dynamic Range Compressor (DRC) / Limiter.
mp3thr N        DRC threshold in dB. Range: -40.0 … 0.0 dB.
mp3gain N       Make-up gain in dB. Range: 0.0 … 12.0 dB.
mp3att N        Attack time in ms for compressor. Range: 1.0 – 100.0 ms.
mp3rel N        Release time in ms for compressor. Range: 10.0 – 1000.0 ms.
```

### MP3 PLAYER TRANSPORT CONTROLS & INFO (v0.26.1+)

```text
play            Start or resume current track playback.
stop            Stop playback completely (reset position to second 0).
pause           Pause or resume playback (Toggle).
next            Go to the next track in the active list.
prev            Go to the previous track in the active list.
repeat N        Set repeat mode: 0=OFF, 1=Track, 2=All.
shuffle N       Enable (1) or disable (0) random track playback.
mallsd          Show total number of tapes (folders) and tracks on the SD card.
table           Show number of tracks in the active playlist.
mcurtrack       Show current track index and active filename.
```

### VOLUME, GAIN & BALANCE (General audio)

```text
vol N           Unified audio volume (DSP + MP3). Range: 0 – 100 %.
balance N       DSP stereo balance. Range: -100 (left only) … 100 (right only).
igain N         Analog ADC gain (PGA) at ES8388 input. Range: 0 – 8.
inatt N         DSP input signal attenuation. Range: 0 – 100 %.
mute            Mute audio output.
unmute          Unmute audio output.
```

### NOISE REDUCTION (Wiener-DD, User live)

```text
nron/nroff      Enable/disable Noise Reduction live (VOICE mode only).
nr N            Noise Reduction aggressiveness live. Range: 1.0 - 10.0.
nrreset         Re-capture background noise (useful after QSY or band change).
```

### FFT / SPECTROGRAM

```text
fftfloor N      FFT floor level. Range: 0.0 - 10.0.
fftrange N      FFT dynamic range. Range: 0.1 - 10.0.
fftspanv N      FFT span frequency in Hz for VOICE mode. Range: 500 - 8000 Hz.
```

### VAS – Voice Activity Squelch (User live)

```text
vason/vasoff    Enable/disable Voice Activity Squelch live.
vaswin N        Live squelch detection threshold. Range: 0.001 – 0.5.
vashang N       Live squelch hold time in ms. Range: 50 – 2000 ms.
```

### SYSTEM / THEMES / DIAGNOSTIC / POWER (v0.27.0)

```text
theme N         Change the interface color theme.
                Values: N = 0 (Dark/Default), 1 (Light), 3 (Military).
                * Theme 2 (Retro Amber) is unmapped/reserved.
displayspace N  Change Display Space page: 0 (Dashboard/Filters), 1 (FFT), 2 (CW Decoder).
                * Without parameter, returns the current active page.
                * Note: Context-aware validation applies (Page 2 is available only in CW mode).
savetomem N     Save current live state (VOICE or CW) to persistent memory slot N (1-3). [NVS]
                * Note: Automatically determines the current context (VOICE/CW) and saves under the mode-specific key.
scrbr N         Set LCD brightness (0 - 100 %). [AXP192 DCDC3]
hapton/off      Enable/disable global haptic feedback.
haptshort       Trigger a short vibration live.
haptlong        Trigger a long vibration live.
haptshort N     Set short vibration duration in ms (10 - 1000). Value is persisted in NVS.
haptlong  N     Set long vibration duration in ms (10 - 2000). Value is persisted in NVS.
dump            Full DSP and NVS parameter status.
dumpaxp         Detailed hex dump of PMIC AXP192 registers.
dumpes          Detailed hex dump of ES8388 codec registers.
dumpall         Execute all dumps sequentially (full diagnostics).
hpinfo          Diagnose headphone jack (OMTP/CTIA standards).
tonetest N      Generate 1kHz calibration tone. N=off, 1=L, 2=R, 3=L+R
time            Show current UTC date/time from RTC.
                * Design note (RTC synchronization): When an external app (Companion App) connects,
                  the local RTC in M5Stack is not queried. The host app owns the more accurate time
                  and sends the exact time to the device using SDAT/SHOU commands. Therefore, no machine-mode
                  time query functions are exposed.
batv            Show battery telemetry in human-friendly format.
                Response: "Battery: [Level]% | Voltage: [Voltage]v | Charging: [YES/NO] | Nominal: [N] mAh | Measured: [M] mAh"
                * Note: This command queries the PMIC AXP192 state. It returns the same
                  parameters as the Machine BATV command (level %, voltage with two decimals,
                  charging flag), supplemented by the nominal capacity (user-defined) and
                  actual measured capacity from Coulomb Counting (stored persistently in NVS).
                * The "Measured" capacity is 0.0 mAh if no full discharge cycle has been completed
                  and saved yet.
```

### EDITING AND DIRECT LOADING OF PRESETS (v0.28.4)

```text
M5DSP supports querying, editing, and directly activating parameters stored in preset memory slots for both operation modes (VOICE and CW), without preloading the slot into DSP.

Slot X mapping:
* X = 1..3     -> The three saved preset memory slots (MV1-3 / MC1-3).
* NOTE: The USER working memory (Slot 0) is no longer loaded generically; dedicated commands 'uservoice' and 'usercw' are used exclusively.

1. Direct preset activation (Load & Apply):
   - For VOICE:
     Command:    loadmvX (where X: 0-3, 0 = Live User, 1-3 = Presets)
     Example:    "loadmv1" -> Load and activate VOICE preset 1.
     Response:   "Loaded and activated VOICE Slot [X] (MV[X])"

   - For CW:
     Command:    loadmcX (where X: 0-3, 0 = Live User, 1-3 = Presets)
     Example:    "loadmc1" -> Load and activate CW preset 1.
     Response:   "Loaded and activated CW Slot [X] (MC[X])"

2. VOICE parameters (MVX presets, X: 1-3):
   mvXlowcut     VOICE preset X Lowcut HPF (Hz, range: 25 - 800)
   mvXhicut      VOICE preset X Hicut LPF (Hz, range: 1200 - 10500)
   mvXslope      VOICE preset X filter slope (range: 0 - 3)
   mvXnron/off   VOICE preset X Noise Reduction on/off (0=OFF, 1=ON)
   mvXnragres    VOICE preset X NR aggressiveness (float, range: 1.0 - 10.0)
   mvXvas        VOICE preset X Voice Activity Squelch (0=OFF, 1=ON)

3. CW parameters (MCX presets, X: 1-3):
   mcXcf         CW preset X BPF center frequency (Hz, range: 400 - 900)
   mcXbw         CW preset X BPF bandwidth (Hz, range: 25 - 1000)
   mcXslope      CW preset X filter slope (range: 0 - 3)
   mcX2d         CW preset X 2D spatial delay (range: 0=OFF, 1 - 25 ms delay)
   mcX3d         CW preset X 3D spatial depth (range: 0=OFF, 1 - 10 alpha factor)

4. Terminal response format (Friendly Human Format):
   - On query (no value sent):
     Example:    "mv1lowcut" -> Response: "MV1-Lowcut: 300 Hz"
     Example:    "mc12d"     -> Response: "MC1-2D Delay: 15 ms"
   - On edit (value sent):
     Example:    "mv1lowcut 300" -> Response: "MV1-Lowcut: 300 Hz Set"
     Example:    "mc12d 0"       -> Response: "MC1-2D Delay: OFF Set"
     Example:    "mc13d 5"       -> Response: "MC1-3D Spatial: Alpha 5 Set"

   * Note: If the edited slot is currently active on the device, the setting is applied live automatically (real-time DSP sync & screen redraw).
```
