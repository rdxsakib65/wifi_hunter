#!/usr/bin/env python3
"""
WiFi_Hunter — Show QR for already found passwords
Reads reports / saved credential files and shows QR codes.
No attack logic. Safe extra option only.
"""
import os
import re
import sys

def make_wifi_qr(ssid, password, auth="WPA"):
    def esc(s):
        return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\:").replace('"', '\\"')
    return f"WIFI:T:{auth};S:{esc(ssid)};P:{esc(password)};;"

def print_ascii_qr(data):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        return True
    except Exception:
        print("  (install: pip install qrcode pillow)")
        print("  QR data:", data)
        return False

def parse_file(path):
    """Parse common credential file formats."""
    creds = []
    try:
        text = open(path, "r", encoding="utf-8", errors="ignore").read()
    except Exception:
        return creds
    # block format
    blocks = re.split(r'\n\s*\n', text)
    for b in blocks:
        ssid = re.search(r'(?:ESSID|SSID|AP SSID)\s*[:=]\s*[\'"]?(.+?)[\'"]?\s*$', b, re.I | re.M)
        psk  = re.search(r'(?:WPA PSK|Password|PSK|KEY)\s*[:=]\s*[\'"]?(.+?)[\'"]?\s*$', b, re.I | re.M)
        pin  = re.search(r'(?:WPS PIN|PIN)\s*[:=]\s*[\'"]?(\d{4,8})[\'"]?', b, re.I | re.M)
        if psk:
            creds.append({
                "ssid": (ssid.group(1).strip() if ssid else "Unknown"),
                "password": psk.group(1).strip(),
                "pin": pin.group(1) if pin else None,
                "file": path
            })
    # single line csv-ish
    for line in text.splitlines():
        if ";" in line and len(line.split(";")) >= 3:
            parts = [p.strip() for p in line.split(";")]
            # try BSSID;ESSID;PIN;PSK
            if len(parts) >= 4 and parts[3]:
                creds.append({"ssid": parts[1] or "Unknown", "password": parts[3], "pin": parts[2] if parts[2].isdigit() else None, "file": path})
    return creds

def find_cred_files():
    home = os.path.expanduser("~")
    candidates = []
    search_dirs = [
        os.getcwd(),
        os.path.join(os.getcwd(), "reports"),
        os.path.join(home, ".BiRi", "sessions"),
        os.path.join(home, ".BiRi", "pixiewps"),
        os.path.join(home, "WiFi_Hunter", "reports"),
    ]
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith((".txt", ".csv", ".log")):
                    candidates.append(os.path.join(root, f))
    return candidates

def main():
    print("\033[1;36m")
    print("  WIFI — Saved Password QR Viewer")
    print("  by SAKIB GAMING")
    print("\033[0m")
    files = find_cred_files()
    all_creds = []
    for f in files:
        all_creds.extend(parse_file(f))
    # dedupe by ssid+password
    seen = set()
    unique = []
    for c in all_creds:
        key = (c["ssid"], c["password"])
        if key not in seen and c["password"]:
            seen.add(key)
            unique.append(c)
    if not unique:
        print("\033[1;33m[!] No saved passwords found yet.\033[0m")
        print("    Run an attack first. Credentials usually save under ./reports or ~/.BiRi/")
        print()
        # allow manual entry
        print("Manual entry:")
        ssid = input("  SSID     : ").strip()
        password = input("  Password : ").strip()
        if password:
            unique.append({"ssid": ssid or "Unknown", "password": password, "pin": None, "file": "manual"})
        else:
            return
    print(f"\033[1;32m[+] Found {len(unique)} password(s)\033[0m\n")
    for i, c in enumerate(unique, 1):
        print(f"  {i}) {c['ssid']}  →  {c['password']}")
    print()
    choice = input("Select number (or Enter = all): ").strip()
    if choice.isdigit():
        idxs = [int(choice) - 1]
    else:
        idxs = list(range(len(unique)))
    for i in idxs:
        if i < 0 or i >= len(unique):
            continue
        c = unique[i]
        print("\n" + "─" * 40)
        print(f"\033[1;37mSSID     : \033[1;36m{c['ssid']}\033[0m")
        if c.get("pin"):
            print(f"\033[1;37mWPS PIN  : \033[1;33m{c['pin']}\033[0m")
        print(f"\033[1;37mPassword : \033[1;32m{c['password']}\033[0m")
        print()
        data = make_wifi_qr(c["ssid"], c["password"])
        print("\033[1;36m[+] Scan QR to connect:\033[0m\n")
        print_ascii_qr(data)
        print()

if __name__ == "__main__":
    main()
