import serial
import serial.tools.list_ports
import time
import re
import sys

def select_port():
    while True:
        ports = list(serial.tools.list_ports.comports())
        print("\n--- Available Serial Ports ---")
        if not ports:
            print("No serial ports found!")
        else:
            for idx, p in enumerate(ports, 1):
                print(f"[{idx}] {p.device} - {p.description}")
        print("-" * 30)
        print("Enter a number to select a port, or type the port name directly (e.g. COM11).")
        print("Type 'r' to rescan, or 'q' to quit.")
        val = input("Selection: ").strip()
        if val.lower() == 'q':
            print("Exiting.")
            sys.exit(0)
        if val.lower() == 'r':
            continue
        if val.isdigit():
            idx = int(val) - 1
            if 0 <= idx < len(ports):
                return ports[idx].device
            else:
                print("Invalid number selection.")
        elif val:
            return val

def get_license_key():
    while True:
        print("\n--- License Key Configuration ---")
        print("Example format: YO3HJV$7*CAF15FED13B57491")
        key = input("Enter license key (or press Enter to skip/leave empty): ").strip()
        if not key:
            print("License key skipped (empty).")
            return ""
        pattern = r"^[A-Za-z0-9/]+\$\d+\*[A-Fa-f0-9]+$"
        if re.match(pattern, key):
            return key
        print("[-] ERROR: Invalid license key format! Please match CALLSIGN$N*HEXSTRING pattern.")

def program_license(ser, key):
    if not key:
        print("[-] ERROR: License key is empty. Please enter a valid license key first.")
        return False
    cmd = f"AUTH::{key}"
    print(f"[!] Sending license command: {cmd}")
    ser.write(f"{cmd}\n".encode('utf-8'))

    print("[*] Waiting for response from device...")
    start_time = time.time()
    response_received = False
    while (time.time() - start_time) < 2.0:
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        if response:
            print(f"[Device Response]: {response}")
            response_received = True
            
    if not response_received:
        print("[?] No response received from device.")
    return response_received

def program_presets(ser):
    voice_commands = [
        # Slot 0 - USER VOICE (Standard values)
        "V0LC200", "V0HC3400", "V0SL1", "V0NR1", "V0NA3.0", "V0VS0",
        # Slot 1 - VOICE Preset 1 (Wide spectrum, NR off)
        "V1LC150", "V1HC4000", "V1SL0", "V1NR0", "V1NA4.5", "V1VS1",
        # Slot 2 - VOICE Preset 2 (Medium BPF, Medium NR)
        "V2LC300", "V2HC2800", "V2SL2", "V2NR1", "V2NA5.0", "V2VS0",
        # Slot 3 - VOICE Preset 3 (Narrow communication BPF, Aggressive NR)
        "V3LC400", "V3HC2200", "V3SL3", "V3NR1", "V3NA7.5", "V3VS1"
    ]

    cw_commands = [
        # Slot 0 - USER CW (Standard frequency 650Hz, Delay 2D active at 15 ms, 3D disabled)
        "C0FC650", "C0BW500", "C0SL1", "C0NR0", "C0NA3.0", "C0VS0", "C0MS1", "C02D15",
        # Slot 1 - CW Preset 1 (Low frequency 550Hz, Narrow filter, 3D active at Alpha 5, 2D disabled)
        "C1FC550", "C1BW200", "C1SL2", "C1NR1", "C1NA5.5", "C1VS1", "C1MS0", "C13D5",
        # Slot 2 - CW Preset 2 (High frequency 700Hz, Medium filter, Delay 2D active at 20 ms)
        "C2FC700", "C2BW100", "C2SL0", "C2NR1", "C2NA4.0", "C2VS0", "C2MS1", "C22D20",
        # Slot 3 - CW Preset 3 (Standard frequency 800Hz, Ultra-narrow filter, 3D active at Alpha 8)
        "C3FC800", "C3BW50",  "C3SL3", "C3NR0", "C3NA2.0", "C3VS1", "C3MS0", "C33D8"
    ]

    all_commands = voice_commands + cw_commands
    
    print("[!] Sending command to switch to MACHINE mode (SPRO1)...")
    ser.write(b"SPRO1\n")
    time.sleep(1.0)
    
    response = ser.readline().decode('utf-8', errors='ignore').strip()
    print(f"[Device Mode]: {response}")

    success_count = 0
    total_commands = len(all_commands)

    print(f"\n[i] Starting preset programming with {total_commands} commands...")
    print("-" * 60)

    for idx, cmd in enumerate(all_commands, 1):
        raw_to_send = f"{cmd}\n"
        print(f"[{idx}/{total_commands}] Sending: {cmd}", end="", flush=True)
        ser.write(raw_to_send.encode('utf-8'))
        
        expected_ack = f"!{cmd}~ACK"
        found_ack = False
        start_time = time.time()
        
        while (time.time() - start_time) < 0.5:
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            if not response:
                continue
            if response == expected_ack:
                print(f"  --> [OK] Device response: {response}")
                success_count += 1
                found_ack = True
                break
            elif "ERR" in response or "NACK" in response:
                print(f"  --> [FAIL] Device error: {response}")
                found_ack = True
                break
                
        if not found_ack:
            print("  --> [TIMEOUT] Did not receive expected ACK.")
        time.sleep(0.05)

    print("[!] Sending command to switch to HUMAN mode (WKM5)...")
    ser.write(b"WKM5\n")
    time.sleep(1.0)
    
    print("-" * 60)
    print(f"[📊] SUMMARY: Successfully sent {success_count}/{total_commands} commands in Machine Protocol.")
    return success_count == total_commands

def open_serial_connection(port, wait_time=6.0):
    print(f"\n[!] Opening serial port {port} at 115200 baud...")
    try:
        ser = serial.Serial(port, 115200, timeout=1.0)
        print(f"[*] Waiting {wait_time} seconds for connection to stabilize / boot...")
        time.sleep(wait_time)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print("[+] Serial connection ready!")
        return ser
    except Exception as e:
        print(f"[-] ERROR: Could not open serial port {port}. Details: {e}")
        return None

def main():
    print("=== M5DSP Interactive Configuration Script (vB.0.4) ===")
    port = select_port()
    license_key = get_license_key()
    
    while True:
        print("\n=================== M5DSP vB.0.4 ===================")
        print(f"Active Serial Port: {port}")
        print(f"Active License Key: {license_key if license_key else '[None Entered]'}")
        print("----------------------------------------------")
        print("[1] Program License and Presets")
        print("[2] Program License")
        print("[3] Program Presets")
        print("[4] Change Serial Port")
        print("[5] Exit")
        print("==============================================")
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            if not license_key:
                print("\nLicense key is currently empty.")
                license_key = get_license_key()
                if not license_key:
                    print("Aborted since license key is empty.")
                    continue
            
            ser = open_serial_connection(port, wait_time=6.0)
            if ser:
                try:
                    print("\n--- Phase 1: Programming License ---")
                    program_license(ser, license_key)
                    time.sleep(1.0)
                    print("\n--- Phase 2: Programming Presets ---")
                    program_presets(ser)
                finally:
                    ser.close()
                    print("[+] Serial port closed.")
                    
        elif choice == '2':
            if not license_key:
                print("\nLicense key is currently empty.")
                license_key = get_license_key()
                if not license_key:
                    print("Aborted since license key is empty.")
                    continue
                    
            ser = open_serial_connection(port, wait_time=2.0)
            if ser:
                try:
                    program_license(ser, license_key)
                finally:
                    ser.close()
                    print("[+] Serial port closed.")
                    
        elif choice == '3':
            ser = open_serial_connection(port, wait_time=6.0)
            if ser:
                try:
                    program_presets(ser)
                finally:
                    ser.close()
                    print("[+] Serial port closed.")
                    
        elif choice == '4':
            port = select_port()
            print(f"Changed active port to: {port}")
            
        elif choice == '5':
            print("Exiting script. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
