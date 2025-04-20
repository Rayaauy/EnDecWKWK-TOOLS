import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from colorama import Fore, Style, init
from tabulate import tabulate

# Inisialisasi colorama
init(autoreset=True)

class CryptoTools:
    @staticmethod
    def caesar_cipher_encrypt(text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            else:
                encrypted_text += char
        return encrypted_text

    @staticmethod
    def caesar_cipher_decrypt(text, shift):
        return CryptoTools.caesar_cipher_encrypt(text, -shift)

    @staticmethod
    def vigenere_cipher_encrypt(text, key):
        encrypted_text = ""
        key_length = len(key)
        for i, char in enumerate(text):
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                key_char = key[i % key_length].upper() if char.isupper() else key[i % key_length].lower()
                key_shift = ord(key_char) - shift_base
                encrypted_text += chr((ord(char) - shift_base + key_shift) % 26 + shift_base)
            else:
                encrypted_text += char
        return encrypted_text

    @staticmethod
    def vigenere_cipher_decrypt(text, key):
        decrypted_text = ""
        key_length = len(key)
        for i, char in enumerate(text):
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                key_char = key[i % key_length].upper() if char.isupper() else key[i % key_length].lower()
                key_shift = ord(key_char) - shift_base
                decrypted_text += chr((ord(char) - shift_base - key_shift) % 26 + shift_base)
            else:
                decrypted_text += char
        return decrypted_text

    @staticmethod
    def base64_encode(text):
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def base64_decode(encoded_text):
        return base64.b64decode(encoded_text).decode()

    @staticmethod
    def xor_cipher_encrypt(text, key):
        key_bytes = key.encode()
        text_bytes = text.encode()
        encrypted_bytes = bytes([text_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(text_bytes))])
        return encrypted_bytes.hex()

    @staticmethod
    def xor_cipher_decrypt(hex_text, key):
        key_bytes = key.encode()
        encrypted_bytes = bytes.fromhex(hex_text)
        decrypted_bytes = bytes([encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])
        return decrypted_bytes.decode()

    @staticmethod
    def aes_encrypt(key, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext

    @staticmethod
    def aes_decrypt(key, ciphertext):
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()


def display_wkwk_art():
    wkwk_art = """   
    {}  ░██╗░░░░░░░██╗██╗░░██╗░██╗░░░░░░░██╗██╗░░██╗
    {}  ░██║░░██╗░░██║██║░██╔╝░██║░░██╗░░██║██║░██╔╝
    {}  ░╚██╗████╗██╔╝█████═╝░░╚██╗████╗██╔╝█████═╝░
    {}  ░░████╔═████║░██╔═██╗░░░████╔═████║░██╔═██╗░
    {}  ░░╚██╔╝░╚██╔╝░██║░╚██╗░░╚██╔╝░╚██╔╝░██║░╚██╗
    {}  ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝  
    """.format(Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN)
    print(wkwk_art)


def display_menu():
    print(Fore.CYAN + "╔════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                     ENCRYPTION & DECRYPTION TOOLS              ║")
    print(Fore.CYAN + "╠════════════════════════════════════════════════════════════════╣")
    print(Fore.YELLOW + "║ 1. Caesar Cipher                                               ║")
    print(Fore.YELLOW + "║ 2. Vigenère Cipher                                             ║")
    print(Fore.YELLOW + "║ 3. Base64 Encoding/Decoding                                    ║")
    print(Fore.YELLOW + "║ 4. XOR Cipher                                                  ║")
    print(Fore.YELLOW + "║ 5. AES Encryption/Decryption                                   ║")
    print(Fore.YELLOW + "║ 0. Exit                                                        ║")
    print(Fore.CYAN + "╚════════════════════════════════════════════════════════════════╝")


def main():
    while True:
        display_wkwk_art()
        display_menu()
        choice = input(Fore.GREEN + "Enter your choice: ")

        if choice == "1":
            print(Fore.MAGENTA + "\n--- CAESAR CIPHER ---")
            action = input("Choose action (1 for Encrypt, 2 for Decrypt): ")
            text = input("Enter text: ")
            shift = int(input("Enter shift value: "))
            if action == "1":
                result = CryptoTools.caesar_cipher_encrypt(text, shift)
                print(tabulate([["Encrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            elif action == "2":
                result = CryptoTools.caesar_cipher_decrypt(text, shift)
                print(tabulate([["Decrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "Invalid action. Please choose 1 or 2.")

        elif choice == "2":
            print(Fore.MAGENTA + "\n--- VIGENÈRE CIPHER ---")
            action = input("Choose action (1 for Encrypt, 2 for Decrypt): ")
            text = input("Enter text: ")
            key = input("Enter key: ")
            if action == "1":
                result = CryptoTools.vigenere_cipher_encrypt(text, key)
                print(tabulate([["Encrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            elif action == "2":
                result = CryptoTools.vigenere_cipher_decrypt(text, key)
                print(tabulate([["Decrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "Invalid action. Please choose 1 or 2.")

        elif choice == "3":
            print(Fore.MAGENTA + "\n--- BASE64 ENCODING/DECODING ---")
            action = input("Choose action (1 for Encode, 2 for Decode): ")
            if action == "1":
                text = input("Enter text to encode: ")
                result = CryptoTools.base64_encode(text)
                print(tabulate([["Encoded", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            elif action == "2":
                encoded_text = input("Enter text to decode: ")
                result = CryptoTools.base64_decode(encoded_text)
                print(tabulate([["Decoded", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "Invalid action. Please choose 1 or 2.")

        elif choice == "4":
            print(Fore.MAGENTA + "\n--- XOR CIPHER ---")
            action = input("Choose action (1 for Encrypt, 2 for Decrypt): ")
            if action == "1":
                text = input("Enter text to encrypt: ")
                key = input("Enter key: ")
                result = CryptoTools.xor_cipher_encrypt(text, key)
                print(tabulate([["Encrypted (Hex)", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            elif action == "2":
                hex_text = input("Enter hex text to decrypt: ")
                key = input("Enter key: ")
                result = CryptoTools.xor_cipher_decrypt(hex_text, key)
                print(tabulate([["Decrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "Invalid action. Please choose 1 or 2.")

        elif choice == "5":
            print(Fore.MAGENTA + "\n--- AES ENCRYPTION/DECRYPTION ---")
            action = input("Choose action (1 for Encrypt, 2 for Decrypt): ")
            if action == "1":
                text = input("Enter text to encrypt: ")
                aes_key = os.urandom(32)  # Generate a random 256-bit key
                result = CryptoTools.aes_encrypt(aes_key, text)
                print(tabulate([["Encrypted (Hex)", result.hex()], ["AES Key (Hex)", aes_key.hex()]],
                               headers=["Action", "Result"], tablefmt="fancy_grid"))
            elif action == "2":
                hex_text = input("Enter hex text to decrypt: ")
                aes_key_hex = input("Enter AES key (Hex): ")
                aes_key = bytes.fromhex(aes_key_hex)
                result = CryptoTools.aes_decrypt(aes_key, bytes.fromhex(hex_text))
                print(tabulate([["Decrypted", result]], headers=["Action", "Result"], tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "Invalid action. Please choose 1 or 2.")

        elif choice == "0":
            print(Fore.RED + "Exiting the program. Goodbye!")
            print(Fore.RED + "Contact me in telegram : @belimbing_uwu")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")

        input(Fore.CYAN + "\nPress Enter to continue...")


if __name__ == "__main__":
    main()