import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Ensure tables exist (run once)
cursor.execute('''CREATE TABLE IF NOT EXISTS Department (
    D_ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Clinic (
    C_ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, address TEXT, FK_D_ID INTEGER,
    FOREIGN KEY (FK_D_ID) REFERENCES Department(D_ID))''')
conn.commit()

# GUI
root = tk.Tk()
root.title("Clinic Management")

# --- Add Clinic Frame ---
frame_add = ttk.LabelFrame(root, text="Add Clinic")
frame_add.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add, text="Clinic Name:").grid(row=0, column=0, padx=5, pady=5)
clinic_name_var = tk.StringVar()
tk.Entry(frame_add, textvariable=clinic_name_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Address:").grid(row=1, column=0, padx=5, pady=5)
clinic_address_var = tk.StringVar()
tk.Entry(frame_add, textvariable=clinic_address_var).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Department:").grid(row=2, column=0, padx=5, pady=5)
dept_var = tk.StringVar()
dept_combo = ttk.Combobox(frame_add, textvariable=dept_var, state="readonly")
dept_combo.grid(row=2, column=1, padx=5, pady=5)

def refresh_departments():
    cursor.execute("SELECT D_ID, name FROM Department")
    depts = cursor.fetchall()
    dept_combo['values'] = [f"{d[0]} - {d[1]}" for d in depts]
    if depts:
        dept_combo.current(0)

refresh_departments()

def add_clinic():
    name = clinic_name_var.get()
    address = clinic_address_var.get()
    dept = dept_var.get()
    if not name or not dept:
        messagebox.showerror("Error", "Please enter all fields.")
        return
    dept_id = int(dept.split(" - ")[0])
    cursor.execute("INSERT INTO Clinic (Name, address, FK_D_ID) VALUES (?, ?, ?)", (name, address, dept_id))
    conn.commit()
    messagebox.showinfo("Success", "Clinic added!")
    clinic_name_var.set("")
    clinic_address_var.set("")
    refresh_clinics()

tk.Button(frame_add, text="Add Clinic", command=add_clinic).grid(row=3, column=0, columnspan=2, pady=10)

# --- View Clinics Frame ---
frame_view = ttk.LabelFrame(root, text="All Clinics")
frame_view.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("C_ID", "Name", "Address", "Department")
tree = ttk.Treeview(frame_view, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

def refresh_clinics():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('''SELECT Clinic.C_ID, Clinic.Name, Clinic.address, Department.name
                      FROM Clinic LEFT JOIN Department ON Clinic.FK_D_ID = Department.D_ID''')
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

refresh_clinics()

# --- Add Department Section (for demo/testing) ---
frame_dept = ttk.LabelFrame(root, text="Add Department (for testing)")
frame_dept.pack(fill="x", padx=10, pady=5)
dept_name_var = tk.StringVar()
tk.Entry(frame_dept, textvariable=dept_name_var).pack(side="left", padx=5)
def add_dept():
    cursor.execute("INSERT INTO Department (name) VALUES (?)", (dept_name_var.get(),))
    conn.commit()
    dept_name_var.set("")
    refresh_departments()
tk.Button(frame_dept, text="Add Department", command=add_dept).pack(side="left", padx=5)

root.mainloop()