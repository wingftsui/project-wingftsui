import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("white")

class DroneIPS(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Drone Deauth Detect and Resp")
        self.geometry("600x300")
        
        # Label
        self.label = ctk.CTkLabel(self, text="Status:Detecting (Safe)", text_color="green", font=("Arial", 24))
        self.label.pack(pady=40)
        
        # Attack detected (From Alfa card)
        self.btn_attack = ctk.CTkButton(self, text="Deauth Detected!", fg_color="red", command=self.trigger_alert)
        self.btn_attack.pack(pady=10)
        
        # Change of Mode (Warning Only vs Warning + Land)
        self.switch_var = ctk.StringVar(value="warning_only")
        self.switch = ctk.CTkSwitch(self, text="Auto Land Mode (Auto-Land)", variable=self.switch_var, onvalue="auto_land", offvalue="warning_only")
        self.switch.pack(pady=20)

    def trigger_alert(self):
        # Response
        self.label.configure(text="Warning:Deauth Detected！", text_color="red")
        
        if self.switch_var.get() == "auto_land":
            print("Response: Land！")
        else:
            print("Warning")

if __name__ == "__main__":
    app = DroneIPS()
    app.mainloop()