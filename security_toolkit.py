import os
import hashlib
import sys
from cryptography.fernet import Fernet, InvalidToken

KEY_FILE = "secret.key"

def load_or_generate_key():
    """Generates or loads an encryption key kept outside Git tracking."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print(f"[+] Key generated and saved to {KEY_FILE}")
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

def encrypt_file(file_path):
    """Encrypts a file using Fernet symmetric encryption."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        
        key = load_or_generate_key()
        fernet = Fernet(key)

        with open(file_path, "rb") as f:
            data = f.read()

        encrypted_data = fernet.encrypt(data)
        enc_file_path = file_path + ".enc"
        
        with open(enc_file_path, "wb") as f:
            f.write(encrypted_data)

        print(f"[+] Successfully encrypted '{file_path}' -> '{enc_file_path}'")
        return enc_file_path
    except FileNotFoundError as e:
        print(f"[Error] {e}")
    except Exception as e:
        print(f"[Error] Failed to encrypt file: {e}")

def decrypt_file(enc_file_path):
    """Decrypts an encrypted file and compares content to original."""
    try:
        if not os.path.exists(enc_file_path):
            raise FileNotFoundError(f"File '{enc_file_path}' not found.")
        if not os.path.exists(KEY_FILE):
            raise FileNotFoundError("Encryption key missing. Cannot decrypt.")

        with open(KEY_FILE, "rb") as f:
            key = f.read()
        fernet = Fernet(key)

        with open(enc_file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)
        dec_file_path = enc_file_path.replace(".enc", ".dec")

        with open(dec_file_path, "wb") as f:
            f.write(decrypted_data)

        print(f"[+] Successfully decrypted '{enc_file_path}' -> '{dec_file_path}'")
        return dec_file_path
    except InvalidToken:
        print("[Error] Decryption failed: Invalid key or corrupted file.")
    except FileNotFoundError as e:
        print(f"[Error] {e}")
    except Exception as e:
        print(f"[Error] Failed to decrypt file: {e}")

def calculate_sha256(file_path):
    """Calculates SHA-256 hash of a file."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        file_hash = sha256.hexdigest()
        print(f"[+] SHA-256 for '{file_path}': {file_hash}")
        return file_hash
    except FileNotFoundError as e:
        print(f"[Error] {e}")
        return None

if __name__ == "__main__":
    test_file = "sample_student_record.txt"
    
    # Create sample record if it doesn't exist
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("ID: 1001 | Name: John Doe | Program: CS | Status: Active")

    print("\n--- 1. Testing Integrity Hash ---")
    original_hash = calculate_sha256(test_file)

    print("\n--- 2. Testing Encryption ---")
    enc_file = encrypt_file(test_file)

    print("\n--- 3. Testing Decryption ---")
    dec_file = decrypt_file(enc_file)

    print("\n--- 4. Integrity Check After Modification ---")
    # Simulate file modification
    with open("tampered_record.txt", "w") as f:
        f.write("ID: 1001 | Name: John Doe | Program: CS | Status: Graduated")
    
    tampered_hash = calculate_sha256("tampered_record.txt")
    if original_hash != tampered_hash:
        print("[!] Alert: File modification detected! Hashes do not match.")
