import os
import binascii
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def generate_key():
    return os.urandom(32)

def encrypt(text, key):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_text = iv + encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_text

def decrypt(encrypted_text, key):
    iv = encrypted_text[:16]
    encrypted_data = encrypted_text[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode()

class EncryptionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Encryption Application")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background="#f0f0f0", foreground='#333333')
        self.style.configure('TNotebook.Tab', background='#cccccc', foreground='#333333', padding=[5, 2])
        self.style.map('TNotebook.Tab', background=[('selected', '#ffffff')])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.key_tab = ttk.Frame(self.notebook)
        self.encrypt_tab = ttk.Frame(self.notebook)
        self.decrypt_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.key_tab, text='Generate Key')
        self.notebook.add(self.encrypt_tab, text='Encrypt Text')
        self.notebook.add(self.decrypt_tab, text='Decrypt Text')

        self.create_key_tab()
        self.create_encrypt_tab()
        self.create_decrypt_tab()

        self.encryption_key = None

        self.iconphoto(False, tk.PhotoImage(file='encryption.png'))

    def create_key_tab(self):
        self.key_label = ttk.Label(self.key_tab, text="Encryption Key (hex):", background="#f0f0f0")
        self.key_label.pack(pady=10)

        self.key_text = scrolledtext.ScrolledText(self.key_tab, wrap=tk.WORD, height=4)
        self.key_text.pack(padx=10, pady=10)

        self.generate_key_button = ttk.Button(self.key_tab, text="Generate Key", command=self.generate_key_action)
        self.generate_key_button.pack(pady=10)

    def generate_key_action(self):
        self.encryption_key = generate_key()
        self.key_text.delete(1.0, tk.END)
        self.key_text.insert(tk.END, self.encryption_key.hex())

    def create_encrypt_tab(self):
        self.encrypt_label = ttk.Label(self.encrypt_tab, text="Enter text to encrypt:", background="#f0f0f0")
        self.encrypt_label.pack(pady=10)

        self.encrypt_input = scrolledtext.ScrolledText(self.encrypt_tab, wrap=tk.WORD, height=4)
        self.encrypt_input.pack(padx=10, pady=10)

        self.encrypt_button = ttk.Button(self.encrypt_tab, text="Encrypt", command=self.encrypt_action)
        self.encrypt_button.pack(pady=10)

        self.encrypted_text_label = ttk.Label(self.encrypt_tab, text="Encrypted Text (hex):", background="#f0f0f0")
        self.encrypted_text_label.pack(pady=10)

        self.encrypted_text = scrolledtext.ScrolledText(self.encrypt_tab, wrap=tk.WORD, height=4)
        self.encrypted_text.pack(padx=10, pady=10)

    def encrypt_action(self):
        plaintext = self.encrypt_input.get(1.0, tk.END).strip()
        if not self.encryption_key:
            messagebox.showerror("Error", "Please generate an encryption key first.")
            return
        encrypted_text = encrypt(plaintext, self.encryption_key)
        self.encrypted_text.delete(1.0, tk.END)
        self.encrypted_text.insert(tk.END, binascii.hexlify(encrypted_text).decode())

    def create_decrypt_tab(self):
        self.decrypt_label = ttk.Label(self.decrypt_tab, text="Enter encrypted text (hex):", background="#f0f0f0")
        self.decrypt_label.pack(pady=10)

        self.decrypt_input = scrolledtext.ScrolledText(self.decrypt_tab, wrap=tk.WORD, height=4)
        self.decrypt_input.pack(padx=10, pady=10)

        self.decrypt_key_label = ttk.Label(self.decrypt_tab, text="Enter encryption key (hex):", background="#f0f0f0")
        self.decrypt_key_label.pack(pady=10)

        self.decrypt_key_input = scrolledtext.ScrolledText(self.decrypt_tab, wrap=tk.WORD, height=2)
        self.decrypt_key_input.pack(padx=10, pady=10)

        self.decrypt_button = ttk.Button(self.decrypt_tab, text="Decrypt", command=self.decrypt_action)
        self.decrypt_button.pack(pady=10)

        self.decrypted_text_label = ttk.Label(self.decrypt_tab, text="Decrypted Text:", background="#f0f0f0")
        self.decrypted_text_label.pack(pady=10)

        self.decrypted_text = scrolledtext.ScrolledText(self.decrypt_tab, wrap=tk.WORD, height=4)
        self.decrypted_text.pack(padx=10, pady=10)

    def decrypt_action(self):
        encrypted_text_hex = self.decrypt_input.get(1.0, tk.END).strip()
        key_hex = self.decrypt_key_input.get(1.0, tk.END).strip()
        try:
            encrypted_text = binascii.unhexlify(encrypted_text_hex)
            key = binascii.unhexlify(key_hex)
            decrypted_text = decrypt(encrypted_text, key)
            self.decrypted_text.delete(1.0, tk.END)
            self.decrypted_text.insert(tk.END, decrypted_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = EncryptionApp()
    app.mainloop()
