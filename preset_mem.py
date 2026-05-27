import serial
import time

# --- CONFIGURARE PORT SERIAL ---
PORT = "COM11"         # Schimbați cu portul COM corect al aparatului dvs.
BAUDRATE = 115200      # Viteza serială standard a M5DSP
TIMEOUT = 0.5          # Timpul de așteptare pentru răspuns serial (secunde)

def run_nvs_populator():
    # 1. Inițializare comenzi distincte și corecte pentru VOICE (Slot 0-3)
    voice_commands = [
        # Slot 0 - USER VOICE (Valori standard)
        "V0LC200", "V0HC3400", "V0SL1", "V0NR1", "V0NA3.0", "V0VS0",
        # Slot 1 - VOICE Preset 1 (Spectru larg, NR off)
        "V1LC150", "V1HC4000", "V1SL0", "V1NR0", "V1NA4.5", "V1VS1",
        # Slot 2 - VOICE Preset 2 (BPF mediu, NR mediu)
        "V2LC300", "V2HC2800", "V2SL2", "V2NR1", "V2NA5.0", "V2VS0",
        # Slot 3 - VOICE Preset 3 (BPF îngust de comunicație, NR agresiv)
        "V3LC400", "V3HC2200", "V3SL3", "V3NR1", "V3NA7.5", "V3VS1"
    ]

    # 2. Inițializare comenzi distincte și corecte pentru CW (Slot 0-3)
    # Rețineți că în v0.28.2, parametrii 2D și 3D se exclud reciproc:
    # Setarea uneia la valoare > 0 va seta automat cealaltă la 0 în firmware.
    cw_commands = [
        # Slot 0 - USER CW (Frecvență standard de 650Hz, Delay 2D activ la 15 ms, 3D dezactivat)
        "C0FC650", "C0BW500", "C0SL1", "C0NR0", "C0NA3.0", "C0VS0", "C0MS1", "C02D15",
        # Slot 1 - CW Preset 1 (Frecvență joasă 550Hz, Filtru îngust, 3D activ la Alpha 5, 2D dezactivat)
        "C1FC550", "C1BW200", "C1SL2", "C1NR1", "C1NA5.5", "C1VS1", "C1MS0", "C13D5",
        # Slot 2 - CW Preset 2 (Frecvență înaltă 700Hz, Filtru mediu, Delay 2D activ la 20 ms)
        "C2FC700", "C2BW100", "C2SL0", "C2NR1", "C2NA4.0", "C2VS0", "C2MS1", "C22D20",
        # Slot 3 - CW Preset 3 (Frecvență standard 800Hz, Filtru ultra-îngust, 3D activ la Alpha 8)
        "C3FC800", "C3BW50",  "C3SL3", "C3NR0", "C3NA2.0", "C3VS1", "C3MS0", "C33D8"
    ]

    all_commands = voice_commands + cw_commands

    print(f"[!] Se deschide portul serial {PORT} la {BAUDRATE} baud...")
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        print("[*] Se așteaptă 6 secunde pentru finalizarea secvenței de boot a Core2...")
        time.sleep(6.0)  # Așteptăm inițializarea completă și RTC Sync
        
        # Curățăm bufferul de orice loguri de boot reziduale
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print("[+] Conexiune serială pregătită și buffer curățat!")
    except Exception as e:
        print(f"[-] EROARE: Nu s-a putut deschide portul serial {PORT}. Detalii: {e}")
        return

    # Forțăm trecerea în modul MACHINE pentru procesarea corectă a comenzilor compacte
    print("[!] Se trimite comanda de comutare în modul MACHINE (SPRO1)...")
    ser.write(b"SPRO1\n")
    time.sleep(1.0)  # Așteptăm 1.0 secundă pentru switch complet de protocol
    
    # Citim confirmarea switch-ului de mod
    response = ser.readline().decode('utf-8', errors='ignore').strip()
    print(f"[Aparat Mod]: {response}")

    success_count = 0
    total_commands = len(all_commands)

    print(f"\n[i] Începe popularea rapidă a memoriilor cu {total_commands} comenzi...")
    print("-" * 60)

    for idx, cmd in enumerate(all_commands, 1):
        raw_to_send = f"{cmd}\n"
        print(f"[{idx}/{total_commands}] Se trimite: {cmd.strip()}", end="", flush=True)
        
        # Trimite comanda
        ser.write(raw_to_send.encode('utf-8'))
        
        # Așteaptă Răspunsul specific pentru această comandă
        expected_ack = f"!{cmd}~ACK"
        found_ack = False
        start_time = time.time()
        
        while (time.time() - start_time) < TIMEOUT:
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            if not response:
                continue
                
            if response == expected_ack:
                print(f"  --> [OK] Răspuns aparat: {response}")
                success_count += 1
                found_ack = True
                break
            elif "ERR" in response or "NACK" in response:
                print(f"  --> [FAIL] Eroare aparat: {response}")
                found_ack = True
                break
            else:
                # Ignorăm resturile de loguri (ex: [RTC] sau [NVS])
                pass 
                
        if not found_ack:
            print("  --> [TIMEOUT] Nu s-a primit ACK-ul așteptat.")
        
        time.sleep(0.05)  # Mică pauză pentru siguranță

        # Forțăm trecerea în modul Human pentru procesarea corectă a comenzilor compacte
    print("[!] Se trimite comanda de comutare în modul HUMAN (WKM5)...")
    ser.write(b"WKM5\n")
    time.sleep(1.0)  # Așteptăm 1.0 secundă pentru switch complet de protocol
    
    print("-" * 60)
    print(f"[📊] REZUMAT: S-au trimis cu succes {success_count}/{total_commands} comenzi în format Machine Protocol.")
    
    # Închidem portul serial curat
    ser.close()
    print("[+] Portul serial a fost închis.")

if __name__ == "__main__":
    run_nvs_populator()
