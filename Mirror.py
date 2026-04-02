import os
import sys
import subprocess
import threading
import urllib.request
import zipfile
import customtkinter as ctk
from tkinter import messagebox

# Kényszerítjük az UTF-8 kódolást a print-ekhez (csak ha van konzol)
if sys.stdout is not None:
    sys.stdout.reconfigure(encoding='utf-8')

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 

# AppData mappa beállítása a jogosultságok miatt
appdata_dir = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
BASE_DIR = os.path.join(appdata_dir, "AndroidMirrorApp")
SCRCPY_FOLDER = os.path.join(BASE_DIR, "scrcpy_tools")

# Itt adjuk meg, honnan töltse le a programot, ha még nincs meg a gépen
SCRCPY_URL = "https://github.com/Genymobile/scrcpy/releases/download/v2.4/scrcpy-win64-v2.4.zip"

def find_scrcpy_exe():
    """Megkeresi a scrcpy.exe-t a letöltött mappában."""
    if not os.path.exists(SCRCPY_FOLDER):
        return None
    for root, dirs, files in os.walk(SCRCPY_FOLDER):
        if "scrcpy.exe" in files:
            return os.path.join(root, "scrcpy.exe")
    return None

def download_and_extract_scrcpy(status_label):
    """Letölti és kicsomagolja a scrcpy-t, ha nincs meg."""
    try:
        os.makedirs(SCRCPY_FOLDER, exist_ok=True)
        zip_path = os.path.join(SCRCPY_FOLDER, "scrcpy_download.zip")
        
        status_label.configure(text="Kérlek várj, scrcpy letöltése folyamatban... (kb. 5-10 MB)")
        urllib.request.urlretrieve(SCRCPY_URL, zip_path)
        
        status_label.configure(text="Fájlok kicsomagolása...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(SCRCPY_FOLDER)
            
        os.remove(zip_path) # Töröljük a zip-et, már nem kell
        status_label.configure(text="Letöltés sikeres!")
        return True
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült letölteni a fájlokat:\n{e}")
        status_label.configure(text="Letöltés sikertelen.")
        return False

def start_android_mirror(max_fps, video_bitrate, rotation_str, turn_screen_off, stay_awake, btn, status_label):
    btn.configure(state="disabled", text="Tükrözés fut...")
    
    # 1. Ellenőrizzük, megvan-e a scrcpy.exe
    scrcpy_exe_path = find_scrcpy_exe()
    if not scrcpy_exe_path:
        success = download_and_extract_scrcpy(status_label)
        if not success:
            btn.configure(state="normal", text="🚀 Tükrözés Indítása")
            return
        scrcpy_exe_path = find_scrcpy_exe()

    status_label.configure(text="Csatlakozás a telefonhoz...")

    # 2. Paraméterek összeállítása
    rotation_map = {"Alap (0°)": "0", "Balra forgat (90°)": "1", "Fejjel lefelé (180°)": "2", "Jobbra forgat (90°)": "3"}
    rotation_val = rotation_map.get(rotation_str, "0")

    command = [
        scrcpy_exe_path, # Itt már a letöltött exe-t használjuk!
        f"--max-fps={max_fps}",
        f"--video-bit-rate={video_bitrate}",
        f"--rotation={rotation_val}",
        "--window-title=Android Tükrözés"
    ]

    if turn_screen_off: command.append("--turn-screen-off")
    if stay_awake: command.append("--stay-awake")

    # 3. Indítás
    try:
        # A creationflags=subprocess.CREATE_NO_WINDOW elrejti a felugró fekete CMD ablakot a háttérben
        process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        status_label.configure(text="Tükrözés leállítva.")
    except Exception as e:
        messagebox.showerror("Hiba", f"A tükrözés nem indult el. Csatlakoztatva van a telefon USB-n?\n(USB Hibakeresés be van kapcsolva?)\n\nRészletek: {e}")
        status_label.configure(text="Hiba a csatlakozáskor.")
    finally:
        btn.configure(state="normal", text="🚀 Tükrözés Indítása")

def on_start_click():
    fps = fps_var.get()
    bitrate = bitrate_var.get()
    rotation = rotation_var.get()
    screen_off = screen_off_var.get()
    awake = awake_var.get()

    thread = threading.Thread(
        target=start_android_mirror, 
        args=(fps, bitrate, rotation, screen_off, awake, start_btn, status_label)
    )
    thread.daemon = True 
    thread.start()

# --- UI LÉTREHOZÁSA ---
app = ctk.CTk()
app.title("Phone Mirror")
app.geometry("420x500")
app.resizable(False, False)

title_label = ctk.CTkLabel(app, text="Tükrözés", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(pady=(20, 10))

frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=20, fill="both", expand=True)

# UI Elemek...
fps_label = ctk.CTkLabel(frame, text="Képfrissítés (FPS):")
fps_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
fps_var = ctk.StringVar(value="60")
ctk.CTkOptionMenu(frame, variable=fps_var, values=["30", "45", "60", "90", "120"]).grid(row=0, column=1, padx=20, pady=(20, 10), sticky="e")

bitrate_label = ctk.CTkLabel(frame, text="Minőség (Bitrate):")
bitrate_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
bitrate_var = ctk.StringVar(value="8M")
ctk.CTkOptionMenu(frame, variable=bitrate_var, values=["2M", "4M", "8M", "16M", "32M"]).grid(row=1, column=1, padx=20, pady=10, sticky="e")

rotation_label = ctk.CTkLabel(frame, text="Tájolás:")
rotation_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
rotation_var = ctk.StringVar(value="Alap (0°)")
ctk.CTkOptionMenu(frame, variable=rotation_var, values=["Alap (0°)", "Balra forgat (90°)", "Fejjel lefelé (180°)", "Jobbra forgat (90°)"]).grid(row=2, column=1, padx=20, pady=10, sticky="e")

screen_off_var = ctk.BooleanVar(value=True)
ctk.CTkSwitch(frame, text="Telefon kijelzőjének kikapcsolása", variable=screen_off_var).grid(row=3, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

awake_var = ctk.BooleanVar(value=True)
ctk.CTkSwitch(frame, text="Telefon ébrentartása futás közben", variable=awake_var).grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

start_btn = ctk.CTkButton(app, text="Tükrözés Indítása", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=on_start_click)
start_btn.pack(pady=(5, 5))

# Státusz szöveg alul
status_label = ctk.CTkLabel(app, text="Készen áll.", text_color="gray", font=ctk.CTkFont(size=12))
status_label.pack(pady=(0, 10))

app.mainloop()