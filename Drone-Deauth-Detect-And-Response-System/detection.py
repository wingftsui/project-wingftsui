import customtkinter as ctk
from scapy.all import sniff
from scapy.layers.dot11 import Dot11, RadioTap
import threading
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Detection Module")
app.geometry("600x300")

#Showing Status
label = ctk.CTkLabel(app, text="Status:Detecting (Safe)", text_color="green",font=("Arial", 20))
label.pack(pady=50)

####################
mac_history{}

# Detailed Warning Display
def trigger_warning(src_mac,rssi_delta):
    global label, switch_var 
    label.configure(text="Warning:Deauth Detected!"\MAC:{src_mac}\nRSSI Delta:{rssi_delta} dBm", text_color="red")

def detect_deauth(packet):
    # Detect Wifi packet
    if packet.haslayer(Dot11):
        dest_mac=packet.addr1
        pkt_type=packet.type
        pkt_subtype=packet.subtype
        
        # The attacker's deauth attack conditions (3 criteria):
        # (1) it is management frame
        # (2) it is deauth type
        
        if pkt_type==0 and (pkt_subtype==12 or pkt_subtype==10):
            src_mac =packet.addr2
                
            # (3) RSSI [The RSSI difference is larger than 10 dBm compare with 0.1s before.]
            if packet.haslayer(RadioTap)

            print(f"Warning:Broadcast Deauth Attack Detected")
            print(f"  - Source Mac Address: {src_mac}")
            print(f"  - Destination Mac Address: {dest_mac}")

            app.after(0, trigger_warning, src_mac)

def keep_sniffing():
    print("Monitoring WiFi Packets")
    sniff(iface="wlan0",prn=detect_deauth,store=0)

sniff_thread = threading.Thread(target=keep_sniffing,daemon=True)
sniff_thread.start()

app.mainloop()
