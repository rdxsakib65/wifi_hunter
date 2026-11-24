#!/data/data/com.termux/files/usr/bin/bash

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${GREEN}[+] Setting up local WiFi_Hunter environment...${RESET}"

echo -e "${GREEN}[+] Installing Python dependencies...${RESET}"
pip install -r requirements.txt --break-system-packages

chmod +x main.py

echo -e "${GREEN}[+] Setting up 'wifi_hunter' command...${RESET}"

BIN_DIR="$PREFIX/bin"
WIFI_HUNTER_BIN="$BIN_DIR/wifi_hunter"
SCRIPT_DIR="$(pwd)"

cat > "$WIFI_HUNTER_BIN" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd "$SCRIPT_DIR" || exit

# Update Logic
if [ "\$1" == "update" ]; then
    echo -e "\033[1;32m[+] Fetching latest updates from MSR's GitHub...\033[0m"
    git reset --hard HEAD > /dev/null 2>&1
    git pull origin main

    echo -e "\033[1;32m[+] Checking for new requirements...\033[0m"
    pip install -r requirements.txt --break-system-packages > /dev/null 2>&1

    chmod +x main.py

    echo -e "\033[1;32m[+] Re-applying wifi_hunter command setup...\033[0m"
    bash install.sh > /dev/null 2>&1

    echo -e "\033[1;32m[✓] WiFi_Hunter updated successfully!\033[0m"
    exit 0
fi

# Help Logic
if [ "\$1" == "help" ]; then
    python help.py
    exit 0
fi

# Fix Logic
if [ "\$1" == "fix" ]; then
    bash fix.sh
    exit 0
fi

# Contact Logic
if [ "\$1" == "qr" ]; then
    python show_qr.py
    exit 0
fi

if [ "\$1" == "contact" ]; then
    python contact.py
    exit 0
fi

# Menu Logic
if [ "\$1" == "menu" ]; then
    sudo python main.py
    exit 0
fi

# Old Logic
if [ "\$1" == "old" ]; then
    sudo python w1.py -i wlan0 -K
    exit 0
fi

# Run Logic
if [ -z "\$1" ]; then
    sudo python main.py -i wlan0 -K
else
    sudo python main.py "\$@"
fi
EOF

chmod +x "$WIFI_HUNTER_BIN"

echo -e "\n${GREEN}[✓] Local setup complete!${RESET}"

echo -e "\n\033[1;36m╔══════════════════════════════════════════════╗\033[0m"
echo -e "\033[1;36m║           📌  READ THIS CAREFULLY            ║\033[0m"
echo -e "\033[1;36m╚══════════════════════════════════════════════╝\033[0m"
echo -e "\033[1;33m  ⚠️  Take a screenshot of the info below now!\033[0m"
echo -e "\033[1;33m     You may need it later. Save it somewhere.\033[0m"

echo -e "\n\033[1;32m  ┌─ Available Commands ──────────────────────┐\033[0m"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter\033[0m         → Run WiFi_Hunter (main tool)"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter update\033[0m  → Update WiFi_Hunter to latest version"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter help\033[0m    → Show help & usage info"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter fix\033[0m     → Fix root/superuser issues"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter contact | wifi_hunter qr\033[0m → Contact / QR for saved passwords"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter menu\033[0m    → Run WiFi_Hunter interactive menu"
echo -e "\033[1;32m  │\033[0m  \033[1;37mwifi_hunter old\033[0m     → Run WiFi_Hunter old engine (w1.py)"
echo -e "\033[1;32m  └───────────────────────────────────────────┘\033[0m"

echo -e "\n\033[1;31m  ⚡ IMPORTANT — If 'wifi_hunter' shows:\033[0m"
echo -e "\033[1;37m     \"no superuser binary detected\"\033[0m"
echo -e "\033[1;33m  → First try:   \033[1;37mwifi_hunter fix\033[0m"
echo -e "\033[1;33m  → Still broken? Visit this link for 3 fix methods:\033[0m"
echo -e "\033[1;36m     https://github.com/rdxsakib65/fix-termux-root\033[0m"
echo -e "\033[1;33m  → Copy or screenshot that link right now!\033[0m"

echo -e "\n\033[1;36m══════════════════════════════════════════════\033[0m"
echo -e "\033[1;32m  ✅ All done! Type 'wifi_hunter' to get started.\033[0m"
echo -e "\033[1;36m══════════════════════════════════════════════\033[0m\n"
