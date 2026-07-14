import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

# your existing logic imports
from files.combiner import combine
from files.encrypt_file import encrypt_file

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("DevGeeks Crypter")
app.geometry("420x320")
app.resizable(False, False)
app.iconbitmap("favicon.ico")

# center window
app.update_idletasks()
x = (app.winfo_screenwidth() - app.winfo_width()) // 2
y = (app.winfo_screenheight() - app.winfo_height()) // 2
app.geometry(f"+{x}+{y}")

# ---------------- FUNCTIONS ----------------

def browse_input():
    path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    input_entry.delete(0, "end")
    input_entry.insert(0, path)

def browse_output():
    path = filedialog.askdirectory()
    output_entry.delete(0, "end")
    output_entry.insert(0, path)

def start_process():
    if not input_entry.get() or not output_entry.get() or not name_entry.get():
        messagebox.showerror("Error", "Please fill all fields")
        return

    loading = ctk.CTkToplevel(app)
    loading.title("Processing")
    loading.geometry("300x150")
    loading.resizable(False, False)

    ctk.CTkLabel(loading, text="Encrypting...", font=("Helvetica", 16)).pack(pady=20)
    bar = ctk.CTkProgressBar(loading, mode="indeterminate")
    bar.pack(pady=10)
    bar.start()

    threading.Thread(
        target=process_files,
        args=(loading,)
    ).start()

def process_files(loading):
    try:
        input_file = input_entry.get()
        output_dir = output_entry.get()
        name = name_entry.get()

        if not name.endswith(".py"):
            name += ".py"

        output_path = os.path.join(output_dir, name)

        key = os.urandom(32)
        nonce = os.urandom(16)

        payload, tag = encrypt_file(key, nonce, input_file)
        combine(key, nonce, tag, payload, output_path)

        loading.destroy()
        messagebox.showinfo(
            "Done",
            "Encryption completed successfully!"
        )

    except Exception as e:
        loading.destroy()
        messagebox.showerror("Error", str(e))

# ---------------- UI ----------------

title = ctk.CTkLabel(
    app,
    text="DevGeeks Crypter",
    font=("Helvetica", 26)
)
title.pack(pady=15)

input_entry = ctk.CTkEntry(
    app,
    width=280,
    placeholder_text="Input py path"
)
input_entry.pack(pady=5)

ctk.CTkButton(
    app,
    text="Browse Input",
    command=browse_input
).pack(pady=5)

output_entry = ctk.CTkEntry(
    app,
    width=280,
    placeholder_text="Output folder"
)
output_entry.pack(pady=5)

ctk.CTkButton(
    app,
    text="Browse Output",
    command=browse_output
).pack(pady=5)

name_entry = ctk.CTkEntry(
    app,
    width=280,
    placeholder_text="Output file name"
)
name_entry.pack(pady=10)

ctk.CTkButton(
    app,
    text="Encrypt",
    fg_color="black",
    hover_color="#363636",
    command=start_process
).pack(pady=15)

app.mainloop()
