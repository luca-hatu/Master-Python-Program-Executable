import requests
import tkinter as tk
from tkinter import ttk
import json
import os

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
FAVORITES_FILE = "favorites.json"
ICON_FILE = "exchange.ico"

def fetch_exchange_rates():
    response = requests.get(API_URL)
    data = response.json()
    return data['rates']

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency != "USD":
        amount = amount / rates[from_currency]
    return round(amount * rates[to_currency], 2)

def convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combobox.get()
        to_currency = to_currency_combobox.get()
        if not from_currency or not to_currency:
            result_label.config(text="Please select both currencies.", foreground="red")
            return
        rates = fetch_exchange_rates()
        converted_amount = convert_currency(amount, from_currency, to_currency, rates)
        result_label.config(text=f"{amount} {from_currency} = {converted_amount} {to_currency}", foreground="green")
    except ValueError:
        result_label.config(text="Invalid amount. Please enter a number.", foreground="red")

def add_to_favorites():
    from_currency = from_currency_combobox.get()
    to_currency = to_currency_combobox.get()
    if from_currency and to_currency:
        favorites.append((from_currency, to_currency))
        save_favorites()
        update_favorites_list()
    else:
        result_label.config(text="Please select both currencies to add to favorites.", foreground="red")

def delete_favorite():
    selected_index = favorites_list.curselection()
    if selected_index:
        favorites.pop(selected_index[0])
        save_favorites()
        update_favorites_list()
    else:
        result_label.config(text="Please select a favorite to delete.", foreground="red")

def save_favorites():
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f)

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    return []

def update_favorites_list():
    favorites_list.delete(0, tk.END)
    for from_currency, to_currency in favorites:
        favorites_list.insert(tk.END, f"{from_currency} -> {to_currency}")

def set_favorite(event):
    selection = favorites_list.get(favorites_list.curselection())
    from_currency, to_currency = selection.split(" -> ")
    from_currency_combobox.set(from_currency)
    to_currency_combobox.set(to_currency)

root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x450")

if os.path.exists(ICON_FILE):
    root.iconbitmap(ICON_FILE)
else:
    print(f"Icon file {ICON_FILE} not found.")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12))
style.configure("TListbox", font=("Arial", 12))

amount_label = ttk.Label(root, text="Amount:")
amount_label.grid(column=0, row=0, padx=10, pady=5, sticky='E')
amount_entry = ttk.Entry(root)
amount_entry.grid(column=1, row=0, padx=10, pady=5)

from_currency_label = ttk.Label(root, text="From Currency:")
from_currency_label.grid(column=0, row=1, padx=10, pady=5, sticky='E')
from_currency_combobox = ttk.Combobox(root, values=list(fetch_exchange_rates().keys()))
from_currency_combobox.grid(column=1, row=1, padx=10, pady=5)

to_currency_label = ttk.Label(root, text="To Currency:")
to_currency_label.grid(column=0, row=2, padx=10, pady=5, sticky='E')
to_currency_combobox = ttk.Combobox(root, values=list(fetch_exchange_rates().keys()))
to_currency_combobox.grid(column=1, row=2, padx=10, pady=5)

convert_button = ttk.Button(root, text="Convert", command=convert)
convert_button.grid(column=1, row=3, padx=10, pady=10)

add_favorite_button = ttk.Button(root, text="Add to Favorites", command=add_to_favorites)
add_favorite_button.grid(column=1, row=4, padx=10, pady=10)

delete_favorite_button = ttk.Button(root, text="Delete Favorite", command=delete_favorite)
delete_favorite_button.grid(column=1, row=5, padx=10, pady=10)

result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=6, columnspan=2, pady=10)

favorites_label = ttk.Label(root, text="Favorites:")
favorites_label.grid(column=0, row=7, padx=10, pady=5, sticky='E')
favorites_list = tk.Listbox(root, font=("Arial", 12), height=6)
favorites_list.grid(column=1, row=7, padx=10, pady=5)
favorites_list.bind("<<ListboxSelect>>", set_favorite)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=favorites_list.yview)
scrollbar.grid(column=2, row=7, sticky="NSW", pady=5)
favorites_list.config(yscrollcommand=scrollbar.set)

favorites = load_favorites()
update_favorites_list()

root.mainloop()

