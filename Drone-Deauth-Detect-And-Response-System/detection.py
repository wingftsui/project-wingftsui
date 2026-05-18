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
mac_history={}

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
        # (2) it is deauth or disassociation.
        
        if pkt_type==0 and (pkt_subtype==12 or pkt_subtype==10):
            src_mac =packet.addr2
                
            # Detect the RSSI using RadioTap(the tag that alfa card added onto the packet)
            if packet.haslayer(RadioTap):
                try:
                    current_rssi=packet[RadioTap].dBm_AntSignal
                    current_time=packet.time

                    if current_rssi is not None:
                        
                        if src_mac in mac_history:
                            previous_time=mac_history[src_mac]["time"]
                            previous_rssi=mac_history[src_mac]["rssi"]

                            time_diff=current_time - previous_time
                            rssi_delta=abs(current_rssi-previous_rssi)
                             
                            # The attacker's deauth attack conditions (3 criteria):
                            # 3) RSSI [The RSSI difference is larger than 10 dBm compare with 0.1s before.]    
                            if time<=0.1 and rssi_delta>10:
                                print(f"Warning:Broadcast Deauth Attack Detected")
                                print(f"  - Source Mac Address: {src_mac}")
                                print(f"  - Destination Mac Address: {dest_mac}")

                                app.after(0, trigger_warning, src_mac)
                            
                            mac_history[src_mac]={"time":current_time,"rssi":current_rssi}
                except AttributeError:
                    pass

def keep_sniffing():
    print("Monitoring WiFi Packets")
    sniff(iface="wlan0",prn=detect_deauth,store=0)

sniff_thread = threading.Thread(target=keep_sniffing,daemon=True)
sniff_thread.start()

app.mainloop()
