import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk

def get_user_preferences():
    length = length_var.get()
    include_uppercase = uppercase_var.get()
    include_lowercase = lowercase_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()

    return length, include_uppercase, include_lowercase, include_digits, include_special

def generate_password(length, include_uppercase, include_lowercase, include_digits, include_special):
    character_pool = ''
    if include_uppercase:
        character_pool += string.ascii_uppercase
    if include_lowercase:
        character_pool += string.ascii_lowercase
    if include_digits:
        character_pool += string.digits
    if include_special:
        character_pool += string.punctuation

    if not character_pool:
        raise ValueError("No character types selected for password generation.")

    password = []
    if include_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if include_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if include_digits:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice(string.punctuation))

    while len(password) < length:
        password.append(random.choice(character_pool))

    random.shuffle(password)
    return ''.join(password)

def on_generate_password():
    try:
        length, include_uppercase, include_lowercase, include_digits, include_special = get_user_preferences()
        if length <= 0:
            messagebox.showerror("Error", "Password length must be a positive integer.")
            return

        password = generate_password(length, include_uppercase, include_lowercase, include_digits, include_special)
        result_var.set(password)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size)
    return ImageTk.PhotoImage(image)

style = Style(theme="darkly")
root = style.master
root.title("Password Generator")
try:
    root.iconphoto(False, tk.PhotoImage(file="password_generator.png"))
except Exception as e:
    messagebox.showerror("Error", f"Failed to load icon: {e}")

length_var = tk.IntVar()
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()
result_var = tk.StringVar()

style.configure('TLabel', foreground='white')
style.configure('TButton', foreground='white')
style.configure('TCheckbutton', foreground='white')
style.configure('TEntry', foreground='white')


mainframe = ttk.Frame(root, padding="10 10 10 10", style="primary.TFrame")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon_size = (20, 20)
icon_generate = resize_image("generate.png", icon_size)  

ttk.Label(mainframe, text="Length:", compound="left", style="secondary.TLabel").grid(column=0, row=0, sticky=tk.W)
length_entry = ttk.Entry(mainframe, textvariable=length_var, style="info.TEntry")
length_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
length_entry.focus()

ttk.Checkbutton(mainframe, text="Include Uppercase", variable=uppercase_var, style="success.TCheckbutton").grid(column=0, row=1, sticky=tk.W)
ttk.Checkbutton(mainframe, text="Include Lowercase", variable=lowercase_var, style="success.TCheckbutton").grid(column=0, row=2, sticky=tk.W)
ttk.Checkbutton(mainframe, text="Include Digits", variable=digits_var, style="success.TCheckbutton").grid(column=0, row=3, sticky=tk.W)
ttk.Checkbutton(mainframe, text="Include Special Characters", variable=special_var, style="success.TCheckbutton").grid(column=0, row=4, sticky=tk.W)

ttk.Button(mainframe, text="Generate Password", command=on_generate_password, image=icon_generate, compound="left", style="warning.TButton").grid(column=0, row=5, columnspan=2, pady=10)

ttk.Label(mainframe, text="Generated Password:", style="secondary.TLabel").grid(column=0, row=6, sticky=tk.W)
result_entry = ttk.Entry(mainframe, textvariable=result_var, state='readonly', style="info.TEntry")
result_entry.grid(column=1, row=6, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
