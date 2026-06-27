import serial
import serial.tools.list_ports
import time

# --- CONFIGURATION ---
BAUDRATE = 115200      # Standard serial speed for M5DSP
TIMEOUT = 1.0          # Timeout for serial response (seconds)

# --- PRESET COMMANDS DEFINITIONS ---
VOICE_COMMANDS = [
    # Slot 0 - USER VOICE (Standard values)
    "V0LC200", "V0HC3400", "V0SL1", "V0NR1", "V0NA3.0", "V0VS0",
    # Slot 1 - VOICE Preset 1 (Wide spectrum, NR off)
    "V1LC150", "V1HC4000", "V1SL0", "V1NR0", "V1NA4.5", "V1VS1",
    # Slot 2 - VOICE Preset 2 (Medium BPF, Medium NR)
    "V2LC300", "V2HC2800", "V2SL2", "V2NR1", "V2NA5.0", "V2VS0",
    # Slot 3 - VOICE Preset 3 (Narrow communication BPF, Aggressive NR)
    "V3LC400", "V3HC2200", "V3SL3", "V3NR1", "V3NA7.5", "V3VS1"
]

CW_COMMANDS = [
    # Slot 0 - USER CW (Standard frequency 650Hz, Delay 2D active at 15 ms, 3D disabled)
    "C0FC650", "C0BW500", "C0SL1", "C0NR0", "C0NA3.0", "C0VS0", "C0MS1", "C02D15",
    # Slot 1 - CW Preset 1 (Low frequency 550Hz, Narrow filter, 3D active at Alpha 5, 2D disabled)
    "C1FC550", "C1BW200", "C1SL2", "C1NR1", "C1NA5.5", "C1VS1", "C1MS0", "C13D5",
    # Slot 2 - CW Preset 2 (High frequency 700Hz, Medium filter, Delay 2D active at 20 ms)
    "C2FC700", "C2BW100", "C2SL0", "C2NR1", "C2NA4.0", "C2VS0", "C2MS1", "C22D20",
    # Slot 3 - CW Preset 3 (Standard frequency 800Hz, Ultra-narrow filter, 3D active at Alpha 8)
    "C3FC800", "C3BW50",  "C3SL3", "C3NR0", "C3NA2.0", "C3VS1", "C3MS0", "C33D8"
]

ALL_PRESETS = VOICE_COMMANDS + CW_COMMANDS

def select_serial_port():
    print("\n--- Serial Port Selection ---")
    ports = list(serial.tools.list_ports.comports())
    if ports:
        print("Detected serial ports:")
        for idx, p in enumerate(ports, 1):
            print(f"  {idx}. {p.device} ({p.description})")
        print(f"  {len(ports) + 1}. Manual entry")
        
        while True:
            choice = input(f"Select a port (1-{len(ports) + 1}): ").strip()
            if not choice:
                continue
            if choice.isdigit():
                val = int(choice)
                if 1 <= val <= len(ports):
                    return ports[val - 1].device
                elif val == len(ports) + 1:
                    break
            else:
                # If they typed the port name directly
                return choice
            print("Invalid choice, please select a valid option.")
            
    # Fallback to manual entry
    while True:
        port = input("Enter serial port name (e.g. COM11 or /dev/ttyUSB0): ").strip()
        if port:
            return port

def show_menu():
    print("\n" + "="*50)
    print("                 M5DSP PROGRAMMER MENU")
    print("="*50)
    print("  1. Program presets only")
    print("  2. Program presets & license key")
    print("  3. Program license key only")
    print("  4. Exit")
    print("="*50)
    while True:
        choice = input("Select an option (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            return int(choice)
        print("Invalid selection. Please choose 1, 2, 3, or 4.")

def send_command(ser, cmd, expected_ack=None, check_contains=None, timeout=TIMEOUT, verbose=True):
    """
    Sends a command to the serial interface, reads lines to check for expected responses.
    """
    # Clear anything in the input buffer to ensure we read fresh responses
    ser.reset_input_buffer()
    
    raw_cmd = f"{cmd}\n"
    if verbose:
        print(f"Sending command: {cmd.strip()}...", end="", flush=True)
    ser.write(raw_cmd.encode('utf-8'))
    
    start_time = time.time()
    last_response = ""
    while (time.time() - start_time) < timeout:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue
        
        last_response = line
        if expected_ack and line == expected_ack:
            if verbose:
                print(" [OK]")
            return True, line
        if check_contains and check_contains in line:
            if verbose:
                print(" [OK]")
            return True, line
        if "ERR" in line or "NACK" in line or "FAILED" in line:
            if verbose:
                print(f" [FAIL] ({line})")
            return False, line
            
    # If no specific validation string was requested, treat as successful transmission
    if not expected_ack and not check_contains:
        if verbose:
            print(" [SENT]")
        return True, last_response
        
    if verbose:
        print(" [TIMEOUT]")
    return False, f"TIMEOUT (Last response: {last_response})"

def run_programmer():
    # 1. Select and connect to the serial port (retry on failure)
    while True:
        port = select_serial_port()
        print(f"\n[!] Opening serial port {port} at {BAUDRATE} baud...")
        try:
            ser = serial.Serial(port, BAUDRATE, timeout=TIMEOUT)
            print("[*] Waiting 6 seconds for Core2 boot sequence (reset triggered by port opening)...")
            time.sleep(6.0)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print("[+] Serial connection ready and buffer cleared!")
            break
        except Exception as e:
            print(f"[-] ERROR: Failed to open serial port {port}. Details: {e}")
            print("[*] Port connection failed. Please select the port again.\n")
            print("="*50)
            
    try:
        # 2. Get menu option
        choice = show_menu()
        if choice == 4:
            print("Exiting...")
            return
            
        # 3. Request license key if Option 2 or 3 is chosen
        license_key = ""
        if choice in [2, 3]:
            while True:
                license_key = input("\nEnter license key (starting with 'AUTH:', e.g., AUTH:CALL$TIER*KEY): ").strip()
                if not license_key:
                    continue
                if not license_key.startswith("AUTH:"):
                    print("Error: The license key must start with 'AUTH:'. Please try again.")
                    continue
                break
        # 5. Initialize Machine Protocol (SPRO1) once
        print("\n[!] Establish Serial Link...", end="", flush=True)
        # Check contains '!SPRO1~ACK' to verify mode switch
        success, resp = send_command(ser, "SPRO1", check_contains="!SPRO1~ACK", verbose=False)
        if success:
            print(" Link Established")
        else:
            print(" Failed")
            print(f"[*] Note: Machine protocol initialization response: {resp}")
            
        time.sleep(0.5)
        
        # 6. Execute selected option logic
        presets_success = True
        # Option 1 or 2: Program presets
        if choice in [1, 2]:
            print(f"\n[!] Programming {len(ALL_PRESETS)} presets: ", end="", flush=True)
            for idx, cmd in enumerate(ALL_PRESETS, 1):
                expected = f"!{cmd}~ACK"
                ok, resp = send_command(ser, cmd, expected_ack=expected, verbose=False)
                if ok:
                    print(".", end="", flush=True)
                else:
                    status_lbl = " [TIMEOUT]" if "TIMEOUT" in resp else " [FAIL]"
                    print(f"{status_lbl}\n\n[-] ERROR: Command '{cmd}' failed. Response: {resp}")
                    print("[-] Programming aborted.")
                    presets_success = False
                    break
                time.sleep(0.05)
            if presets_success:
                print(" [OK]")
                print(f"[📊] SUMMARY: Successfully programmed all {len(ALL_PRESETS)} presets.")
            
        # Option 2 or 3: Program license key
        if presets_success and choice in [2, 3]:
            print(f"\n[!] Programming license key: {license_key}...")
            # Expect #AUTH: response
            ok, resp = send_command(ser, license_key, check_contains="#AUTH:")
            
            if ok and "OK" in resp:
                print("[+] License key accepted!")
            else:
                print(f"[-] License key programming failed. Response: {resp}")
                
    finally:
        ser.close()
        print("\n[+] Serial port closed.")
        if 'choice' in locals() and choice != 4:
            print("HaM5dsp will reboot now.")

if __name__ == "__main__":
    run_programmer()
