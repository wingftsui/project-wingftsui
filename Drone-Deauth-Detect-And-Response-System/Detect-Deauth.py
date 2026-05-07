import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# GUI background
app = ctk.CTk()
app.title("Drone Deauth Response")
app.geometry("600x300")

#Showing Status
label = ctk.CTkLabel(app, text="Status:Detecting (Safe)", text_color="green")
label.pack(pady=40)

def trigger_alert():
    global label, switch_var 
    label.configure(text="Warning:Deauth Detected！", text_color="red")

btn_attack = ctk.CTkButton(app, text="Deauth Detected!", command=trigger_alert)
btn_attack.pack(pady=10)

app.mainloop()