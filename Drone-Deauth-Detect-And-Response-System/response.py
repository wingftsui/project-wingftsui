import customtkinter as ctk
import socket
import time
import json
import ipaddress
import threading
from scapy.all import RadioTap, Dot11, LLC, SNAP, IP, UDP, sendp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Active Response Module")
app.geometry("600x400")


def load_drone_json(filepath='drones.json'):
    try:
        with open(filepath,'r') as file:
            return json.load(file)
    # Check if the json config file is here. 
    # It records the Drone's profile data.
    # The details of the json content are in the readme file under "Drone-Deauth-Detect-And-Response-System" folder.  
    except FileNotFoundError:
        status_label.configure(text=f'No json config file found.')
    except json.JSONDecodeError:
        status_label.configure(text=f'Wrong file format. It should be json file')

target_mac=.get("mac_address")
iface-profile.get("interface","wlan0") 
    try:
        if profile.get("initial_command"):
            status_label.configure(text="send intial command")
            # Change string into UTF-8
            initial_bytes=profile["initial_command"].encode('utf-8')
            sock.sendto(initial_bytes,(target_ip,target_port))
            time.sleep(0.5)

        if profile.get("land_cmd"):
            status_label.configure(text="Send land command now")
            land_bytes=profile["land_cmd"].encode('utf-8')
            sock.sendto(land_bytes, (target_ip,target_port))
            status_label.configure(text="Land command sent successfully")
        
        else:
             status_label.configure(text="Json config file has no land commond")
    except Exception as e:
         status_label.configure(text=f"Unsuccess : {e}")


    finally:
        sock.close()

def btn_trigger_land():

    selected_drone = drone_combo.get()
    input_ip = ip_entry.get()
    final_ip = input_ip if input_ip.strip() != "" else None 
    threading.Thread(target=active_response_land, args=(selected_drone, final_ip), daemon=True).start()


title_label = ctk.CTkLabel(app, text="Active Defense Response System", font=("Arial", 24, "bold"))
title_label.pack(pady=(20, 10))

status_label = ctk.CTkLabel(app, text="Status: Standby", text_color="white", font=("Arial", 16))
status_label.pack(pady=(0, 20))

drone_data = load_drone_json()
drone_list = list(drone_data.keys()) if "Error" not in drone_data else ["DRONE1"]

drone_combo = ctk.CTkComboBox(app, values=drone_list, width=200)
drone_combo.pack(pady=10)
if drone_list:
    drone_combo.set(drone_list[0])

ip_entry = ctk.CTkEntry(app, placeholder_text="Custom IP (Optional)", width=200)
ip_entry.pack(pady=10)

land_btn = ctk.CTkButton(app, text="EMERGENCY LAND", fg_color="red", hover_color="darkred", 
                         font=("Arial", 20, "bold"), height=50, command=btn_trigger_land)
land_btn.pack(pady=30)

app.mainloop()