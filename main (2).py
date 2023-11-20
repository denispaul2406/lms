# Importing all necessary modules
import sqlite3

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter.simpledialog import askstring

# Connecting to Database
connector = sqlite3.connect('library11.db')
cursor = connector.cursor()



# Functions
def issuer_card():
	Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

	if not Cid:
		mb.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
	else:
		return Cid

def display_records():
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())

    # Assuming your Library_View includes all the necessary columns for display
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)



def clear_fields():
    global bk_status, bk_name, bk_id, author_name, card_id, category, asset_code, department, subject
    global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies
    
    bk_status.set('Available')
    fields_to_clear = [
        bk_id, bk_name, author_name, card_id, category, asset_code, department, subject,
        edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies
    ]
    
    for field in fields_to_clear:
        field.set('')
    
    # Assuming bk_id_entry and tree are global variables and they are defined somewhere in your code.
    try:
        bk_id_entry.config(state='normal')
    except NameError:
        print("bk_id_entry is not defined or initialized")
    
    try:
        if tree.selection():
            tree.selection_remove(tree.selection()[0])
    except NameError:
        print("tree is not defined or initialized")



def clear_and_display():
	clear_fields()
	display_records()


def add_record():
    global connector
    global bk_name, bk_id, author_name, bk_status, card_id, category, asset_code, department, subject
    global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')

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

            clear_and_display()

            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            mb.showerror('Book ID already in use!',
                         'The Book ID you are trying to enter is already in the database, please alter that book\'s record or check any discrepancies on your side')

def view_record():
    global bk_name, bk_id, bk_status, author_name, card_id, category, asset_code, department, subject
    global tree, edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return

    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']

    bk_name.set(selection[0])
    bk_id.set(selection[1])
    author_name.set(selection[2])
    bk_status.set(selection[3])

    # Handle the rest of the fields
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


def update_record():
    def update():
        global bk_status, bk_name, bk_id, author_name, card_id
        global connector, tree, category, asset_code, department, subject
        global edition, date_year, call_No, publisher, place, isbn, price, bill_date, vendor, pages, number_of_copies

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

    view_record()

    bk_id_entry.config(state='disable')
    clear.config(state='disable')

    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=20, y=785)


def remove_record():
    global tree, connector

    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    try:
        # Assuming the structure of your database and columns, adjust as per your actual schema
        bk_id = selection[1]

        connector.execute('DELETE FROM BookInventory WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM Transactions WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM BookDetails WHERE BK_ID=?', (bk_id,))
        connector.execute('DELETE FROM Books WHERE BK_ID=?', (bk_id,))
        
        connector.commit()
        
        tree.delete(current_item)
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        clear_and_display()

    except sqlite3.Error as e:
        print("Error deleting record:", e)



def delete_inventory():
    global tree, connector

    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
        try:
            # Assuming the structure of your database and columns, adjust as per your actual schema
            connector.execute('DELETE FROM BookInventory')
            connector.execute('DELETE FROM Transactions')
            connector.execute('DELETE FROM BookDetails')
            connector.execute('DELETE FROM Books')

            connector.commit()
            
            tree.delete(*tree.get_children())
            mb.showinfo('Inventory Deleted', 'The entire inventory was successfully deleted.')

        except sqlite3.Error as e:
            print("Error deleting inventory:", e)
            # Handle the error appropriately
    else:
        return
    


def open_search_dialog():
    search_term = askstring('Search', 'Enter your search query:')
    if search_term:
        search_records(search_term)

def search_records(search_term):
    global connector, tree

    tree.delete(*tree.get_children())

    if search_term:
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
        query = 'SELECT * FROM Library'

    curr = connector.execute(query)
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)




def change_availability():
    global card_id, tree, connector

    if not tree.selection():
        mb.showerror('Error!', 'Please select a book from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    BK_id = values['values'][1]
    BK_status = values["values"][3]

    try:
        if BK_status == 'Issued':
            surety = mb.askyesno('Is return confirmed?', 'Has the book been returned to you?')
            if surety:
                connector.execute('UPDATE BookDetails SET BK_STATUS=? WHERE BK_ID=?', ('Available', BK_id))
                connector.execute('UPDATE Transactions SET CARD_ID=? WHERE BK_ID=?', ('N/A', BK_id))
                connector.execute('UPDATE BookInventory SET Number_of_Copies=Number_of_Copies+1 WHERE BK_ID=?', (BK_id,))
                connector.commit()
            else:
                mb.showinfo('Cannot be returned', 'The book status cannot be set to Available unless it has been returned')
        else:
            # Modify the 'issuer_card()' function call according to your implementation
            new_card_id = issuer_card()  # Assuming this function retrieves a new card ID
            connector.execute('UPDATE BookDetails SET BK_STATUS=? WHERE BK_ID=?', ('Issued', BK_id))
            connector.execute('UPDATE Transactions SET CARD_ID=? WHERE BK_ID=?', (new_card_id, BK_id))
            connector.execute('UPDATE BookInventory SET Number_of_Copies=Number_of_Copies-1 WHERE BK_ID=?', (BK_id,))
            connector.commit()

        clear_and_display()

    except sqlite3.Error as e:
        print("Error updating availability:", e)

def exit_fullscreen():
    root.attributes('-fullscreen', False)
    root.destroy()


# Variables
lf_bg = 'LightSkyBlue'  # Left Frame Background Color
rtf_bg = 'DeepSkyBlue'  # Right Top Frame Background Color
rbf_bg = 'DodgerBlue'  # Right Bottom Frame Background Color
btn_hlb_bg = 'SteelBlue'  # Background color for Head Labels and Buttons

lbl_font = ('Georgia', 13)  # Font for all labels
entry_font = ('Times New Roman', 12)  # Font for all Entry widgets
btn_font = ('Gill Sans MT', 13)

root = Tk()
root.title('Library Management System')
# root.geometry('1440x1000')
root.resizable(0, 0)
close_button = Button(root, text='Close', command=exit_fullscreen)
close_button.pack()

# Making the window full screen
root.attributes('-fullscreen', True)

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

# StringVars
bk_status = StringVar()
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
card_id = StringVar()
category = StringVar()
asset_code = StringVar()
department = StringVar()
subject = StringVar() 
edition = StringVar()
date_year = StringVar()
call_No  = StringVar()
publisher = StringVar()
place = StringVar() 
isbn = StringVar() 
price = StringVar()
bill_date = StringVar()
vendor = StringVar()
pages = StringVar() 
number_of_copies = StringVar()

# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

# Labels and Entry widgets for all fields
Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).place(x=20, y=25)
Entry(left_frame, width=25, font=entry_font, textvariable=bk_name).place(x=145, y=25)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=20, y=65)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, textvariable=bk_id)
bk_id_entry.place(x=145, y=65)

Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).place(x=20, y=105)
Entry(left_frame, width=25, font=entry_font, textvariable=author_name).place(x=145, y=105)

Label(left_frame, text='Status', bg=lf_bg, font=lbl_font).place(x=20, y=145)
dd = OptionMenu(left_frame, bk_status, *['Available', 'Issued'])
dd.configure(font=entry_font, width=12)
dd.place(x=145, y=145)

Label(left_frame, text='Category', bg=lf_bg, font=lbl_font).place(x=20, y=185)
Entry(left_frame, width=25, font=entry_font, textvariable=category).place(x=145, y=185)

Label(left_frame, text='Asset Code', bg=lf_bg, font=lbl_font).place(x=20, y=225)
Entry(left_frame, width=25, font=entry_font, textvariable=asset_code).place(x=145, y=225)

Label(left_frame, text='Department', bg=lf_bg, font=lbl_font).place(x=20, y=265)
Entry(left_frame, width=25, font=entry_font, textvariable=department).place(x=145, y=265)

Label(left_frame, text='Subject', bg=lf_bg, font=lbl_font).place(x=20, y=305)
Entry(left_frame, width=25, font=entry_font, textvariable=subject).place(x=145, y=305)

Label(left_frame, text='Edition', bg=lf_bg, font=lbl_font).place(x=20, y=345)
Entry(left_frame, width=25, font=entry_font, textvariable=edition).place(x=145, y=345)

Label(left_frame, text='Date Year', bg=lf_bg, font=lbl_font).place(x=20, y=385)
Entry(left_frame, width=25, font=entry_font, textvariable=date_year).place(x=145, y=385)

Label(left_frame, text='Call No', bg=lf_bg, font=lbl_font).place(x=20, y=425)
Entry(left_frame, width=25, font=entry_font, textvariable=call_No).place(x=145, y=425)

Label(left_frame, text='Publisher', bg=lf_bg, font=lbl_font).place(x=20, y=465)
Entry(left_frame, width=25, font=entry_font, textvariable=publisher).place(x=145, y=465)

Label(left_frame, text='Place', bg=lf_bg, font=lbl_font).place(x=20, y=505)
Entry(left_frame, width=25, font=entry_font, textvariable=place).place(x=145, y=505)

Label(left_frame, text='ISBN', bg=lf_bg, font=lbl_font).place(x=20, y=545)
Entry(left_frame, width=25, font=entry_font, textvariable=isbn).place(x=145, y=545)

Label(left_frame, text='Price', bg=lf_bg, font=lbl_font).place(x=20, y=585)
Entry(left_frame, width=25, font=entry_font, textvariable=price).place(x=145, y=585)

Label(left_frame, text='Bill Date', bg=lf_bg, font=lbl_font).place(x=20, y=625)
Entry(left_frame, width=25, font=entry_font, textvariable=bill_date).place(x=145, y=625)

Label(left_frame, text='Vendor', bg=lf_bg, font=lbl_font).place(x=20, y=665)
Entry(left_frame, width=25, font=entry_font, textvariable=vendor).place(x=145, y=665)

Label(left_frame, text='Pages', bg=lf_bg, font=lbl_font).place(x=20, y=705)
Entry(left_frame, width=25, font=entry_font, textvariable=pages).place(x=145, y=705)

Label(left_frame, text='Copies', bg=lf_bg, font=lbl_font).place(x=20, y=745)
Entry(left_frame, width=25, font=entry_font, textvariable=number_of_copies).place(x=145, y=745)

submit = Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=add_record)
submit.place(x=20, y=785)

clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields)
clear.place(x=230, y=785)

# Right Top Frame
Button(RT_frame, text='Delete book record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).place(x=20, y=110)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).place(x=220, y=110)
Button(RT_frame, text='Update book details', font=btn_font, bg=btn_hlb_bg, width=17,
       command=update_record).place(x=420, y=110)
Button(RT_frame, text='Change Book Availability', font=btn_font, bg=btn_hlb_bg, width=19,
       command=change_availability).place(x=620, y=110)
Button(RT_frame, text='Search', font=btn_font, bg=btn_hlb_bg, width=10, command=open_search_dialog).place(x=840, y=110)
Button(RT_frame, text='Reload', font=btn_font, bg=btn_hlb_bg, width=10, command=display_records).place(x=980, y=110)


Label(RT_frame, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

# Right Bottom Frame
Label(RB_frame, text='BOOK INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=(
     'BK_NAME', 'BK_ID','AUTHOR_NAME','BK_STATUS', 'Issuer Card ID','Category','Asset_Code', 'Department', 'Subject', 'Edition', 'Date_Year','Call_No', 'Publisher', 'Place', 'ISBN', 'Price', 'Bill_Date', 'Vendor', 'Pages','Number_of_Copies'))

XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)

tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)



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
tree.heading('Number_of_Copies', text='Number_of_Copies', anchor=CENTER)


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

clear_and_display()

# Finalizing the window
root.update()
root.mainloop()
