# core/key_manager.py
import binascii
from cryptography.fernet import Fernet
# שינוי: מייבאים מהקובץ המקומי שיצרנו במקום מהספרייה השבורה
from core.shamir import split_secret_hex, recover_secret_hex

def create_shared_keys():
    """
    1. מייצר מפתח Master.
    2. מפצל אותו ל-2 חלקים באמצעות המימוש המקומי שלנו.
    """
    # יצירת מפתח
    master_key = Fernet.generate_key()
    
    # המרה ל-Hex
    master_key_hex = binascii.hexlify(master_key).decode('utf-8')
    
    # פיצול (דורש 2 מתוך 2)
    shares = split_secret_hex(master_key_hex, 2, 2)
    
    return shares[0], shares[1]

def recover_key(share_file, share_password):
    """
    משחזר את המפתח מהחלקים
    """
    try:
        shares = [share_file, share_password]
        # שחזור באמצעות הקובץ המקומי
        recovered_hex = recover_secret_hex(shares)
        
        # המרה חזרה לפורמט של Fernet
        master_key = binascii.unhexlify(recovered_hex)
        return master_key
        
    except Exception as e:
        print(f"Error recovering key: {e}")
        return None