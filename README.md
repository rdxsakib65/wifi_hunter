<div align="center">

```
██╗    ██╗██╗███████╗██╗
██║    ██║██║██╔════╝██║
██║ █╗ ██║██║█████╗  ██║
██║███╗██║██║██╔══╝ ██║
╚███╔███╔╝██║██║     ██║
 ╚══╝╚══╝ ╚═╝╚═╝      ╚═╝
```

**WiFi_Hunter v2.0** — WPS Security Auditing Tool for Android / Termux

[![Version](https://img.shields.io/badge/version-2.0-brightgreen)](https://github.com/rdxsakib65/WiFi_Hunter/releases)
[![Platform](https://img.shields.io/badge/platform-Android%20%2F%20Termux-blue)](https://termux.dev)
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=rdxsakib65.wifi_hunter)](https://github.com/rdxsakib65/WiFi_Hunter)

</div>

---

## Overview

WiFi_Hunter is a WPS (Wi-Fi Protected Setup) security auditing tool built for Android devices running Termux. It automates Pixie Dust and Bruteforce attacks against WPS-enabled routers, allowing security researchers and network administrators to evaluate the strength of their own wireless infrastructure.

WiFi_Hunter v2.0 is a complete rewrite of the original v1 engine, introducing a global command system, session management, reporting, improved stability, and a built-in interactive help guide — all optimized for Android / Termux.

> This tool is intended for authorized security testing only. Only use it on networks you own or have explicit permission to test.

---
<div align="center">

[![Support this project](https://img.shields.io/badge/Support%20this%20project-FFD700?style=for-the-badge&logo=ko-fi&logoColor=black)](https://www.supportkori.com/msrsakibur)
 
  <a href="https://youtu.be/Y73jDqTqkxI">
    <img src="https://img.shields.io/badge/wifi_hunter_full_setup_video_tutorial-2EA043?style=for-the-badge&logo=android&logoColor=white" alt="WiFi_Hunter Full Setup Video Tutorial">
  </a><br> </div>

## Requirements

- Android device with root access (Magisk or KernelSU)
- [Termux](https://f-droid.org/en/packages/com.termux/) installed (from fdroid. not from playstore)
- Root-capable WiFi adapter (internal wlan0 or external)

---

## Installation

WiFi_Hunter v2.0 installs globally. Once set up, you can run it from any directory using the `wifi_hunter` command.

### Method 1 — One Command (Recommended)

```bash
curl -sLo installer.sh https://raw.githubusercontent.com/rdxsakib65/WiFi_Hunter/main/installer.sh && bash installer.sh
```

This will automatically update packages, install all dependencies, clone the repository, and register the `wifi_hunter` global command.

### Method 2 — Manual

```bash
pkg update && pkg upgrade -y
pkg install root-repo git tsu python wpa-supplicant pixiewps iw -y
git clone https://github.com/rdxsakib65/WiFi_Hunter
cd WiFi_Hunter
chmod +x installer.sh
bash installer.sh
```

---

## Commands

| Command | Description |
|---|---|
| `wifi_hunter` | Run WiFi_Hunter with default settings (wlan0 + Pixie Dust) |
| `wifi_hunter menu` | Open WiFi_Hunter interactive menu without auto-attack |
| `wifi_hunter old` | Run the legacy engine (w1.py) with wlan0 |
| `wifi_hunter update` | Pull latest updates from GitHub |
| `wifi_hunter help` | Open the built-in interactive help guide |
| `wifi_hunter fix` | Fix root / superuser issues |
| `wifi_hunter contact` | Contact the developer |

---

## Usage

**Default run — scan nearby networks and attack:**
```bash
wifi_hunter
```

**Pixie Dust on a specific router:**
```bash
wifi_hunter -i wlan0 -b <BSSID> -K
```

**Bruteforce on a specific router:**
```bash
wifi_hunter -i wlan0 -b <BSSID> -B
```

**Pixie Dust without touching Android WiFi settings:**
```bash
wifi_hunter -i wlan0 -K --dts
```

**Resume a previous session:**
```bash
wifi_hunter --list-sessions
wifi_hunter -i wlan0 --resume-session <BSSID>
```

**Generate an HTML report:**
```bash
wifi_hunter -i wlan0 -b <BSSID> -K --html-report
```

For the full argument reference, run `wifi_hunter help` and select option 5.

---

## Troubleshooting

**"No superuser binary detected"**

Run the built-in fix first:
```bash
wifi_hunter fix
```

If the issue persists, use the dedicated fix script:
```bash
curl -sO https://raw.githubusercontent.com/rdxsakib65/fix-termux-root/main/fix.sh && chmod +x fix.sh && ./fix.sh
```

Manual solutions: [github.com/rdxsakib65/fix-termux-root](https://github.com/rdxsakib65/fix-termux-root)

---

**Common issues and fixes**

| Problem | Fix |
|---|---|
| "Run it as root" error | Run `su` first, then retry |
| "Unable to up interface" | Check interface name with `ip link show` |
| wpa_supplicant crash | Run `pkill wpa_supplicant`, then retry |
| No WPS networks found | Disable Location/GPS, toggle WiFi off and on |
| Router keeps locking | Add `-d 3` delay or use `--lock-delay 120` |
| WiFi rfkill blocked | Use `--handle-rfkill` or run `rfkill unblock wifi` |
| Pixie Dust not working | Router may not be vulnerable — switch to Bruteforce (`-B`) |

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full list of changes between versions.

---

## Disclaimer

WiFi_Hunter is provided for educational and authorized penetration testing purposes only. You are solely responsible for ensuring you have permission to test any network. The author is not liable for any misuse, damage, or legal consequences resulting from the use of this tool.

---

## Author

**SAKIB GAMING**

| Platform | Link |
|---|---|
| GitHub | [rdxsakib65](https://github.com/rdxsakib65) |
| Facebook | [rdxsakib65](https://www.facebook.com/share/14f5biWkac4/) |
| Telegram | [@rdxsakib65](https://t.me/panel21p) |
| Website | [tiktok.com/@panel1.1](https://tiktok.com/@panel1.1) |

Honorable mentions include: rofl0r, Rayhan, Alamin, Sojib, Sanji, Mustakin, Sakib, rizzi

---

<div align="center">
If WiFi_Hunter has been useful, consider leaving a star on GitHub.<br>
It helps the project grow and encourages further development.
</div>
