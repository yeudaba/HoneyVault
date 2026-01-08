# core/deception.py
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# רשימת המלכודות
DECOY_NAMES = ["passwords.txt", "bitcoin_wallet.dat", "employee_salaries.pdf"]
FAKE_CONTENT = "Gmail: user@gmail.com / Pass: 123456\nBank: 1029384"

def create_decoys(target_folder):
    """יוצר את קבצי המלכודת"""
    created = []
    for name in DECOY_NAMES:
        full_path = os.path.join(target_folder, name)
        if not os.path.exists(full_path):
            with open(full_path, "w") as f:
                f.write(FAKE_CONTENT)
            created.append(name)
    if created:
        print(f"[DECEPTION] Honeytokens deployed: {created}")

class HoneyHandler(FileSystemEventHandler):
    def __init__(self, key_file_path, stop_event):
        self.key_file_path = key_file_path # הנתיב לקובץ שצריך להשמיד
        self.stop_event = stop_event

    def on_modified(self, event):
        # בדיקה אם נגעו בקובץ מלכודת
        if os.path.basename(event.src_path) in DECOY_NAMES:
            print("\n" + "!"*60)
            print(f" [ALERT] INTRUSION DETECTED on {event.src_path}!")
            print(" [DEFENSE] EXECUTING SELF-DESTRUCT PROTOCOL...")
            
            # --- המחיקה האמיתית ---
            if os.path.exists(self.key_file_path):
                os.remove(self.key_file_path)
                print(f" [DELETED] Key file '{self.key_file_path}' has been destroyed.")
                print(" [STATUS] The data is now permanently inaccessible.")
            else:
                print(" [INFO] Key file already gone.")
            
            print("!"*60 + "\n")
            self.stop_event.set() # עוצר את המערכת

def start_guard(target_folder, key_file_to_protect):
    """מתחיל את השמירה"""
    create_decoys(target_folder)
    
    print(f"\n--- 🛡️  ACTIVE DEFENSE SYSTEM ONLINE 🛡️  ---")
    print(f"Monitoring '{target_folder}' for intruders...")
    print(f"Protecting key file: '{key_file_to_protect}'")
    print("Press Ctrl+C to stop surveillance.\n")
    
    stop_event = threading.Event()
    # כאן אנחנו שולחים לו את שם קובץ המפתח כדי שידע מה למחוק
    handler = HoneyHandler(key_file_to_protect, stop_event)
    
    observer = Observer()
    observer.schedule(handler, target_folder, recursive=False)
    observer.start()
    
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        print("\n[SYSTEM] Surveillance stopped.")