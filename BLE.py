import serial
import serial.tools.list_ports
import time
import re
import sys

BAUDRATE = 9600  # doit correspondre au HC-05

def trouver_port_bluetooth():
    ports = list(serial.tools.list_ports.comports())
    candidats = []

    for p in ports:
        desc = p.description.upper()
        if any(keyword in desc for keyword in ["HC", "BLUETOOTH", "STANDARD SERIAL", "SPP"]):
            # extraire le numéro de port COM
            match = re.search(r'COM(\d+)', p.device, re.IGNORECASE)
            if match:
                candidats.append((int(match.group(1)), p.device))

    if not candidats:
        print("❌ Aucun port Bluetooth détecté.")
        print("Ports disponibles :", [p.device for p in ports])
        return None

    # tri par numéro de COM croissant → on prend le plus grand
    candidats.sort(key=lambda x: x[0])
    port_final = candidats[-1][1]
    print(f"→ Ports Bluetooth détectés : {[c[1] for c in candidats]}")
    print(f"✅ Sélection automatique du port le plus récent : {port_final}")
    return port_final


def ouvrir_connexion():
    port = trouver_port_bluetooth()
    if not port:
        sys.exit(1)

    try:
        ser = serial.Serial(port, BAUDRATE, timeout=1)
        print(f"✅ Connecté au port {port}")
        return ser
    except serial.SerialException as e:
        print(f"Erreur : {e}")
        sys.exit(1)


def envoyer_commande(ser, cmd):
    if not ser.is_open:
        print("Port série fermé.")
        return
    ser.write((cmd + "\r\n").encode())
    print(f"Commande envoyée : {cmd}")
    time.sleep(0.1)

    # Lecture éventuelle d'une réponse du STM32 (optionnel)
    reponse = ser.readline().decode(errors='ignore').strip()
    if reponse:
        print("↩ Réponse STM32 :", reponse)


if __name__ == "__main__":
    ser = ouvrir_connexion()
    try:
        while True:
            cmd = input("Entrer commande (ex: A000, B000, C012, q pour quitter): ").strip()
            if cmd.lower() == 'q':
                break
            envoyer_commande(ser, cmd)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("Connexion fermée.")
