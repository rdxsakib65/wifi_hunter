![logo](Logo/Logo.jpeg)

# WiFi Hunter v1.0
> Full WiFi Attack & Recon Suite

**Developer: SAKIB**

---

## Quick Install (Termux)

```bash
apt update -y && apt upgrade -y
apt install python git -y
pkg install termux-api -y
git clone https://github.com/rdxsakib65/wifi_hunter.git
cd WiFi_Hunter
python wifi_hunter.py
```

## WiFi Attack Tools (Root needed)

```bash
pkg install root-repo -y && pkg update -y
pkg install aircrack-ng reaver -y
```

---

## Features
```
[01] WiFi Scanner     → termux-wifi-scaninfo (no root!)
[02] WPS Scanner      → wash
[03] WPS Attack       → reaver / bully (Pixie Dust / PIN)
[04] Handshake Capture→ airodump-ng + auto deauth
[05] Deauth Attack    → aireplay-ng
[06] PMKID Attack     → hcxdumptool
[07] Password Cracker → aircrack-ng / hashcat
[08] Evil Twin AP     → hostapd + dnsmasq
[09] Network Monitor  → airodump-ng
[10] WEP Crack        → ARP replay + aircrack
[11] Check Tools      → dependency status
```

---

## WiFi Scanner — No Root Needed!

Install **Termux:API** from F-Droid, then:
```bash
pkg install termux-api -y
```
Scanner will show all nearby networks automatically.

---

## Save Output

```bash
cp *.cap ~/storage/shared
cp *.json ~/storage/shared
```

---

## Legal Notice
> Authorized testing only. Developer not responsible for misuse.

**WiFi Hunter v1.0 · SAKIB**
