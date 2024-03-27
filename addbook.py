from tkinter import *
from tkinter import messagebox
import sqlite3
con = sqlite3.connect('library.db')
cur=con.cursor()

class AddBook(Toplevel):
  def __init__(self):  # inherits from the Toplevel widget class - to create seperate window
    Toplevel.__init__(self)
    self.geometry("650x750+550+200") # sets the window dimensions
    self.title("Add Book") # set the window title text 
    self.resizable(False,False) # disable resizing the window
 
# Frames
    # Top frame
    self.topFrame=Frame(self,height=135, bg='white') # creates frame height and sets the colour
    self.topFrame.pack(fill=X) # places frame
    # Bottom frame
    self.bottomFrame=Frame(self,height=615, bg='#fcc324') # creates frame height and sets the colour
    self.bottomFrame.pack(fill=X) # places frame

    # Heading + Image
    self.top_image= PhotoImage(file='icons/add_book.png') # loads image 
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white') # creates a label and displays the image
    top_image_lbl.place(x=220,y=33)
    heading= Label(self.topFrame, text='Add Book', font = 'arial 22 bold', fg = 'black', bg = 'white') # creates label for text
    heading.place(x=285, y=60) # specify placing of the text and image

#Entries and Lables
  #Name
    self.lbl_name=Label(self.bottomFrame, text='Name:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the book name field 
    self.lbl_name.place(x=40,y=40) # postitions the label
    self.ent_name=Entry(self.bottomFrame,width=30,bd=4) # creates an entry box to enter the book name
    self.ent_name.insert(0, 'Please Enter Book Name') # placeholder text
    self.ent_name.place(x=150,y=45) # positions the entry below the label
   
  #Author
    self.lbl_author=Label(self.bottomFrame, text='Author:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the author name field 
    self.lbl_author.place(x=40,y=80) # creates an entry box to enter the author name
    self.ent_author=Entry(self.bottomFrame,width=30,bd=4)
    self.ent_author.insert(0, 'Please Enter Author Name') # placeholder text
    self.ent_author.place(x=150,y=85) # positions the entry below the label
    
  #Pages
    self.lbl_page=Label(self.bottomFrame, text='Page:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the No. pages field 
    self.lbl_page.place(x=40,y=120) # creates an entry box to enter the pages
    self.ent_page=Entry(self.bottomFrame,width=30,bd=4)
    self.ent_page.insert(0, 'Please No. Pages') # placeholder text
    self.ent_page.place(x=150,y=125)  # positions the entry below the label

  #Language
    self.lbl_language=Label(self.bottomFrame, text='Language:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the lanuages field 
    self.lbl_language.place(x=40,y=160) # creates an entry box to enter the language
    self.ent_language=Entry(self.bottomFrame,width=30,bd=4)
    self.ent_language.insert(0, 'Please Enter Language') # placeholder text
    self.ent_language.place(x=150,y=165) # positions the entry below the label

  #Button to add books
    button = Button(self.bottomFrame, text = ' Add Book', command=self.addBook) # creates the actual button
    button.place(x=300, y=250)  # places button in the desired postition

  def addBook(self):
    name = self.ent_name.get() # get the text entered into the name entry box 
    author = self.ent_author.get() # get the text entered into the author entry box
    page = self.ent_page.get() # get the text entered into the name pages box
    language = self.ent_language.get() # get the text entered into the language entry box

    if (name and author and page and language != ""): # check if entry fields are not empty
      try:
        query="INSERT INTO 'books' (book_name, book_author, book_page, book_language) VALUES(?,?,?,?)" # SQL query to insert new book 
        cur.execute(query, (name, author, page, language)) # execute query with input values
        con.commit() # save changes
        messagebox.showinfo("Success", "Successfully added to database",icon='info') # popup message for successful insert 

      except:
        messagebox.showerror("Error", "Cant add to database", icon='warning') # catch errors with insert
    else:  
      messagebox.showerror("Error", "Fields cant be empty", icon='warning')   # popup if fields are empty 

