import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pint

def fetch_units():
    ureg = pint.UnitRegistry()
    units = [str(unit) for unit in ureg]
    return units

def get_compatible_units(unit):
    ureg = pint.UnitRegistry()
    try:
        input_quantity = ureg(unit)
        base_unit = input_quantity.dimensionality
        compatible_units = [str(u) for u in ureg if ureg(u).dimensionality == base_unit]
        return compatible_units
    except Exception as e:
        print(f"Error fetching compatible units: {e}")
        return []

def convert_units(value, from_unit, to_unit):
    ureg = pint.UnitRegistry()
    from_quantity = value * ureg(from_unit)
    to_quantity = from_quantity.to(ureg(to_unit))
    return to_quantity.magnitude

def update_compatible_units(event):
    from_unit = from_unit_var.get().strip().lower()
    compatible_units = get_compatible_units(from_unit)
    to_unit_var.set('')
    to_unit_combobox['values'] = compatible_units

def perform_conversion():
    try:
        value = float(value_entry.get())
        from_unit = from_unit_var.get().strip().lower()
        to_unit = to_unit_var.get().strip().lower()
        
        if from_unit and to_unit:
            result = convert_units(value, from_unit, to_unit)
            result_text = f"{value} {from_unit} = {result:.4f} {to_unit}"
            result_label.config(text=result_text)
            add_to_history(result_text)
            animate_result_label()
        else:
            messagebox.showerror("Error", "Please select valid units.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to perform conversion: {e}")

def add_to_history(conversion):
    history_text.config(state=tk.NORMAL)
    history_text.insert(tk.END, conversion + '\n')
    history_text.config(state=tk.DISABLED)

def clear_fields():
    value_entry.delete(0, tk.END)
    from_unit_var.set('')
    to_unit_var.set('')
    result_label.config(text='')

def save_history():
    with open("conversion_history.txt", "w") as f:
        history_text.config(state=tk.NORMAL)
        f.write(history_text.get("1.0", tk.END))
        history_text.config(state=tk.DISABLED)
    messagebox.showinfo("Save History", "History saved to conversion_history.txt")

def show_about():
    messagebox.showinfo("About", "Unit Converter v1.0")

def animate_result_label():
    def blink():
        current_color = result_label.cget("foreground")
        next_color = "red" if current_color == "blue" else "blue"
        result_label.config(foreground=next_color)
        root.after(500, blink)
    blink()

def filter_units_combobox(event, combobox, units_list):
    typed = combobox.get().lower()
    filtered_units = [unit for unit in units_list if typed in unit.lower()]
    combobox['values'] = filtered_units

units = fetch_units()

root = tk.Tk()
root.title("Unit Converter")

root.iconbitmap('icon.ico')

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = ttk.Style()
style.configure("TFrame", background="#e0f7fa")
style.configure("TLabel", background="#e0f7fa", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TCombobox", font=("Helvetica", 12))

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save History", command=save_history)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

ttk.Label(mainframe, text="Value:").grid(row=0, column=0, sticky=tk.W)
value_entry = ttk.Entry(mainframe, width=10)
value_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="From unit:").grid(row=1, column=0, sticky=tk.W)
from_unit_var = tk.StringVar()
from_unit_combobox = ttk.Combobox(mainframe, textvariable=from_unit_var)
from_unit_combobox['values'] = units
from_unit_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))
from_unit_combobox.bind('<<ComboboxSelected>>', update_compatible_units)
from_unit_combobox.bind('<KeyRelease>', lambda event: filter_units_combobox(event, from_unit_combobox, units))

ttk.Label(mainframe, text="To unit:").grid(row=2, column=0, sticky=tk.W)
to_unit_var = tk.StringVar()
to_unit_combobox = ttk.Combobox(mainframe, textvariable=to_unit_var)
to_unit_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E))
to_unit_combobox.bind('<KeyRelease>', lambda event: filter_units_combobox(event, to_unit_combobox, units))

convert_button = ttk.Button(mainframe, text="Convert", command=perform_conversion)
convert_button.grid(row=3, column=0, columnspan=2)

clear_button = ttk.Button(mainframe, text="Clear", command=clear_fields)
clear_button.grid(row=4, column=0, columnspan=2)
result_label = ttk.Label(mainframe, text="", font=("Helvetica", 16), foreground="blue")
result_label.grid(row=5, column=0, columnspan=2)
ttk.Label(mainframe, text="Conversion History:").grid(row=6, column=0, columnspan=2)
history_text = scrolledtext.ScrolledText(mainframe, state=tk.DISABLED, width=40, height=10, wrap=tk.WORD)
history_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
root.configure(bg="#e0f7fa")

root.mainloop()
