# -------------------- IMPORT REQUIRED MODULES --------------------

import tkinter as tk                  # For GUI
from tkinter import messagebox        # For popup messages
import json                           # For storing contacts in JSON format
import os                             # To check if file exists

# -------------------- FILE CONFIGURATION --------------------

FILE_NAME = "contacts.json"           # File where contacts will be stored


# -------------------- LOAD CONTACTS FROM FILE --------------------

def load_contacts():
    """
    Loads contacts from JSON file.
    If file does not exist, return empty list.
    """
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


# -------------------- SAVE CONTACTS TO FILE --------------------

def save_contacts():
    """
    Saves the current contacts list to JSON file.
    """
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


# Load contacts when program starts
contacts = load_contacts()


# -------------------- CREATE MAIN WINDOW --------------------

root = tk.Tk()
root.title("Contact Management System")
root.geometry("750x550")
root.configure(bg="#e6f2ff")   # Light blue background


# -------------------- CREATE FRAMES FOR BETTER LAYOUT --------------------

# Frame for input fields
input_frame = tk.Frame(root, bg="#e6f2ff")
input_frame.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#e6f2ff")
button_frame.pack(pady=10)

# Frame for search
search_frame = tk.Frame(root, bg="#e6f2ff")
search_frame.pack(pady=10)

# Frame for contact list
list_frame = tk.Frame(root, bg="#e6f2ff")
list_frame.pack(pady=10)


# -------------------- INPUT FIELDS --------------------

# Labels and Entry widgets arranged using grid

tk.Label(input_frame, text="Name:", bg="#e6f2ff", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(input_frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Phone:", bg="#e6f2ff", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(input_frame, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Email:", bg="#e6f2ff", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(input_frame, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Address:", bg="#e6f2ff", font=("Arial", 11)).grid(row=3, column=0, padx=5, pady=5)
entry_address = tk.Entry(input_frame, width=30)
entry_address.grid(row=3, column=1, padx=5, pady=5)


# -------------------- FUNCTION TO ADD CONTACT --------------------

def add_contact():
    """
    Adds a new contact to the list.
    """
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    # Check if required fields are filled
    if name == "" or phone == "":
        messagebox.showerror("Error", "Name and Phone are required!")
        return

    # Add contact to list
    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })

    save_contacts()     # Save to file
    view_contacts()     # Refresh listbox
    clear_fields()      # Clear input fields
    messagebox.showinfo("Success", "Contact Added Successfully!")


# -------------------- FUNCTION TO VIEW CONTACTS --------------------

def view_contacts():
    """
    Displays all contacts in the listbox.
    """
    listbox.delete(0, tk.END)
    for contact in contacts:
        listbox.insert(tk.END, f"{contact['name']}  |  {contact['phone']}")


# -------------------- FUNCTION TO SEARCH CONTACT --------------------

def search_contact():
    """
    Searches contacts by name or phone.
    """
    keyword = entry_search.get().lower()
    listbox.delete(0, tk.END)

    for contact in contacts:
        if keyword in contact["name"].lower() or keyword in contact["phone"]:
            listbox.insert(tk.END, f"{contact['name']}  |  {contact['phone']}")


# -------------------- FUNCTION TO UPDATE CONTACT --------------------

def update_contact():
    """
    Updates selected contact details.
    """
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a contact to update")
        return

    index = selected[0]

    contacts[index] = {
        "name": entry_name.get(),
        "phone": entry_phone.get(),
        "email": entry_email.get(),
        "address": entry_address.get()
    }

    save_contacts()
    view_contacts()
    clear_fields()
    messagebox.showinfo("Success", "Contact Updated Successfully!")


# -------------------- FUNCTION TO DELETE CONTACT --------------------

def delete_contact():
    """
    Deletes selected contact.
    """
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a contact to delete")
        return

    index = selected[0]
    contacts.pop(index)

    save_contacts()
    view_contacts()
    clear_fields()
    messagebox.showinfo("Success", "Contact Deleted Successfully!")


# -------------------- FILL FIELDS WHEN CONTACT IS SELECTED --------------------

def fill_fields(event):
    """
    When user selects a contact from list,
    automatically fill input fields.
    """
    selected = listbox.curselection()

    if selected:
        contact = contacts[selected[0]]

        entry_name.delete(0, tk.END)
        entry_name.insert(0, contact["name"])

        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, contact["phone"])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, contact["email"])

        entry_address.delete(0, tk.END)
        entry_address.insert(0, contact["address"])


# -------------------- CLEAR INPUT FIELDS --------------------

def clear_fields():
    """
    Clears all input fields.
    """
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_search.delete(0, tk.END)


# -------------------- BUTTONS --------------------

tk.Button(button_frame, text="Add", width=15, bg="#4CAF50", fg="white", command=add_contact).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update", width=15, bg="#2196F3", fg="white", command=update_contact).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete", width=15, bg="#f44336", fg="white", command=delete_contact).grid(row=0, column=2, padx=5)


# -------------------- SEARCH SECTION --------------------

tk.Label(search_frame, text="Search (Name or Phone):", bg="#e6f2ff").grid(row=0, column=0, padx=5)

entry_search = tk.Entry(search_frame, width=30)
entry_search.grid(row=0, column=1, padx=5)

tk.Button(search_frame, text="Search", width=10, command=search_contact).grid(row=0, column=2, padx=5)


# -------------------- CONTACT LIST DISPLAY --------------------

listbox = tk.Listbox(list_frame, width=70, height=10)
listbox.pack()

listbox.bind("<<ListboxSelect>>", fill_fields)

# Show contacts when program starts
view_contacts()


# -------------------- RUN APPLICATION --------------------

root.mainloop()
