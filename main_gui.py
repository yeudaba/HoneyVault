# main_gui.py
import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox

# ייבוא הפונקציות שבנינו
from core.key_manager import create_shared_keys, recover_key
from core.deception import start_guard
from run_vault import perform_cryptography, USB_SHARE_FILE

# הגדרות עיצוב
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HoneyVaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HoneyVault - Active Cyber Defense")
        self.geometry("600x500")
        
        # --- כותרת ---
        self.label_title = ctk.CTkLabel(self, text="HoneyVault 🛡️", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=20)

        # --- בחירת תיקייה ---
        self.frame_select = ctk.CTkFrame(self)
        self.frame_select.pack(pady=10, padx=20, fill="x")
        
        self.btn_browse = ctk.CTkButton(self.frame_select, text="Select Target Folder", command=self.select_folder)
        self.btn_browse.pack(side="left", padx=10)
        
        self.label_folder = ctk.CTkLabel(self.frame_select, text="No folder selected", text_color="gray")
        self.label_folder.pack(side="left", padx=10)
        
        self.selected_folder = None

        # --- איזור הפעולות (Lock / Unlock) ---
        self.frame_actions = ctk.CTkFrame(self)
        self.frame_actions.pack(pady=20, padx=20, fill="both", expand=True)

        # כפתור נעילה
        self.btn_lock = ctk.CTkButton(self.frame_actions, text="🔒 LOCK & ARM SYSTEM", 
                                      command=self.lock_system, fg_color="#d32f2f", hover_color="#b71c1c", height=50)
        self.btn_lock.pack(pady=20, padx=40, fill="x")

        # כפתור פתיחה
        self.btn_unlock = ctk.CTkButton(self.frame_actions, text="🔓 UNLOCK & RESTORE", 
                                        command=self.unlock_system, fg_color="#388e3c", hover_color="#2e7d32", height=50)
        self.btn_unlock.pack(pady=10, padx=40, fill="x")

        # סטטוס
        self.label_status = ctk.CTkLabel(self, text="System Ready.", text_color="gray")
        self.label_status.pack(side="bottom", pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.label_folder.configure(text=os.path.basename(folder), text_color="white")

    def lock_system(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        # תהליך הנעילה
        try:
            self.label_status.configure(text="Generating Split Keys...", text_color="yellow")
            self.update()
            
            # 1. יצירת מפתחות
            file_share, password_share = create_shared_keys()
            master_key = recover_key(file_share, password_share)
            
            # 2. הצפנה
            perform_cryptography(self.selected_folder, master_key, "encrypt")
            
            # 3. שמירת קובץ ה-USB
            with open(USB_SHARE_FILE, "w") as f:
                f.write(file_share)
            
            # הצגת הסיסמה למשתמש בחלון קופץ
            messagebox.showinfo("LOCKED!", f"System Locked Successfully.\n\nYOUR PASSWORD SHARE:\n{password_share}\n\nSave this carefully!")
            
            # שאלה על הגנה אקטיבית
            ans = messagebox.askyesno("Active Defense", "Do you want to enable Active Defense Mode?\n(Surveillance for intruders)")
            
            if ans:
                self.start_active_defense()
            else:
                self.label_status.configure(text="Locked (Defense OFF)", text_color="orange")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_active_defense(self):
        self.label_status.configure(text="🛡️ ACTIVE DEFENSE: MONITORING...", text_color="#00e676")
        # מריצים את השמירה בתהליך נפרד (Thread) כדי שהממשק לא ייתקע
        t = threading.Thread(target=start_guard, args=(self.selected_folder, USB_SHARE_FILE))
        t.daemon = True
        t.start()
        messagebox.showinfo("ARMED", "Honeytokens deployed.\nAny intrusion will trigger key destruction.")

    def unlock_system(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        if not os.path.exists(USB_SHARE_FILE):
            messagebox.showerror("CRITICAL ERROR", "USB Key File missing!\nIt might have been destroyed by Active Defense.")
            return

        # בקשת סיסמה
        dialog = ctk.CTkInputDialog(text="Enter your Password Share:", title="Unlock")
        pass_share = dialog.get_input()
        
        if pass_share:
            with open(USB_SHARE_FILE, "r") as f:
                file_share = f.read().strip()
            
            master_key = recover_key(file_share, pass_share)
            
            if master_key:
                perform_cryptography(self.selected_folder, master_key, "decrypt")
                messagebox.showinfo("Success", "Folder Unlocked Successfully!")
                self.label_status.configure(text="System Unlocked", text_color="white")
            else:
                messagebox.showerror("Error", "Wrong Password or Corrupted Key!")

if __name__ == "__main__":
    app = HoneyVaultApp()
    app.mainloop()