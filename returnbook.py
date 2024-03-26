from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()

class ReturnBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Return Book")
        self.resizable(False, False)

        # Frames
        self.topFrame = Frame(self, height=135, bg='white')
        self.topFrame.pack(fill=X)
        self.bottomFrame = Frame(self, height=615, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # Heading and image
        self.top_image = PhotoImage(file='icons/book_return.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=200, y=42)
        heading = Label(self.topFrame, text='Return Book', font='arial 22 bold', fg='black', bg='white')
        heading.place(x=270, y=60)

        # Borrowed books list
        self.member_name = StringVar()    
        self.lbl_name = Label(self.bottomFrame, text="Select Book:", font="arial 15 bold", fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=42)
        self.combo_name = ttk.Combobox(self.bottomFrame)
        self.combo_name.place(x=165, y=45)

        # Get list of borrowed books
        query = "SELECT * FROM books WHERE book_status=1"
        borrowed_books = cur.execute(query).fetchall() # fetch all books that are borrowed
        book_list = []
        for book in borrowed_books:
            book_list.append(str(book[0]) + "-" + book[1])
        self.combo_name['values'] = book_list # fill the combo box

        self.btn_return = Button(self.bottomFrame, text="Return Book", command=self.returnBook)
        self.btn_return.place(x=270, y=120)       

    def returnBook(self):
        book_id = self.combo_name.get().split('-')[0] # removing the - and splitting there
        if book_id != "":
            try:
                cur.execute("UPDATE books SET book_status = 0 WHERE book_id = ?", (book_id,)) # update books to be available
                con.commit()

                cur.execute("DELETE FROM borrows WHERE bbook_id = ?", (book_id,)) # remove books from borrowed table
                con.commit()

                messagebox.showinfo("Success", "Book returned successfully!")
            except:
                messagebox.showerror("Error", "Error returning book")
        else:
            messagebox.showerror("Error", "Please select a book to return")         