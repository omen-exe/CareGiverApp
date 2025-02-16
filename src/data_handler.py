import tkinter as tk
from tkinter import ttk

def display_data_in_table(data, columns, window_title):
    """Displays data in a table format using Treeview widget."""
    window = tk.Toplevel()
    window.title(window_title)

    # Create a Treeview widget with columns
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)

    # Insert data into the treeview
    for row in data:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")