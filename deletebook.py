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
    self.topFrame=Frame(self,height=135, bg='white') # creates frame height and sets the colour
    self.topFrame.pack(fill=X) #places frame
    #bottom frame
    self.bottomFrame=Frame(self,height=615, bg='#fcc324') # creates frame height and sets the colour
    self.bottomFrame.pack(fill=X)  #places frame
    #heading, image
    self.top_image= PhotoImage(file='icons/book_remove.png') # loads image 
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white') # creates a label and displays the image
    top_image_lbl.place(x=200,y=43)
    heading= Label(self.topFrame, text='Delete Book', font = 'arial 22 bold', fg = 'black', bg = 'white') # creates label for text
    heading.place(x=270, y=60) # specify placing of the text and image

      # Get list of books
    query = "SELECT * FROM books" # getting all books from database  
    books = cur.execute(query).fetchall() # storing all books in list
    book_list = []
    for book in books: # iterates through books
        book_list.append(str(book[0])+ "-" + book[1]) # getting book ID and book name

      # Widgets
    self.lbl_name = Label(self.bottomFrame, text="Select Book:", font="arial 15 bold", fg = 'white', bg = '#fcc324') # creates label
    self.lbl_name.place(x=40, y=42) # places label

    self.combo_name = ttk.Combobox(self.bottomFrame, values=book_list) # creates combobox
    self.combo_name.place(x=165, y=45) # places combobox

    self.btn_delete = Button(self.bottomFrame, text="Delete", command=self.deleteBook)  # creates button
    self.btn_delete.place(x=270, y=120)    # places button

  def deleteBook(self):
      book_id = self.combo_name.get().split('-')[0] # getting book ID
      
      # Confirm delete
      confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this book?")

      if confirm and (book_id != ""): # if confirmation is true and book ID is not empty
          try:
              cur.execute("DELETE FROM books WHERE book_id=?", (book_id,)) # deleting books from database
              con.commit()
              messagebox.showinfo("Success", "Book deleted from database") # success popup
          except:
              messagebox.showerror("Error", "Error deleting from database")
      else:
         messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning') # if empty or confirmation false
                    
