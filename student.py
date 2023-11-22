# Importing necessary modules
import sqlite3  # For working with SQLite database
from tkinter import *  # For creating the graphical user interface
import tkinter.ttk as ttk  # For additional Tkinter widgets
import tkinter.messagebox as mb  # For displaying message boxes
import tkinter.simpledialog as sd  # For simple dialogs
from tkinter.simpledialog import askstring  # For asking user input


# Connecting to the SQLite database
connector = sqlite3.connect('library.sqlite')  # 'library.sqlite' is the database file name
cursor = connector.cursor()  # Creating a cursor object for executing SQL queries

def display_records():
    global connector, cursor  # Using global variables for database connection and cursor
    global tree  # Assuming 'tree' is a Tkinter treeview widget

    # Clearing existing records from the treeview
    tree.delete(*tree.get_children())

    # Executing a SQL query to retrieve all records from the 'Library' table
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()

    # Inserting retrieved records into the treeview
    for records in data:
        tree.insert('', END, values=records)



def open_search_dialog():
    # Asking the user for a search query using a simple dialog
    search_term = askstring('Search', 'Enter your search query:')
    # Checking if a search term is provided
    if search_term:
        # Initiating the search with the entered search term
        search_records(search_term)


# Function to search records in the 'Library' table based on a search term
def search_records(search_term):
    global connector, tree
    # Clearing existing records from the treeview
    tree.delete(*tree.get_children())
    if search_term:
        # Constructing a SQL query with LIKE clauses for various columns
        query = f'''
            SELECT * FROM Library 
            WHERE 
                book_name LIKE '%{search_term}%' 
                OR book_id LIKE '%{search_term}%' 
                OR author_name LIKE '%{search_term}%'
                OR book_status LIKE '%{search_term}%'
                OR card_id LIKE '%{search_term}%'
                OR category LIKE '%{search_term}%'
                OR asset_code LIKE '%{search_term}%'
                OR department LIKE '%{search_term}%'
                OR subject LIKE '%{search_term}%'
                OR edition LIKE '%{search_term}%'
                OR date_year LIKE '%{search_term}%'
                OR call_no LIKE '%{search_term}%'
                OR publisher LIKE '%{search_term}%'
                OR place LIKE '%{search_term}%'
                OR isbn LIKE '%{search_term}%'
                OR price LIKE '%{search_term}%'
                OR bill_date LIKE '%{search_term}%'
                OR vendor LIKE '%{search_term}%'
                OR pages LIKE '%{search_term}%'
                OR num_copies LIKE '%{search_term}%'
        '''
    else:
        # If no search term provided, retrieve all records
        query = 'SELECT * FROM Library'
    # Executing the constructed query
    curr = connector.execute(query)
    data = curr.fetchall()
    # Inserting retrieved records into the treeview
    for records in data:
        tree.insert('', END, values=records)

# Color variables for frames and buttons
lf_bg = 'LightSkyBlue'  # Left Frame Background Color
rtf_bg = 'DeepSkyBlue'  # Right Top Frame Background Color
rbf_bg = 'DodgerBlue'  # Right Bottom Frame Background Color
btn_hlb_bg = 'SteelBlue'  # Background color for Head Labels and Buttons

# Font styles for labels, entry widgets, and buttons
lbl_font = ('Georgia', 13)  # Font for all labels
entry_font = ('Times New Roman', 12)  # Font for all Entry widgets
btn_font = ('Gill Sans MT', 13)  # Font for buttons

# Creating the main Tkinter window
root = Tk()

# Setting the title of the window
root.title('Library Management System')

# Getting the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Creating a label at the top of the window
Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)


# Right top frame for additional user interface elements
RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0, rely=0.0, relheight=0.3, relwidth=1)

# Right bottom frame for the main content and user interaction
RB_frame = Frame(root)
RB_frame.place(relx=0, rely=0.3, relheight=0.7, relwidth=1)
# Search button
Button(RT_frame, text='Search', font=btn_font, bg=btn_hlb_bg, width=15, command=open_search_dialog).grid(row=10, column=10, padx=250, pady=100)

# Reload button
Button(RT_frame, text='Reload', font=btn_font, bg=btn_hlb_bg, width=15, command=display_records).grid(row=10, column=15, padx=450, pady=100)


# Right Bottom Frame
# Label for Book Inventory
Label(RB_frame, text='BOOK INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

# Treeview for displaying book inventory
tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=(
     'BK_NAME', 'BK_ID','AUTHOR_NAME','BK_STATUS', 'Issuer Card ID','Category','Asset_Code', 'Department', 'Subject', 'Edition', 'Date_Year','Call_No', 'Publisher', 'Place', 'ISBN', 'Price', 'Bill_Date', 'Vendor', 'Pages','Number_of_Copies'))

# Scrollbars for the Treeview
XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)

# Configure Treeview with Scrollbars
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

# Set up column headings for the Treeview
tree.heading('BK_NAME', text='Title', anchor=CENTER)
tree.heading('BK_ID', text='Access No', anchor=CENTER)
tree.heading('AUTHOR_NAME', text='Authors', anchor=CENTER)
tree.heading('BK_STATUS', text='Status', anchor=CENTER)
tree.heading('Issuer Card ID', text='Issuer Card ID', anchor=CENTER)
tree.heading('Category', text='Category', anchor=CENTER)
tree.heading('Asset_Code', text='Asset Code', anchor=CENTER)
tree.heading('Department', text='Department', anchor=CENTER)
tree.heading('Subject', text='Subject', anchor=CENTER)
tree.heading('Edition', text='Edition', anchor=CENTER)
tree.heading('Date_Year', text='Date Year', anchor=CENTER)
tree.heading('Call_No', text='Call No', anchor=CENTER)
tree.heading('Publisher', text='Publisher', anchor=CENTER)
tree.heading('Place', text='Place', anchor=CENTER)
tree.heading('ISBN', text='ISBN', anchor=CENTER)
tree.heading('Price', text='Price', anchor=CENTER)
tree.heading('Bill_Date', text='Bill Date', anchor=CENTER)
tree.heading('Vendor', text='Vendor', anchor=CENTER)
tree.heading('Pages', text='Pages', anchor=CENTER)
tree.heading('Number_of_Copies', text='Number of Copies', anchor=CENTER)

# Set column width and stretch properties
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=100, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=120, stretch=NO)
tree.column('#5', width=120, stretch=NO)
tree.column('#6', width=100, stretch=NO)
tree.column('#7', width=100, stretch=NO)
tree.column('#8', width=100, stretch=NO)
tree.column('#9', width=100, stretch=NO)
tree.column('#10', width=120, stretch=NO)
tree.column('#11', width=120, stretch=NO)
tree.column('#12', width=120, stretch=NO)
tree.column('#13', width=100, stretch=NO)
tree.column('#14', width=100, stretch=NO)
tree.column('#15', width=100, stretch=NO)
tree.column('#16', width=100, stretch=NO)
tree.column('#17', width=100, stretch=NO)
tree.column('#18', width=100, stretch=NO)
tree.column('#19', width=100, stretch=NO)
tree.place(y=30, x=0, relheight=0.9, relwidth=1)

# Populate and display records in the Treeview
display_records()
# Update the Tkinter window to reflect any changes
root.update()
# Start the Tkinter main event loop to handle user interactions
def student():
    root.mainloop()
# root.mainloop()
student()