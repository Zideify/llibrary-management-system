from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

con = sqlite3.connect('library.db')
cur=con.cursor()

class GiveBook(Toplevel):
  def __init__(self):
    Toplevel.__init__(self)
    self.geometry("650x750+550+300")
    self.title("Lend Book")
    self.resizable(False, False)
    query = "SELECT * FROM books WHERE book_status=0"
    books = cur.execute(query).fetchall()
    book_list = []
    for book in books:
      book_list.append(str(book[0])+ "-" + book[1])

    query = "SELECT * FROM members"
    members = cur.execute(query).fetchall()
    member_list = []
    for member in members:
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
    self.book_name = StringVar()
    self.lbl_name=Label(self.bottomFrame, text='Book:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') 
    self.lbl_name.place(x=40,y=40)
    self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.book_name)
    self.combo_name['values']=book_list
    self.combo_name.place(x=150, y=45)

  #Member Name
    self.member_name = StringVar()    
    self.lbl_phone=Label(self.bottomFrame, text='Member:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324')
    self.lbl_phone.place(x=40,y=80)
    self.combo_member = ttk.Combobox(self.bottomFrame, textvariable = self.member_name)
    self.combo_member['values']=member_list
    self.combo_member.place(x=150, y=85) 

    #button
    button = Button(self.bottomFrame, text = 'Lend Book', command = self.lendBook)
    button.place(x=270, y=120)
    
  def lendBook(self):
    member_name = self.member_name.get()
    book_name = self.book_name.get() 
    self.book_id=book_name.split('-')[0]  
   

    if (book_name and member_name) != "":
      try:
        query = "INSERT INTO 'borrows' (bbook_id, bmember_id) VALUES(?,?)"
        cur.execute(query, (book_name, member_name))
        con.commit()
        messagebox.showinfo("Success", "Successfully added to database!", icon = 'info')
        cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id))
        con.commit()
      except:
        messagebox.showerror("Error", "Cannot add to database", icon = 'warning')  

    else:
      messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning')   