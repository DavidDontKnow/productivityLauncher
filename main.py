import os
import sys
import webbrowser
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
import json


with open('data.json', 'r') as file:
    data = json.load(file)

    websites = data.get("websites", [])
    applications = data.get("applications", {})


def open_websites():
    for site in websites:
        webbrowser.open(site)

def open_apps():
    for name, path in applications.items():
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {name}: {e}")

def launch_all():
    open_websites()
    open_apps()

def edit_websites_and_apps():
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Websites and Apps")
    edit_window.geometry("500x400")

    # --- Websites ---
    tk.Label(edit_window, text="Websites").pack()
    root.attributes("-topmost", True)
    website_listbox = tk.Listbox(edit_window, height=6)
    website_listbox.pack(fill=tk.X, padx=10)

    for site in websites:
        website_listbox.insert(tk.END, site)

    def add_website():
        new_site = simpledialog.askstring("Add Website", "Enter website URL:")
        if new_site:
            websites.append(new_site)
            with open('data.json', 'w') as file:
                json.dump({"websites": websites, "applications": applications}, file)
            # Update the listbox
            website_listbox.insert(tk.END, new_site)

    def remove_website():
        selection = website_listbox.curselection()
        if selection:
            index = selection[0]
            websites.pop(index)
            with open('data.json', 'w') as file:
                json.dump({"websites": websites, "applications": applications}, file)

            website_listbox.delete(index)

    tk.Button(edit_window, text="Add Website", command=add_website).pack(pady=2)
    tk.Button(edit_window, text="Remove Selected Website", command=remove_website).pack(pady=2)

    # --- Apps ---
    tk.Label(edit_window, text="\nApplications").pack()
    app_listbox = tk.Listbox(edit_window, height=6)
    app_listbox.pack(fill=tk.X, padx=10)

    for name, path in applications.items():
        app_listbox.insert(tk.END, f"{name} => {path}")

    def add_app():
        name = simpledialog.askstring("App Name", "Enter app name:")
        path = simpledialog.askstring("App Path", "Enter full path to app:")
        if name and path:
            applications[name] = path
            app_listbox.insert(tk.END, f"{name} => {path}")
            with open('data.json', 'w') as file:
                json.dump({"websites": websites, "applications": applications}, file)

    def remove_app():
        selection = app_listbox.curselection()
        if selection:
            index = selection[0]
            key = list(applications.keys())[index]
            del applications[key]
            app_listbox.delete(index)
            with open('data.json', 'w') as file:
                json.dump({"websites": websites, "applications": applications}, file)

    tk.Button(edit_window, text="Add App", command=add_app).pack(pady=2)
    tk.Button(edit_window, text="Remove Selected App", command=remove_app).pack(pady=2)

# GUI
root = tk.Tk()
root.title("Productivity Launcher")
root.attributes("-topmost", True)

tk.Label(root, text="Productivity Launcher", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Edit Websites and Apps", command=edit_websites_and_apps, width=20).pack(pady=5)
tk.Button(root, text="Open Websites", command=open_websites, width=20).pack(pady=5)
tk.Button(root, text="Open Apps", command=open_apps, width=20).pack(pady=5)
tk.Button(root, text="Launch All", command=launch_all, width=30).pack(pady=20)

root.mainloop()
