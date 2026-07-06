#!/usr/bin/env python3
# ────────────────────────────────────────────────────────────
# CAT MAC TUNEUP 0.2 — PHOTON OS GRADE
# files = off · Proto AC edition · hardened & minimal
# Blue hue + black background · Photon-grade TCP hardening
# ────────────────────────────────────────────────────────────

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import shlex

# ─── PHOTON-GRADE COLORS ─────────────────────────────────────
BG = "#000000"
TEXT = "#00b4ff"
ACCENT = "#00d4ff"
DIM = "#003366"
PANEL = "#0a0f1a"
BTN_BG = "#000000"
BTN_FG = "#00b4ff"
BTN_HOVER = "#001a33"
GREEN = "#00ffaa"
RED = "#ff3366"
WHITE = "#ffffff"

VERSION = "0.2"
APP_NAME = "Cat Mac Tuneup"
TAGLINE = "files = off · Photon OS Grade"

# ─── HARDENED TCP SETTINGS (Photon-inspired) ───────────────
TCP_SETTINGS = {
    "net.inet.tcp.always_keepalive": "1",
    "net.inet.tcp.keepidle": "30000",      # 30s idle before probe
    "net.inet.tcp.keepintvl": "5000",      # 5s between probes
    "net.inet.tcp.keepcnt": "8",           # max 8 probes
    "net.inet.tcp.mssdflt": "1448",        # better MTU
    "net.inet.tcp.blackhole": "2",         # drop bogus packets
    "net.inet.tcp.log_in_vain": "1",       # log invalid attempts
    "net.inet.tcp.syncookie": "1",         # SYN flood protection (macOS OID)
}

class CatMacTuneup:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {VERSION} — Photon Grade")
        self.root.geometry("760x620")
        self.root.minsize(680, 520)
        self.root.configure(bg=BG)

        self.is_admin = os.geteuid() == 0
        
        self._setup_ui()
        self._check_status()

    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(24, 12))
        
        tk.Label(
            header, text=f"🐱 {APP_NAME} {VERSION}",
            font=("Helvetica Neue", 26, "bold"), fg=TEXT, bg=BG
        ).pack(side="left")
        
        tk.Label(
            header, text=TAGLINE,
            font=("Helvetica Neue", 11), fg=DIM, bg=BG
        ).pack(side="left", padx=16)

        # Status
        status_frame = tk.Frame(self.root, bg=PANEL, bd=2, relief="solid", highlightbackground=ACCENT)
        status_frame.pack(fill="x", padx=24, pady=8)
        
        self.status_label = tk.Label(
            status_frame, text="🔍 Checking Photon-grade TCP status...",
            font=("Helvetica Neue", 13, "bold"), fg=TEXT, bg=PANEL, padx=20, pady=12
        )
        self.status_label.pack(anchor="w")

        self.admin_label = tk.Label(
            status_frame, text="", font=("Helvetica Neue", 10),
            fg=DIM, bg=PANEL, padx=20
        )
        self.admin_label.pack(anchor="w")

        self.detail_label = tk.Label(
            status_frame, text="", font=("Helvetica Neue", 10),
            fg=DIM, bg=PANEL, padx=20
        )
        self.detail_label.pack(anchor="w", pady=(0, 12))

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="x", padx=24, pady=12)
        
        for text, cmd, color in [
            ("🔧 Apply Photon TCP Hardening", self.apply_fix, ACCENT),
            ("✅ Verify Settings", self._check_status, GREEN),
            ("🔄 Install Persistent Fix", self.install_launchd, TEXT),
        ]:
            tk.Button(
                btn_frame, text=text, command=cmd,
                bg=BTN_BG, fg=color, activebackground=BTN_HOVER,
                font=("Helvetica Neue", 11, "bold"), padx=24, pady=12,
                relief="flat", cursor="hand2"
            ).pack(side="left", padx=(0, 12))

        self.sudo_btn = tk.Button(
            btn_frame, text="👑 Restart with Admin", command=self._elevate,
            bg=BTN_BG, fg=GREEN, activebackground=BTN_HOVER,
            font=("Helvetica Neue", 11, "bold"), padx=24, pady=12,
            relief="flat", cursor="hand2"
        )
        self.sudo_btn.pack(side="left", padx=(0, 12))
        if self.is_admin:
            self.sudo_btn.pack_forget()

        # Log
        log_frame = tk.Frame(self.root, bg=PANEL, bd=2, relief="solid", highlightbackground=DIM)
        log_frame.pack(fill="both", expand=True, padx=24, pady=8)
        
        tk.Label(log_frame, text="📋 Activity Log", font=("Helvetica Neue", 11, "bold"),
                 fg=DIM, bg=PANEL, padx=16, pady=6).pack(anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, bg=BG, fg=TEXT, font=("Menlo", 10), wrap="word",
            height=14, highlightthickness=0, relief="flat"
        )
        self.log_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Footer
        tk.Label(
            self.root, text=f"Proto AC 2026 · files = off · Photon OS Grade",
            font=("Helvetica Neue", 9), fg=DIM, bg=BG
        ).pack(pady=12)

    def _log(self, msg, color=TEXT):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {msg}\n", "log")
        self.log_text.see("end")
        self.root.update_idletasks()

    def _elevate(self):
        self._log("👑 Re-launching with admin privileges via sudo...", ACCENT)
        try:
            subprocess.Popen(
                ["/usr/bin/osascript", "-e",
                 f'do shell script "sudo python3 {shlex.quote(__file__)}" with administrator privileges']
            )
            self.root.after(500, self.root.destroy)
        except Exception as e:
            self._log(f"❌ Elevation failed: {e}", RED)

    def _check_status(self):
        self._log("🔍 Checking Photon-grade TCP hardening...")
        if self.is_admin:
            self.admin_label.config(text="👑 Running with admin privileges", fg=GREEN)
        else:
            self.admin_label.config(text="⚠️ Not running as root — sysctl writes will fail without sudo", fg=RED)
        try:
            val = self._sysctl_get("net.inet.tcp.always_keepalive")
            if val == "1":
                self.status_label.config(text="✅ PHOTON-GRADE TCP: HARDENED", fg=GREEN)
                self.detail_label.config(text="always_keepalive=1 + aggressive keepalives")
                self._log("✅ TCP Time Bomb mitigation active", GREEN)
            else:
                self.status_label.config(text="❌ TCP TIME BOMB: ACTIVE", fg=RED)
                self.detail_label.config(text="Run 'Apply Photon TCP Hardening'")
                self._log("❌ TCP hardening not fully applied", RED)
        except Exception as e:
            self._log(f"⚠️ Error: {e}", RED)

    def _sysctl_get(self, key):
        r = subprocess.run(["sysctl", "-n", key], capture_output=True, text=True)
        return r.stdout.strip()

    def apply_fix(self):
        if not self.is_admin:
            self._log("❌ Admin privileges required — re-run with sudo", RED)
            self.status_label.config(text="❌ NEEDS SUDO — re-run with sudo", fg=RED)
            self.detail_label.config(text="sudo python3 catbooster0.2.py")
            return
        self._log("🔧 Applying Photon OS Grade TCP hardening...")
        success = True
        for key, value in TCP_SETTINGS.items():
            try:
                result = subprocess.run(["sysctl", "-w", f"{key}={value}"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self._log(f"✅ {key} = {value}", GREEN)
                else:
                    self._log(f"❌ Failed {key}: {result.stderr.strip()}", RED)
                    success = False
            except Exception as e:
                self._log(f"❌ Error setting {key}: {e}", RED)
                success = False
        if success:
            self._log("✅ Photon-grade TCP hardening applied!", GREEN)
            self._check_status()
        else:
            self._log("⚠️ Some settings failed (run with sudo if needed)", RED)

    def install_launchd(self):
        if not self.is_admin:
            self._log("❌ Admin privileges required — re-run with sudo", RED)
            return
        self._log("🔄 Installing persistent Photon fix via launchd...")
        # Each key=value pair gets its own ProgramArguments entry so the
        # plist is valid and sysctl receives them correctly.
        args = ["/usr/sbin/sysctl", "-w"]
        for key, value in TCP_SETTINGS.items():
            args.append(f"{key}={value}")
        plist_args = "\n".join(f"        <string>{shlex.quote(a)}</string>" for a in args)
        plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ac.tunecat</string>
    <key>ProgramArguments</key>
    <array>
{plist_args}
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>300</integer>
</dict>
</plist>"""
        path = "/Library/LaunchDaemons/com.ac.tunecat.plist"
        try:
            with open(path, "w") as f:
                f.write(plist)
            subprocess.run(["launchctl", "load", path], capture_output=True, text=True, check=True)
            self._log(f"✅ Persistent Photon fix installed at {path}", GREEN)
        except subprocess.CalledProcessError as e:
            self._log(f"❌ launchctl load failed: {e.stderr.strip()}", RED)
        except Exception as e:
            self._log(f"❌ Failed to install launchd: {e}", RED)

def main():
    root = tk.Tk()
    app = CatMacTuneup(root)
    root.mainloop()

if __name__ == "__main__":
    main()