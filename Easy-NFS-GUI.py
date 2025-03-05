import tkinter as tk
from tkinter import ttk 
import os 
import subprocess
import re
import sys
from tkinter import filedialog
import platform
from tkinter import PhotoImage

def get_ip_info():
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output("ipconfig", shell=True, text=True)
            ip_match = re.search(r"IPv4 Address[.\s]*: ([\d.]+)", result)
        else:
            result = subprocess.check_output("ip addr show", shell=True, text=True)
            ip_match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", result)
        
        ip_info.set(ip_match.group(1) if ip_match else "IP Not Found")
    except Exception as e:
        ip_info.set("Error fetching IP")

# Gets the home directory path for saving user choices this makes it so that when redownloading the GUI you don't need to set it up again
def get_file_path(filename):
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, filename)

# Saves user choices
def save_user_choices():
    file_path = get_file_path('NFS_choices.txt')
    with open(file_path, 'w') as file:
        file.write(f"{selected_dir.get()}\n")
        file.write(f"{my_ip.get()}\n")
        file.write(f"{root.geometry()}\n")
        file.write(f"{theme_var.get()}\n") 

# Loads user choices
def load_user_choices():
    file_path = get_file_path('NFS_choices.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 4:
                selected_dir.set(lines[0].strip()) 
                my_ip.delete(0, tk.END)  
                my_ip.insert(0, lines[1].strip())
                root.geometry(lines[2].strip())
                theme_var.set(lines[3].strip())
                apply_theme()

# Clears selected share directory
def clear_dict_settings():
    selected_dir.set("No directory selected")
    save_user_choices()  

def set_window_size():
    if platform.system() == "Windows":
        root.geometry('410x360')  

# Clears GUI size settings
def clear_size_settings(): 
    set_window_size()

# Clears all settings
def clear_all_settings():
    selected_dir.set("No directory selected") 
    my_ip.delete(0, tk.END)  
    theme_var.set("Dark")  
    apply_theme()  
    set_window_size()  
    save_user_choices() 

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        formatted_directory = os.path.normpath(directory) 
        selected_dir.set(formatted_directory)

def run_command():
    ip = my_ip.get()
    if not ip:
        ip = "0.0.0.0"
    
    directory = selected_dir.get()
    if directory == "No directory selected":
        return 

    command = f"WinNFSd.exe -addr {ip} {directory} /"
    # Batch file for future use
    with open("run_NFS.bat", "w") as batch_file:
        batch_file.write(command)
    
    subprocess.call(["start", "cmd", "/k", command], shell=True)

# Open Network Connections command idk just if someone wants it :/
def net_command():
    command = f"ncpa.cpl"
    subprocess.Popen('ncpa.cpl', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    print(command)

# Open CMD ipconfig just cuz
def ip_command():
    command = f"ipconfig"
    subprocess.call(["start", "cmd", "/k", command], shell=True)
    print(command)

# Theme doggle
def toggle_theme():
    if theme_var.get() == "Dark":
        theme_var.set("Light")
    else:
        theme_var.set("Dark")
    apply_theme()

# Applies theme
def apply_theme():
    theme = theme_var.get()
    
    bg_color = "#2E2E2E" if theme == "Dark" else "#FFFFFF"
    fg_color = "#FFFFFF" if theme == "Dark" else "#000000"
    button_bg = "#4B4B4B" if theme == "Dark" else "#E0E0E0"

    root.configure(bg=bg_color)
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=button_bg, foreground=fg_color)
    style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
    save_user_choices()

# Builds the GUI window 
root = tk.Tk()
root.bind("<Configure>", lambda event: save_user_choices()) 
root.geometry('410x360')
root.title("NFS GUI")

root.configure(bg="#2E2E2E")
icon_path = 'imgs/icon.ico'
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Background image for the GUI window
if os.path.exists("imgs/background.png"):
    background_image = tk.PhotoImage(file="imgs/background.png")
    root.background_image = background_image  
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#2E2E2E")
style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
style.configure("TButton", background="#4B4B4B", foreground="#FFFFFF")
theme_var = tk.StringVar(value="Dark")

# Directory selection
button = ttk.Button(root, text="Select share directory", command=select_directory)
button.pack(pady=5)
selected_dir = tk.StringVar(value="No directory selected")
label = tk.Label(root, textvariable=selected_dir, wraplength=400, anchor="w", justify="left")
label.pack(pady=10)

def apply_ip():
    ip_address = ip_info.get() 
    my_ip.delete(0, tk.END)  
    my_ip.insert(0, ip_address)  

# Frame for buttons
parent_frame = tk.Frame(root)
parent_frame.pack(pady=5, anchor="center")  

# Refresh button 
refresh_button = ttk.Button(parent_frame, text="Refresh", command=get_ip_info, style="TButton")
refresh_button.pack(side=tk.LEFT, padx=(5, 0)) # Added padding for better spacing

# IP info
ip_info_frame = tk.Frame(parent_frame)
ip_info_frame.pack(side=tk.LEFT, padx=(5, 10))  # Added padding for better spacing
ip_label = tk.Label(ip_info_frame, text="Current IP:", font=("Arial", 10, "bold"))
ip_label.pack(side=tk.LEFT, padx=(0, 5))  # Added padding for better spacing
ip_info = tk.StringVar(value="Fetching...")
ip_value_label = tk.Label(ip_info_frame, textvariable=ip_info, font=("Arial", 10))
ip_value_label.pack(side=tk.LEFT)

# Apply button (on the right side)
apply_button = ttk.Button(parent_frame, text="Apply", command=apply_ip, style="TButton")
apply_button.pack(side=tk.LEFT, padx=(10, 5))   # Added padding for better spacing

# IP entry
myipLabel = ttk.Label(root, text="Your IP Address")
myipLabel.pack() 
my_ip = tk.Entry(root)
my_ip.pack(pady=(0, 5))  # Added padding for better spacing

# Fetch IP info on startup
get_ip_info()

run_button = ttk.Button(root, text="Run NFS server", command=lambda: [run_command(), save_user_choices()])
run_button.pack(pady=(10, 10))  # Added padding for better spacing

# Frame for settings buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=(10, 10))

# Clear user settings
clear_button = ttk.Button(button_frame, text="Clear Directory Settings", command=clear_dict_settings)
clear_button.pack(side=tk.LEFT, padx=(0, 10))  # Added padding for better spacing

# Clear user settings
clear_button = ttk.Button(button_frame, text="Clear Size Settings", command=clear_size_settings)
clear_button.pack(side=tk.LEFT, padx=(10, 0))  # Added padding for better spacing

# Clear all settings
clear_button = ttk.Button(button_frame, text="Clear All Settings", command=clear_all_settings)
clear_button.pack(side=tk.LEFT, padx=(10, 0))  # Added padding for better spacing

# Create a frame to hold the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=(0, 10))  # Added padding for better spacing

# Open Network Connections 
net_button = ttk.Button(button_frame, text="Open Network Settings", command=net_command)
net_button.pack(side=tk.LEFT, padx=(0, 10))  # Added padding for better spacing

# Open ipconfig 
ip_button = ttk.Button(button_frame, text="Show full IP info", command=ip_command)
ip_button.pack(side=tk.LEFT)  # Added padding for better spacing

# Light and dark theme toggle
toggle_button = ttk.Button(root, text="Light/Dark Theme", command=toggle_theme)
toggle_button.pack(pady=(10, 10))  # Added padding for better spacing

# Load user choices on start
load_user_choices()

# Save user choices on exit
root.protocol("WM_DELETE_WINDOW", lambda: [save_user_choices(), root.destroy()])

root.mainloop()