from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()

class deleteBook(Toplevel):

  def __init__(self):
    Toplevel.__init__(self)
    self.geometry("650x750+550+200")
    self.title("Delete Book")
    self.resizable(False, False)

    #####frames#######

    # top frame
    self.topFrame=Frame(self,height=135, bg='white')
    self.topFrame.pack(fill=X)
    #bottom frame
    self.bottomFrame=Frame(self,height=615, bg='#fcc324')
    self.bottomFrame.pack(fill=X) 
    #heading, image
    self.top_image= PhotoImage(file='icons/book_remove.png')
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white')
    top_image_lbl.place(x=200,y=43)
    heading= Label(self.topFrame, text='Delete Book', font = 'arial 22 bold', fg = 'black', bg = 'white')
    heading.place(x=270, y=60)

      # Get list of books
    query = "SELECT * FROM books"
    books = cur.execute(query).fetchall()
    book_list = []
    for book in books:
        book_list.append(str(book[0])+ "-" + book[1])

      # Widgets
    self.lbl_name = Label(self.bottomFrame, text="Select Book:", font="arial 15 bold", fg = 'white', bg = '#fcc324')
    self.lbl_name.place(x=40, y=42)

    self.combo_name = ttk.Combobox(self.bottomFrame, values=book_list)
    self.combo_name.place(x=165, y=45)

    self.btn_delete = Button(self.bottomFrame, text="Delete", command=self.deleteBook)  
    self.btn_delete.place(x=270, y=120)    

  def deleteBook(self):
      book_id = self.combo_name.get().split('-')[0]
      
      # Confirm delete
      confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this book?")

      if confirm and (book_id != ""):
          try:
              cur.execute("DELETE FROM books WHERE book_id=?", (book_id,)) 
              con.commit()
              messagebox.showinfo("Success", "Book deleted from database")
          except:
              messagebox.showerror("Error", "Error deleting from database")
      else:
         messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning')
                    