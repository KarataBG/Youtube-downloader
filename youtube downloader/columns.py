import tkinter as tk
from tkinter import ttk
from tkinter import Message

# root window
root = tk.Tk()
root.geometry("440x900")
root.title('Login')
# root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# username
username_label = ttk.Label(root, text="Username:")
username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

username_entry = ttk.Entry(root)
username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# password
password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

password_entry = ttk.Entry(root, show="*")
password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# login button
login_button = ttk.Button(root, text="Login")
login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

# for i in range(10):
#     lab = ttk.Label(root, text=i)
#     lab.grid(column=i, row=i)
# print("A")


def cock():
    ttk.Label(root, text="AAААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА").grid(column=0, row=4, columnspan=4)
    print("V")


cock()
root.mainloop()
