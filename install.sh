#!/bin/bash
# WiFi Hunter — Auto Installer for Termux
echo "[*] Updating packages..."
apt update -y && apt upgrade -y

echo "[*] Installing Python & Git..."
apt install python git -y

echo "[*] Installing WiFi tools..."
pkg install aircrack-ng reaver bully hcxdumptool hcxtools iw hashcat -y

echo "[*] Installing optional tools..."
pkg install hostapd dnsmasq -y 2>/dev/null

echo "[+] Done. Run: python wifi_hunter.py"
