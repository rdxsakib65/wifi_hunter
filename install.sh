#!/bin/bash
# WiFi Hunter — Auto Installer
echo "[*] Updating..."
apt update -y && apt upgrade -y

echo "[*] Core tools..."
apt install python git -y

echo "[*] Termux API (for WiFi scan without root)..."
pkg install termux-api -y

echo "[*] WiFi attack tools..."
pkg install root-repo -y
pkg update -y
pkg install aircrack-ng reaver -y

echo ""
echo "[+] Done! Run: python wifi_hunter.py"
echo "[!] Also install 'Termux:API' app from F-Droid for WiFi scan"
