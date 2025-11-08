#!/usr/bin/env python3
# RSA Encryption, Decryption, Signature, and Verification
# Author: Gilman (Modified from StackOverflow CC BY-SA 3.0 example)
# Date: 2025-11-08

import os
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto import Random

KEY_SIZE = 2048
PRIVATE_KEY_FILE = "private_key.pem"
PUBLIC_KEY_FILE = "public_key.pem"

# ===================== KEY MANAGEMENT ======================
def generate_keys():
    """Generate RSA public/private key pair and save to files"""
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        print("[+] Keys already exist.")
        return
    print("[*] Generating RSA key pair...")
    start_time = time.time()
    random_generator = Random.new().read
    key = RSA.generate(KEY_SIZE, random_generator)
    elapsed_time = time.time() - start_time

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_key)
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_key)

    print(f"[+] RSA keys generated ({KEY_SIZE} bits).")
    print(f"    Time taken: {elapsed_time:.6f}s ({KEY_SIZE/elapsed_time:.2f} bits/sec)\n")


def load_keys():
    """Load RSA keys from files"""
    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = RSA.import_key(f.read())
    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = RSA.import_key(f.read())
    return private_key, public_key


# ===================== ENCRYPTION / DECRYPTION ======================
def rsa_encrypt(input_file, output_file, public_key):
    """Encrypt file contents with RSA public key"""
    with open(input_file, "rb") as f:
        plaintext = f.read()

    cipher = PKCS1_OAEP.new(public_key)
    start_time = time.time()
    ciphertext = cipher.encrypt(plaintext)
    elapsed_time = time.time() - start_time

    with open(output_file, "wb") as f:
        f.write(ciphertext)

    bits = len(plaintext) * 8
    print(f"[+] Encrypted data saved to {output_file}")
    print(f"    Time taken: {elapsed_time:.6f}s ({bits/elapsed_time:.2f} bits/sec)\n")


def rsa_decrypt(input_file, private_key):
    """Decrypt file contents with RSA private key"""
    with open(input_file, "rb") as f:
        ciphertext = f.read()

    cipher = PKCS1_OAEP.new(private_key)
    start_time = time.time()
    plaintext = cipher.decrypt(ciphertext)
    elapsed_time = time.time() - start_time

    bits = len(plaintext) * 8
    print("[+] Decrypted content:")
    print(plaintext.decode(errors="ignore"))
    print(f"    Time taken: {elapsed_time:.6f}s ({bits/elapsed_time:.2f} bits/sec)\n")


# ===================== SIGN / VERIFY ======================
def rsa_sign(input_file, signature_file, private_key):
    """Generate RSA signature for a file"""
    with open(input_file, "rb") as f:
        data = f.read()

    h = SHA256.new(data)
    start_time = time.time()
    signature = pkcs1_15.new(private_key).sign(h)
    elapsed_time = time.time() - start_time

    with open(signature_file, "wb") as f:
        f.write(signature)

    bits = len(data) * 8
    print(f"[+] Signature saved to {signature_file}")
    print(f"    Time taken: {elapsed_time:.6f}s ({bits/elapsed_time:.2f} bits/sec)\n")


def rsa_verify(input_file, signature_file, public_key):
    """Verify RSA signature of a file"""
    with open(input_file, "rb") as f:
        data = f.read()
    with open(signature_file, "rb") as f:
        signature = f.read()

    h = SHA256.new(data)
    start_time = time.time()
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        elapsed_time = time.time() - start_time
        print("[+] Signature is VALID.")
    except (ValueError, TypeError):
        elapsed_time = time.time() - start_time
        print("[-] Signature is INVALID.")
    bits = len(data) * 8
    print(f"    Time taken: {elapsed_time:.6f}s ({bits/elapsed_time:.2f} bits/sec)\n")



# ===================== MENU ======================
def main():
    generate_keys()
    private_key, public_key = load_keys()

    while True:
        print("=== RSA Command-Line Tool ===")
        print("1) RSA Encryption")
        print("2) RSA Decryption")
        print("3) RSA Signature")
        print("4) RSA Signature Verification")
        print("5) Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            infile = input("Enter input file name: ").strip()
            outfile = input("Enter output (encrypted) file name: ").strip()
            rsa_encrypt(infile, outfile, public_key)
        elif choice == "2":
            infile = input("Enter encrypted file name: ").strip()
            rsa_decrypt(infile, private_key)
        elif choice == "3":
            infile = input("Enter file name to sign: ").strip()
            sigfile = input("Enter signature file name: ").strip()
            rsa_sign(infile, sigfile, private_key)
        elif choice == "4":
            infile = input("Enter file name to verify: ").strip()
            sigfile = input("Enter signature file name: ").strip()
            rsa_verify(infile, sigfile, public_key)
        elif choice == "5":
            infile = input("Enter file name to hash: ").strip()
            sha256_hash(infile)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
