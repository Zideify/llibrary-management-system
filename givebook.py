from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

con = sqlite3.connect('library.db')
cur=con.cursor()

class GiveBook(Toplevel):
  def __init__(self):
    Toplevel.__init__(self)
    self.geometry("650x750+550+300") # setting dimensions
    self.title("Lend Book") # setting title
    self.resizable(False, False)
    query = "SELECT * FROM books WHERE book_status=0" # getting all available books
    books = cur.execute(query).fetchall()
    book_list = []
    for book in books: # getting availble books ID and name
      book_list.append(str(book[0])+ "-" + book[1])

    query = "SELECT * FROM members" # getting all members
    members = cur.execute(query).fetchall()
    member_list = []
    for member in members: # getting member ID and name 
      member_list.append(str(member[0])+ "-" + member[1])          

#Frames
    # Top frame
    self.topFrame=Frame(self,height=135, bg='white') # creates frame height and sets the colour
    self.topFrame.pack(fill=X) # places frame
    # Bottom frame
    self.bottomFrame=Frame(self,height=615, bg='#fcc324') # creates frame height and sets the colour
    self.bottomFrame.pack(fill=X) # places frame

    #heading, image
    self.top_image= PhotoImage(file='icons/givebook1.png') # loads image 
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white') # creates a label and displays the image
    top_image_lbl.place(x=200,y=43)
    heading= Label(self.topFrame, text='Lend Book:', font = 'arial 22 bold', fg = 'black', bg = 'white') # creates label for text
    heading.place(x=270, y=60) # specify placing of the text and image

#Entries and Lables
    
  #Book Name
    self.book_name = StringVar()  # variable to store the selected book name
    self.lbl_name=Label(self.bottomFrame, text='Book:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label and displays the image
    self.lbl_name.place(x=40,y=40)
    self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.book_name)
    self.combo_name['values']=book_list # assigning book names to the combobox
    self.combo_name.place(x=150, y=45)

  #Member Name
    self.member_name = StringVar() # variable to store the selected member name
  
    self.lbl_phone=Label(self.bottomFrame, text='Member:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label and displays the image
    self.lbl_phone.place(x=40,y=80)
    self.combo_member = ttk.Combobox(self.bottomFrame, textvariable = self.member_name)
    self.combo_member['values']=member_list # assigning book members to the combobox
    self.combo_member.place(x=150, y=85) 

    #button
    button = Button(self.bottomFrame, text = 'Lend Book', command = self.lendBook) # creates button
    button.place(x=270, y=120)
    
  def lendBook(self):
    member_name = self.member_name.get() # getting selected member name
    book_name = self.book_name.get() # getting selected member name
    self.book_id=book_name.split('-')[0]  
   

    if (book_name and member_name) != "":
      try:
        query = "INSERT INTO 'borrows' (bbook_id, bmember_id) VALUES(?,?)" # inserting book and member into borrows table
        cur.execute(query, (book_name, member_name))
        con.commit()
        messagebox.showinfo("Success", "Successfully added to database!", icon = 'info') # success message
        cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id)) # make book unavailble
        con.commit()
      except:
        messagebox.showerror("Error", "Cannot add to database", icon = 'warning')  

    else:
      messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning')  # error message if either field is empty
