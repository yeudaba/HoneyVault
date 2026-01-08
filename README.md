# HoneyVault 🛡️
### Secure File Storage with Active Deception & Threshold Cryptography

**HoneyVault** is an advanced cybersecurity tool developed as a final project. Unlike standard encryption tools, it employs active defense mechanisms and mathematical key splitting to secure data against ransomware and physical theft.

## 🚀 Key Features
1.  **Threshold Cryptography (Shamir's Secret Sharing):**
    The master encryption key is split into two parts:
    * **Part A:** A file stored physically (simulating a USB token).
    * **Part B:** A password memorized by the user.
    * *Mathematical Guarantee:* The data cannot be recovered without BOTH parts.

2.  **Active Defense (Honeytokens):**
    The system plants decoy files (e.g., `passwords.txt`, `bitcoin_wallet.dat`) inside the vault.

3.  **Tamper Detection & Self-Destruct:**
    A background watchdog monitors the decoys. If an intruder touches a decoy file, the system **instantly deletes the physical key file**, rendering the encrypted data permanently inaccessible.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Encryption:** Fernet (AES-128)
* **Mathematics:** Custom implementation of Shamir's Secret Sharing (Lagrange Interpolation).
* **Monitoring:** `watchdog` library for file system events.
* **GUI:** `customtkinter` for a modern, dark-themed interface.

## 📦 Installation
```bash
git clone [https://github.com/YOUR_USERNAME/HoneyVault.git](https://github.com/YOUR_USERNAME/HoneyVault.git)
cd HoneyVault
pip install -r requirements.txt
python main_gui.py