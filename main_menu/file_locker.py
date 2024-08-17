from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Key Generation", "Key generated and saved to 'secret.key'")

def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        messagebox.showinfo("Key Not Found", "No key found. Generating a new key...")
        generate_key()
        return open("secret.key", "rb").read()

def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    
    messagebox.showinfo("Encryption", f"File '{file_path}' encrypted successfully.")

def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    
    messagebox.showinfo("Decryption", f"File '{file_path}' decrypted successfully.")

def on_generate_key():
    generate_key()

def on_encrypt_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypt_file(file_path)

def on_decrypt_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        decrypt_file(file_path)

def main():
    root = tk.Tk()
    root.title("File Locker")
    try:
        root.iconphoto(False, tk.PhotoImage(file="lock.png"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load icon: {e}")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    generate_key_button = tk.Button(frame, text="Generate Key", command=on_generate_key)
    generate_key_button.grid(row=0, column=0, padx=5, pady=5)

    encrypt_file_button = tk.Button(frame, text="Encrypt File", command=on_encrypt_file)
    encrypt_file_button.grid(row=0, column=1, padx=5, pady=5)

    decrypt_file_button = tk.Button(frame, text="Decrypt File", command=on_decrypt_file)
    decrypt_file_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
