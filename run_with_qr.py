#!/usr/bin/env python3
"""
WiFi_Hunter - QR-enhanced runner
When password is found, shows it + QR code for easy connect.
"""
import sys
import os
import re

# ensure local path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qr_show import show_qr

# Pattern that original tool prints on success
# [+] WPS PIN: 'xxxx'
# [+] WPA PSK: 'yyyy'
# [+] AP SSID: 'zzzz'

_captured = {"pin": None, "psk": None, "ssid": None}
_orig_print = print

def _smart_print(*args, **kwargs):
    text = " ".join(str(a) for a in args)
    # capture
    m = re.search(r"\[\+\]\s*WPS PIN:\s*'([^']*)'", text)
    if m:
        _captured["pin"] = m.group(1)
    m = re.search(r"\[\+\]\s*WPA PSK:\s*'([^']*)'", text)
    if m:
        _captured["psk"] = m.group(1)
    m = re.search(r"\[\+\]\s*AP SSID:\s*'([^']*)'", text)
    if m:
        _captured["ssid"] = m.group(1)
    _orig_print(*args, **kwargs)
    # when we have psk, show QR
    if _captured["psk"] and (_captured["ssid"] or _captured["pin"]):
        show_qr(
            ssid=_captured["ssid"] or "Unknown",
            password=_captured["psk"],
            pin=_captured["pin"]
        )
        # reset so we don't spam
        _captured["psk"] = None

# install intercept
import builtins
builtins.print = _smart_print

# now run the real tool (old engine is clearer for intercept)
# Prefer main.py if user wants menu, else w1
if __name__ == "__main__":
    # pass through args
    # default to old engine path used by "wifi_hunter old"
    target = os.path.join(os.path.dirname(__file__), "w1.py")
    # if first arg is "main" use main.py
    if len(sys.argv) > 1 and sys.argv[1] == "--main":
        target = os.path.join(os.path.dirname(__file__), "main.py")
        sys.argv.pop(1)
    # execute target in this process so print intercept works
    with open(target, "rb") as f:
        code = compile(f.read(), target, "exec")
    # keep __name__ as __main__ for argparse
    g = {"__name__": "__main__", "__file__": target}
    exec(code, g)
