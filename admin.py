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




# Function to get Issuer's Card ID from user input
def issuer_card():
    # Using a simple dialog to ask for Issuer's Card ID
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

    # Checking if Issuer's Card ID is provided
    if not Cid:
        # Displaying an error message if Issuer ID is not provided
        mb.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
    else:
        # Returning the Issuer's Card ID if provided
        return Cid

# Function to display records in the Tkinter treeview
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

# Function to clear input fields and reset values
def clear_fields():
    global bk_status, bk_name, bk_id, author_name, card_id, category, asset_code, department, subject
    global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies
    
    # Resetting book status to 'Available'
    bk_status.set('Available')
    
    # List of fields to clear
    fields_to_clear = [
        bk_id, bk_name, author_name, card_id, category, asset_code, department, subject,
        edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies
    ]
    
    # Clearing values in each field
    for field in fields_to_clear:
        field.set('')
    
    # Trying to set the 'bk_id_entry' state to 'normal' (assuming it's an entry widget)
    try:
        bk_id_entry.config(state='normal')
    except NameError:
        print("bk_id_entry is not defined or initialized")
    
    # Trying to remove selection from the treeview widget
    try:
        if tree.selection():
            tree.selection_remove(tree.selection()[0])
    except NameError:
        print("tree is not defined or initialized")



# Function to clear fields and display updated records
def clear_and_display():
    # Clearing input fields
    clear_fields()
    
    # Displaying updated records in the Tkinter treeview
    display_records()


# Function to add a new record to the database
def add_record():
    global connector
    global bk_name, bk_id, author_name, bk_status, card_id, category, asset_code, department, subject
    global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

    # Checking if the book status is 'Issued' to prompt for the issuer's card ID
    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')

    # Asking for confirmation from the user
    surety = mb.askyesno('Are you sure?',
                         'Are you sure this is the data you want to enter?\nPlease note that Book ID cannot be changed in the future')

    if surety:
        try:
            # Inserting data into respective tables
            cursor.execute(
                'INSERT INTO Books (BK_ID, BK_NAME, AUTHOR_NAME, Edition, Date_Year, Publisher, Place, ISBN, Price, Pages, Category, Department, Subject) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (bk_id.get(), bk_name.get(), author_name.get(), edition.get(), date_year.get(), publisher.get(), place.get(), isbn.get(), price.get(), pages.get(), category.get(), department.get(), subject.get()))
            cursor.execute(
                'INSERT INTO BookInventory (BK_ID, Number_of_Copies) VALUES (?, ?)',
                (bk_id.get(), number_of_copies.get()))
            cursor.execute(
                'INSERT INTO BookDetails (Asset_Code, Call_No, BK_ID, BK_STATUS) VALUES (?, ?, ?, ?)',
                (asset_code.get(), call_No.get(), bk_id.get(), bk_status.get()))
            cursor.execute(
                'INSERT INTO Transactions (BK_ID, CARD_ID, Bill_Date, Vendor) VALUES (?, ?, ?, ?)',
                (bk_id.get(), card_id.get(), bill_date.get(), vendor.get()))
            
            connector.commit()

            # Clearing fields and updating display
            clear_and_display()

            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            # Handling the case where the Book ID is already in use
            mb.showerror('Book ID already in use!',
                         'The Book ID you are trying to enter is already in the database, please alter that book\'s record or check any discrepancies on your side')

# Function to populate input fields with selected record for viewing
def view_record():
    global bk_name, bk_id, bk_status, author_name, card_id, category, asset_code, department, subject
    global tree, edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

    # Checking if a row in the treeview is selected
    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return

    # Getting the selected item and its values
    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']

    # Setting values to corresponding variables
    bk_name.set(selection[0])
    bk_id.set(selection[1])
    author_name.set(selection[2])
    bk_status.set(selection[3])

    # Handling the rest of the fields with try-except blocks to manage potential IndexErrors
    try:
        card_id.set(selection[4])
    except IndexError:
        card_id.set('')

    try:
        category.set(selection[5])
    except IndexError:
        category.set('')

    try:
        asset_code.set(selection[6])
    except IndexError:
        asset_code.set('')

    try:
        department.set(selection[7])
    except IndexError:
        department.set('')

    try:
        subject.set(selection[8])
    except IndexError:
        subject.set('')

    try:
        edition.set(selection[9])
    except IndexError:
        edition.set('')

    try:
        date_year.set(selection[10])
    except IndexError:
        date_year.set('')

    try:
        call_No.set(selection[11])
    except IndexError:
        call_No.set('')

    try:
        publisher.set(selection[12])
    except IndexError:
        publisher.set('')

    try:
        place.set(selection[13])
    except IndexError:
        place.set('')

    try:
        isbn.set(selection[14])
    except IndexError:
        isbn.set('')

    try:
        price.set(selection[15])
    except IndexError:
        price.set('')

    try:
        bill_date.set(selection[16])
    except IndexError:
        bill_date.set('')

    try:
        vendor.set(selection[17])
    except IndexError:
        vendor.set('')

    try:
        pages.set(selection[18])
    except IndexError:
        pages.set('')

    try:
        number_of_copies.set(selection[19])
    except IndexError:
        number_of_copies.set('')


# Function to update a selected record in the database
def update_record():
    def update():
        global bk_status, bk_name, bk_id, author_name, card_id
        global connector, tree, category, asset_code, department, subject
        global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

        # Checking book status to prompt for issuer's card ID if 'Issued'
        if bk_status.get() == 'Issued':
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')

        try:
            # Update data in respective parent tables (Books, BookDetails, Transactions)
            connector.execute('''
                UPDATE Books 
                SET BK_NAME=?, AUTHOR_NAME=?, Edition=?, Date_Year=?, Publisher=?, Place=?, ISBN=?, Price=?, Pages=?, Category=?, Department=?, Subject=? 
                WHERE BK_ID=?''',
                (bk_name.get(), author_name.get(), edition.get(), date_year.get(), publisher.get(), place.get(), isbn.get(), price.get(), pages.get(), category.get(), department.get(), subject.get(), bk_id.get()))

            connector.execute('UPDATE BookDetails SET BK_STATUS=?, Asset_Code=?, Call_No=? WHERE BK_ID=?',
                              (bk_status.get(), asset_code.get(), call_No.get(), bk_id.get()))

            connector.execute('UPDATE Transactions SET CARD_ID=?, Bill_Date=?, Vendor=? WHERE BK_ID=?',
                              (card_id.get(), bill_date.get(), vendor.get(), bk_id.get()))

            connector.execute('UPDATE BookInventory SET Number_of_Copies=? WHERE BK_ID=?',
                              (number_of_copies.get(), bk_id.get()))

            connector.commit()
            clear_and_display()
            edit.destroy()
            bk_id_entry.config(state='normal')
            clear.config(state='normal')

        except sqlite3.Error as e:
            print("Error updating record:", e)
            # Handle the error appropriately

    # Call the function to populate input fields with the selected record
    view_record()

    # Disable bk_id_entry and clear button
    bk_id_entry.config(state='disable')
    clear.config(state='disable')

    # Create an 'Update' button that calls the update function
    edit = Button(left_frame, text='Update', font=btn_font, bg=btn_hlb_bg, width=8, command=update)
    edit.grid(row=19, column=0, padx=(10, 5), pady=20)  # Adjust padx for left side spacing

# Function to remove a selected record from the database
def remove_record():
    global tree, connector

    # Checking if a row in the treeview is selected
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    # Getting the selected item and its values
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    try:
        # Assuming the structure of your database and columns, adjust as per your actual schema
        bk_id = selection[1]

        # Deleting records from respective tables
        connector.execute('DELETE FROM BookInventory WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM Transactions WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM BookDetails WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM Books WHERE BK_ID=?', (bk_id,))
        
        connector.commit()
        
        # Deleting the selected item from the treeview
        tree.delete(current_item)
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        # Updating and displaying the remaining records
        clear_and_display()

    except sqlite3.Error as e:
        print("Error deleting record:", e)



# Function to delete the entire inventory from the database
def delete_inventory():
    global tree, connector

    # Asking for confirmation from the user
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
        try:
            # Assuming the structure of your database and columns, adjust as per your actual schema
            connector.execute('DELETE FROM BookInventory')
            connector.execute('DELETE FROM Transactions')
            connector.execute('DELETE FROM BookDetails')
            connector.execute('DELETE FROM Books')

            connector.commit()
            
            # Clearing the treeview and displaying a message
            tree.delete(*tree.get_children())
            mb.showinfo('Inventory Deleted', 'The entire inventory was successfully deleted.')

        except sqlite3.Error as e:
            print("Error deleting inventory:", e)
            # Handle the error appropriately
    else:
        return
    


# Function to open a search dialog and initiate search
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




# Function to change the availability status of a book in the database
def change_availability():
    global card_id, tree, connector

    # Checking if a row in the treeview is selected
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book from the database')
        return

    # Getting the selected item and its values
    current_item = tree.focus()
    values = tree.item(current_item)
    BK_id = values['values'][1]
    BK_status = values["values"][3]

    try:
        # Checking the current status of the book
        if BK_status == 'Issued':
            # Asking for confirmation of book return
            surety = mb.askyesno('Is return confirmed?', 'Has the book been returned to you?')
            
            if surety:
                # Setting the book status to 'Available' and updating card ID to 'N/A'
                connector.execute('UPDATE BookDetails SET BK_STATUS=? WHERE BK_ID=?', ('Available', BK_id))
                connector.execute('UPDATE Transactions SET CARD_ID=? WHERE BK_ID=?', ('N/A', BK_id))
                connector.commit()
            else:
                mb.showinfo('Cannot be returned', 'The book status cannot be set to Available unless it has been returned')
        else:
            # Modify the 'issuer_card()' function call according to your implementation
            new_card_id = issuer_card()  # Assuming this function retrieves a new card ID
            
            # Setting the book status to 'Issued' and updating card ID
            connector.execute('UPDATE BookDetails SET BK_STATUS=? WHERE BK_ID=?', ('Issued', BK_id))
            connector.execute('UPDATE Transactions SET CARD_ID=? WHERE BK_ID=?', (new_card_id, BK_id))
            connector.commit()

        # Updating and displaying the records
        clear_and_display()

    except sqlite3.Error as e:
        print("Error updating availability:", e)



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

# Initializing StringVar variables for various data fields
bk_status = StringVar()  # Book status (Available/Issued)
bk_name = StringVar()  # Book name
bk_id = StringVar()  # Book ID
author_name = StringVar()  # Author name
card_id = StringVar()  # Card ID (for book issuance)
category = StringVar()  # Book category
asset_code = StringVar()  # Asset code
department = StringVar()  # Department
subject = StringVar()  # Book subject
edition = StringVar()  # Book edition
date_year = StringVar()  # Year of publication
call_No  = StringVar()  # Call number
publisher = StringVar()  # Publisher
place = StringVar()  # Place of publication
isbn = StringVar()  # ISBN (International Standard Book Number)
price = StringVar()  # Book price
bill_date = StringVar()  # Billing date
vendor = StringVar()  # Vendor
pages = StringVar()  # Number of pages
number_of_copies = StringVar()  # Number of book copies

# Left frame for user interface elements
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

# Right top frame for additional user interface elements
RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

# Right bottom frame for the main content and user interaction
RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

# Labels and Entry widgets for book-related information in the left frame

# Book Name
Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).grid(row=0, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=bk_name).grid(row=0, column=1, padx=10, pady=5)

# Book ID
Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).grid(row=1, column=0, sticky='w', padx=10, pady=5)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, textvariable=bk_id)
bk_id_entry.grid(row=1, column=1, padx=10, pady=5)

# Author Name
Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).grid(row=2, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=author_name).grid(row=2, column=1, padx=10, pady=5)

# Status (Dropdown)
Label(left_frame, text='Status', bg=lf_bg, font=lbl_font).grid(row=3, column=0, sticky='w', padx=10, pady=5)
status_options = ['Available', 'Issued']
bk_status.set(status_options[0])  # Set default value
status_dropdown = OptionMenu(left_frame, bk_status, *status_options)
status_dropdown.configure(font=entry_font, width=12)
status_dropdown.grid(row=3, column=1, padx=10, pady=5)

# Category
Label(left_frame, text='Category', bg=lf_bg, font=lbl_font).grid(row=4, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=category).grid(row=4, column=1, padx=10, pady=5)

# Asset Code
Label(left_frame, text='Asset Code', bg=lf_bg, font=lbl_font).grid(row=5, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=asset_code).grid(row=5, column=1, padx=10, pady=5)

# Department
Label(left_frame, text='Department', bg=lf_bg, font=lbl_font).grid(row=6, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=department).grid(row=6, column=1, padx=10, pady=5)

# Subject
Label(left_frame, text='Subject', bg=lf_bg, font=lbl_font).grid(row=7, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=subject).grid(row=7, column=1, padx=10, pady=5)

# Edition
Label(left_frame, text='Edition', bg=lf_bg, font=lbl_font).grid(row=8, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=edition).grid(row=8, column=1, padx=10, pady=5)

# Date Year
Label(left_frame, text='Date Year', bg=lf_bg, font=lbl_font).grid(row=9, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=date_year).grid(row=9, column=1, padx=10, pady=5)

# Call No
Label(left_frame, text='Call No', bg=lf_bg, font=lbl_font).grid(row=10, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=call_No).grid(row=10, column=1, padx=10, pady=5)

# Publisher
Label(left_frame, text='Publisher', bg=lf_bg, font=lbl_font).grid(row=11, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=publisher).grid(row=11, column=1, padx=10, pady=5)

# Place
Label(left_frame, text='Place', bg=lf_bg, font=lbl_font).grid(row=12, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=place).grid(row=12, column=1, padx=10, pady=5)

# ISBN
Label(left_frame, text='ISBN', bg=lf_bg, font=lbl_font).grid(row=13, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=isbn).grid(row=13, column=1, padx=10, pady=5)

# Price
Label(left_frame, text='Price', bg=lf_bg, font=lbl_font).grid(row=14, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=price).grid(row=14, column=1, padx=10, pady=5)

# Bill Date
Label(left_frame, text='Bill Date', bg=lf_bg, font=lbl_font).grid(row=15, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=bill_date).grid(row=15, column=1, padx=10, pady=5)

# Vendor
Label(left_frame, text='Vendor', bg=lf_bg, font=lbl_font).grid(row=16, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=vendor).grid(row=16, column=1, padx=10, pady=5)

# Pages
Label(left_frame, text='Pages', bg=lf_bg, font=lbl_font).grid(row=17, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=pages).grid(row=17, column=1, padx=10, pady=5)

# Copies
Label(left_frame, text='Copies', bg=lf_bg, font=lbl_font).grid(row=18, column=0, sticky='w', padx=10, pady=5)
Entry(left_frame, width=25, font=entry_font, textvariable=number_of_copies).grid(row=18, column=1, padx=10, pady=5)


# edit = Button(left_frame, text='Update', font=btn_font, bg=btn_hlb_bg, width=8, command=update_record)
# edit.grid(row=19, column=0, padx=(10, 5), pady=20)

# Submit button
submit = Button(left_frame, text='Submit', font=btn_font, bg=btn_hlb_bg, width=8, command=add_record)
submit.grid(row=19, column=1, padx=5, pady=15)

# Clear button
clear = Button(left_frame, text='Clear', font=btn_font, bg=btn_hlb_bg, width=8, command=clear_fields)
clear.grid(row=19, column=2, padx=(5, 10), pady=15)



# Labels and Entry widgets for all fields


# Right Top Frame
# Delete book record button
Button(RT_frame, text='Delete book record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).grid(row=10, column=0, padx=10, pady=100)

# Delete full inventory button
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).grid(row=10, column=1, padx=10, pady=100)

# Update book detail button
Button(RT_frame, text='Update book detail', font=btn_font, bg=btn_hlb_bg, width=17, command=update_record).grid(row=10, column=2, padx=10, pady=100)

# Change Book Availability button
Button(RT_frame, text='Change Book Availability', font=btn_font, bg=btn_hlb_bg, width=19, command=change_availability).grid(row=10, column=3, padx=10, pady=100)

# Search button
Button(RT_frame, text='Search', font=btn_font, bg=btn_hlb_bg, width=15, command=open_search_dialog).grid(row=10, column=4, padx=10, pady=100)

# Reload button
Button(RT_frame, text='Reload', font=btn_font, bg=btn_hlb_bg, width=15, command=display_records).grid(row=10, column=5, padx=10, pady=100)


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
clear_and_display()

# Update the Tkinter window to reflect any changes
root.update()
def admin():
# Start the Tkinter main event loop to handle user interactions
    root.mainloop()

admin()