![logo](Logo/Logo.jpeg)

# WiFi Hunter v1.0
> Full WiFi Attack & Recon Suite for Termux

---

## Developer
**SAKIB**

---

## Features

```
[01] WiFi Scanner          — iw / iwlist full network scan
[02] WPS Scanner           — wash WPS network discovery
[03] WPS Attack            — Pixie Dust · PIN Brute · Null PIN (reaver/bully)
[04] Handshake Capture     — airodump-ng + auto deauth
[05] Deauth Attack         — aireplay-ng broadcast/targeted
[06] PMKID Attack          — hcxdumptool capture + hashcat convert
[07] Password Cracker      — aircrack-ng + hashcat
[08] Evil Twin AP          — hostapd + dnsmasq fake AP
[09] Network Monitor       — full channel airodump-ng
[10] WEP Crack             — IVs + ARP replay + aircrack
[11] Dependency Checker    — verify all tools installed
```

---

## Install (Termux)

```bash
apt update -y && apt upgrade -y
apt install python git -y
termux-setup-storage

# Install WiFi tools
pkg install aircrack-ng reaver bully hcxdumptool hcxtools iw hashcat

# Clone
git clone https://github.com/rdxsakib65/wifi_hunter.git
cd WiFi-Hunter
python wifi_hunter.py
```

---

## Root Required

Most WiFi attack modules need root access.

```bash
# With tsu (Termux su)
pkg install tsu
tsu
python wifi_hunter.py
```

---

## Save Output

```bash
cp *.cap ~/storage/shared
cp *.json ~/storage/shared
cp *.log ~/storage/shared
```

---

## Legal Notice

> For authorized security testing only.
> Do not attack networks you don't own.
> Developer not responsible for misuse.

---

**WiFi Hunter v1.0** ·SAKIB