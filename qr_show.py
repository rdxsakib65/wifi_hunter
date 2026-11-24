#!/usr/bin/env python3
"""Show WiFi password + QR code (WIFI:T:WPA;S:ssid;P:pass;;)"""
import sys
import os

def make_wifi_qr(ssid: str, password: str, auth: str = "WPA") -> str:
    # WIFI QR format (Android/iOS standard)
    # escape special chars
    def esc(s):
        return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\:").replace('"', '\\"')
    return f"WIFI:T:{auth};S:{esc(ssid)};P:{esc(password)};;"

def show_qr(ssid: str, password: str, pin: str = None):
    data = make_wifi_qr(ssid or "Unknown", password or "")
    print()
    print("\033[1;32m[+] WiFi Credentials\033[0m")
    if ssid:
        print(f"\033[1;37m    SSID     : \033[1;36m{ssid}\033[0m")
    if pin:
        print(f"\033[1;37m    WPS PIN  : \033[1;33m{pin}\033[0m")
    if password:
        print(f"\033[1;37m    Password : \033[1;32m{password}\033[0m")
    print()
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        # terminal ASCII QR
        print("\033[1;36m[+] Scan this QR to connect:\033[0m")
        print()
        qr.print_ascii(invert=True)
        print()
        # also save png if pillow available
        try:
            from PIL import Image
            img = qr.make_image(fill_color="black", back_color="white")
            out = os.path.join(os.path.expanduser("~"), "wifi_qr.png")
            img.save(out)
            print(f"\033[1;32m[i] QR image saved: {out}\033[0m")
        except Exception:
            pass
    except ImportError:
        print("\033[1;33m[!] Install qrcode for QR display: pip install qrcode pillow\033[0m")
        print(f"\033[1;37m    QR data : {data}\033[0m")
    print()

if __name__ == "__main__":
    # cli: qr_show.py <ssid> <password> [pin]
    ssid = sys.argv[1] if len(sys.argv) > 1 else "TestWiFi"
    password = sys.argv[2] if len(sys.argv) > 2 else "password123"
    pin = sys.argv[3] if len(sys.argv) > 3 else None
    show_qr(ssid, password, pin)
