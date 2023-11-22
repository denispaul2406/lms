from tkinter import *
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter.ttk import Style, Button

ADMIN_PASSWORD = "admin"  # Set the admin password

def authenticate_admin():
    password = sd.askstring("Admin Authentication", "Enter Admin Password:", show='*')
    if password == ADMIN_PASSWORD:
        open_admin_window()
    else:
        mb.showerror("Authentication Failed", "Incorrect password!")

def open_admin_window():
    root.destroy()  # Hide the login window
    from admin import admin 
    admin()  # Call the admin function from bookwise.py

def open_student_window():
    root.destroy()  # Hide the login window
    from student import student
    student()  # Call the student function from bookwise.py

root = Tk()
root.title('Login')
root.geometry('720x300')

# Label for the title
Label(root, text='Login', font=("Arial", 18)).pack(pady=20)

# Applying a theme using ttk Style
style = Style()
style.theme_use('clam')  # You can change 'clam' to other available themes like 'default', 'alt', etc.

# Configure the style for buttons
style.configure('TButton', font=('Arial', 12), width=15)

# Button to open the Admin window with authentication
admin_button = Button(root, text='Admin', style='TButton', command=authenticate_admin)
admin_button.pack(pady=10)

# Button to open the Student window
student_button = Button(root, text='Student', style='TButton', command=open_student_window)
student_button.pack(pady=10)

root.mainloop()
