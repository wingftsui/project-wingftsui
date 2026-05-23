import customtkinter as ctk
import socket
import time
import json
import ipaddress

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Active Response Module")
app.geometry("600x300")


def load_drone_json(filepath='drones.json'):
    try:
        with open(filepath,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'No json config file found!')
    except json.JSONDecodeError:
        print(f'Wrong file format. It should be json file')

def trigger_land(drone_model=None,custom_ip=None):

    # Check if the json config file is here. 
    # It records the Drone's profile data.
    # The details of the json content are in the readme file under "Drone-Deauth-Detect-And-Response-System" folder.
    if drone_model is None:
        print("Please provide drone_model in the json config file.")
        return
    
    profiles=load_drone_json()    
    
    # drone_model is absent in the json config file.
    if drone_model not in profiles:
        print(f'Cannot find dron_model in json config file.')
        return
    
    profile=profiles[drone_model]
    target_ip=custom_ip if custom_ip else profile["default_ip"]
    target_port=profile['port']

    try:
        ip_obj = ipaddress.IPv4Address(target_ip)
        
        if ip_obj.is_multicast or target_ip == "255.255.255.255" or target_ip == "0.0.0.0":
            print(f"Broadcast is rejected")
            return
            
    except ipaddress.AddressValueError:
        print(f"{target_ip} is rejected")
        return 

    print(f"\n Will send defense land command ")

    sock=socket.socket(socket.AF_INET, socket.SOCK_)
    try:
        if profile.get("initial_cmd"):
            print("send intial command")
            # Change string into UTF-8
            initial_bytes=profile["initial_command"].encode('utf-8')
            sock.sendto(initial_bytes,(target_ip,target_port))
            time.sleep(0.5)

        if profile.get("land_cmd"):
            print("Send land command now")
            land_bytes=profile["land_command"].encode('utf-8')
            sock.sendto(land_bytes, (target_ip,target_port))
            print("Land command sent successfully")
        
        else:
            print("Json config file has no land commond")
    except Exception as e:
        print(f"Unsuccess : {e}")


    finally:
        sock.close()
        print("Close.\n")

