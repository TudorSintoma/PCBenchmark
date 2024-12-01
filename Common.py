import tkinter as tk
from tkinter import Scrollbar, Toplevel, ttk
import threading

sieve_is_running = threading.Event()
aritm_is_running = threading.Event()
logic_is_running = threading.Event()
data_is_running = threading.Event()
ram_is_running = threading.Event()

sieve_is_running.clear()
aritm_is_running.clear()
logic_is_running.clear()
data_is_running.clear()
ram_is_running.clear()


def display_scrollable_message(title, content):
    msg_window = Toplevel()
    msg_window.title(title)
    msg_window.geometry("600x400")

    tree = ttk.Treeview(msg_window, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(msg_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    lines = content.strip().split('\n')
    headers = lines[0].split(',')

    tree["columns"] = headers
    for header in headers:
        tree.column(header, anchor="center", width=100)
        tree.heading(header, text=header, anchor="center")

    for line in lines[1:]:
        values = line.split(',')
        tree.insert("", "end", values=values)

    for column in tree["columns"]:
        tree.column(column, anchor="center", width=100, minwidth=30)

def set_sieve_running(state: bool):
    if state:
        sieve_is_running.set()
    else:
        sieve_is_running.clear()

def set_aritm_running(state: bool):
    if state:
        aritm_is_running.set()
    else:
        aritm_is_running.clear()

def set_logic_running(state: bool):
    if state:
        logic_is_running.set()
    else:
        logic_is_running.clear()

def set_data_running(state: bool):
    if state:
        data_is_running.set()
    else:
        data_is_running.clear()

def set_ram_running(state: bool):
    if state:
        ram_is_running.set()
    else:
        ram_is_running.clear()