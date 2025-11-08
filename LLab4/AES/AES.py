#!/usr/bin/env python3
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_FILE = "aes_key.bin"

# Generate AES key (256-bit) and store
def generate_key():
    key = get_random_bytes(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"[+] AES key generated and saved to {KEY_FILE}")
    return key

# Load AES key from file
def load_key():
    if not os.path.exists(KEY_FILE):
        print("[-] AES key not found. Generating new key...")
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    return key

# AES encryption
def encrypt_file(key, input_file, output_file):
    with open(input_file, "rb") as f:
        plaintext = f.read()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    start_time = time.time()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    elapsed_time = time.time() - start_time

    with open(output_file, "wb") as f:
        f.write(iv + ciphertext)

    bits = len(plaintext) * 8
    print(f"[+] Encrypted and saved to {output_file}")
    print(f"    Time taken: {elapsed_time:.6f}s ({bits / elapsed_time:.2f} bits/sec)")

# AES decryption
def decrypt_file(key, input_file):
    with open(input_file, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    start_time = time.time()
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elapsed_time = time.time() - start_time

    bits = len(decrypted_data) * 8
    print(f"[+] Decrypted content:\n{decrypted_data.decode(errors='ignore')}")
    print(f"    Time taken: {elapsed_time:.6f}s ({bits / elapsed_time:.2f} bits/sec)")

# Command-line menu
def main():
    key = load_key()

    while True:
        print("\n=== AES Command-Line Tool ===")
        print("1) Encrypt a file")
        print("2) Decrypt a file")
        print("3) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            infile = input("Enter input file name: ").strip()
            outfile = input("Enter output (encrypted) file name: ").strip()
            encrypt_file(key, infile, outfile)
        elif choice == "2":
            infile = input("Enter encrypted file name: ").strip()
            decrypt_file(key, infile)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
