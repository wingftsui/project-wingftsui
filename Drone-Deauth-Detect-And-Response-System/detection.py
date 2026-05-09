import customtkinter as ctk
from scapy.all import *
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Detection Module")
app.geometry("600x300")

#Showing Status
label = ctk.CTkLabel(app, text="Status:Detecting (Safe)", text_color="green",font=("Arial", 20))
label.pack(pady=50)

def status_changed():
    global label, switch_var 
    label.configure(text="Warning:Deauth Detected！", text_color="red")

def detect_deauth(packet):
    # Detect Wifi packet
    if packet.haslayer(Dot11):
        dest_mac=packet.addr1
        pkt_type=packet.type
        pkt_subtype=packet.subtype
        
        # The attacker's deauth attack conditions:
        # (1) it is broadcast
        # (2) it is management frame
        # (3) it is deauth type
        if dest_mac =="ff:ff:ff:ff:ff:ff":
            if pkt_type==0 and pkt_subtype==12:
                src_mac =packet.addr2
                
                print(f"Warning:Broadcast Deauth Attack Detected")
                print(f"  - Destination Mac Address: {dest_mac}")

                app.after(0, status_changed, src_mac)


app.mainloop()
