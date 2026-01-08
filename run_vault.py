# run_vault.py
import os
import sys
from cryptography.fernet import Fernet
from core.key_manager import create_shared_keys, recover_key
# הוספנו את ייבוא ההגנה האקטיבית
from core.deception import start_guard

USB_SHARE_FILE = "usb.share"

def process_folder(target_folder, mode):
    
    # === נעילה (LOCK) ===
    if mode == "lock":
        print("\n--- STARTING LOCK PROCESS ---")
        
        # 1. יצירת מפתחות
        file_share, password_share = create_shared_keys()
        
        # 2. שחזור זמני להצפנה
        master_key = recover_key(file_share, password_share)
        
        # 3. הצפנה
        perform_cryptography(target_folder, master_key, "encrypt")
        
        # 4. שמירת המפתח לדיסק
        with open(USB_SHARE_FILE, "w") as f:
            f.write(file_share)
            
        print("\n" + "="*40)
        print("LOCKED SUCCESSFULLY!")
        print(f"1. Key Part A saved to: {USB_SHARE_FILE}")
        print(f"2. YOUR PASSWORD (Part B): {password_share}")
        print("SAVE THIS PASSWORD! You cannot unlock without it.")
        print("="*40 + "\n")
        
        # === שלב ההגנה האקטיבית ===
        choice = input("Do you want to enable Active Defense? (y/n): ").lower()
        if choice == 'y':
            # שולחים לו את התיקייה להגנה ואת הקובץ שצריך להשמיד
            start_guard(target_folder, USB_SHARE_FILE)

    # === פתיחה (UNLOCK) ===
    elif mode == "unlock":
        print("\n--- STARTING UNLOCK PROCESS ---")
        
        if not os.path.exists(USB_SHARE_FILE):
            print(f"CRITICAL ERROR: {USB_SHARE_FILE} is missing!")
            print("It might have been destroyed by the Active Defense system.")
            return

        with open(USB_SHARE_FILE, "r") as f:
            file_share = f.read().strip()
            
        user_pass_share = input("Enter your Password Share: ").strip()
        
        print("Combining shares...")
        master_key = recover_key(file_share, user_pass_share)
        
        if master_key:
            print("Access Granted. Decrypting...")
            perform_cryptography(target_folder, master_key, "decrypt")
            print("\nUNLOCKED SUCCESSFULLY!")
        else:
            print("\nERROR: Invalid password or corrupted key.")

def perform_cryptography(folder_path, key, action):
    f = Fernet(key)
    # מוסיפים את קבצי המלכודת לרשימת ההתעלמות (לא מצפינים אותם!)
    IGNORE_FILES = ["run_vault.py", "secret.key", ".DS_Store", "usb.share", 
                   "passwords.txt", "bitcoin_wallet.dat", "employee_salaries.pdf"]
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file in IGNORE_FILES or file.endswith(".py"):
                continue
            
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "rb") as d: data = d.read()
                processed = f.encrypt(data) if action=="encrypt" else f.decrypt(data)
                with open(full_path, "wb") as d: d.write(processed)
                print(f"[{action}] {file}")
            except: pass

if __name__ == "__main__":
    folder_name = "test_vault"
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    
    cmd = input("Type 'lock' or 'unlock': ").strip().lower()
    process_folder(folder_name, cmd)