import customtkinter as ctk
from scapy.all import sniff
from scapy.layers.dot11 import Dot11, RadioTap
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Detection Module")
app.geometry("600x300")

#Showing Status
label = ctk.CTkLabel(app, text="Status:Detecting (Safe)", text_color="green",font=("Arial", 20))
label.pack(pady=50)


mac_history={}

# Detailed Warning Display
def trigger_warning(src_mac, dest_mac,reason):
    global label
    warning_text=(
        f"Warning: Deauth Detected! \n"
        f"Attacker (Source) mac:{src_mac} \n"
        f"Target (Destination):{dest_mac}\n"
        f"Reason: {reason}"
    )    
    label.configure(text=warning_text,text_color="red")

def detect_deauth(packet):
    # Detect Wifi packet
    if packet.haslayer(Dot11):
        dest_mac=packet.addr1
        pkt_type=packet.type
        pkt_subtype=packet.subtype
        
        # Check if it is deauth.
        # (1) it is management frame
        # (2) it is deauth or disassociation.
        if pkt_type==0 and (pkt_subtype==12 or pkt_subtype==10):
            src_mac =packet.addr2
            current_time=packet.time

            current_seq=packet[Dot11].SC>>4
            current_rssi=None
            
            if src_mac in mac_history:
                previous_time = mac_history[src_mac]["time"]
                previous_seq = mac_history[src_mac].get("seq", current_seq)
                time_diff = current_time - previous_time
                if time_diff <= 0.1:
                
                # The system has 2 round checking to distinguish attacker deauth attack.
                
                # 1st Round Checking: Check the sequence number in management frame
                    seq_diff = abs(current_seq-previous_seq)
                    if 50 < seq_diff < 4000:
                        print(f"Warning: Deauth Attack Detected! Abnormal Sequence Number!")
                        app.after(0, trigger_warning, src_mac, "N/A (SEQ Attack)")
                        return
                

                    # 2nd Round Checking: Detect the RSSI using RadioTap (the tag that alfa card added onto the packet)
                    if packet.haslayer(RadioTap):
                        try:
                            current_rssi=packet[RadioTap].dBm_AntSignal
                            if current_rssi is not None:
                                previous_rssi = mac_history[src_mac].get("rssi", current_rssi)
                                rssi_delta = abs(current_rssi - previous_rssi)
                        
                        
                                # The RSSI difference is larger than 10 dBm compare with 0.1s before.]    
                                if rssi_delta>10:
                                    print(f"Warning:Broadcast Deauth Attack Detected")
                                    print(f"  - Source Mac Address: {src_mac}")
                                    print(f"  - Destination Mac Address: {dest_mac}")

                                    app.after(0, trigger_warning, src_mac, rssi_delta)
                                    return       
                           
                        except AttributeError:
                            pass
            if packet.haslayer(RadioTap) and current_rssi is None:
                try:
                    current_rssi = packet[RadioTap].dBm_AntSignal
                except:
                    pass

                mac_history[src_mac]={"time":current_time,"seq": current_seq,"rssi":current_rssi if current_rssi is not None else mac_history.get(src_mac, {}).get("rssi")}


def keep_sniffing():
    print("Monitoring WiFi Packets")
    sniff(iface="wlan0",prn=detect_deauth,store=0)

sniff_thread = threading.Thread(target=keep_sniffing,daemon=True)
sniff_thread.start()

app.mainloop()
