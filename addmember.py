from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('library.db')
cur=con.cursor()

class AddMember(Toplevel):
  def __init__(self):  # inherits from the Toplevel widget class - to make seperate window
    Toplevel.__init__(self)
    self.geometry("650x750+550+200") # sets the window dimensions
    self.title("Add Member") # set the window title text 
    self.resizable(False,False) # disable resizing the window
 
# Frames
    # Top frame
    self.topFrame=Frame(self,height=135, bg='white') # creates frame height and sets the colour
    self.topFrame.pack(fill=X) # places frame
    # Bottom frame
    self.bottomFrame=Frame(self,height=615, bg='#fcc324') # creates frame height and sets the colour
    self.bottomFrame.pack(fill=X) # places frame

    # Heading + Image
    self.top_image= PhotoImage(file='icons/adduser.png') # loads image 
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white') # creates a label and displays the image
    top_image_lbl.place(x=210,y=33)
    heading= Label(self.topFrame, text='Add Member', font = 'arial 22 bold', fg = 'black', bg = 'white') # creates label for text
    heading.place(x=285, y=60) # specify placing of the text and image

#Entries and Lables
  #Name
    self.lbl_name=Label(self.bottomFrame, text='Name:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the member name field 
    self.lbl_name.place(x=40,y=40) # postitions the label
    self.ent_name=Entry(self.bottomFrame,width=30,bd=4) # creates an entry box to enter the member name
    self.ent_name.insert(0, 'Please Enter Member Name') # placeholder text
    self.ent_name.place(x=150,y=45) # positions the entry below the label
   
  #Phone Number
    self.lbl_phone=Label(self.bottomFrame, text='Phone No:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the Phone Number field 
    self.lbl_phone.place(x=40,y=80) # creates an entry box to enter the Phone Number
    self.ent_phone=Entry(self.bottomFrame,width=30,bd=4)
    self.ent_phone.insert(0, 'Please Enter Member Phone No.') # placeholder text
    self.ent_phone.place(x=150,y=85) # positions the entry below the label
    
  #Email
    self.lbl_email=Label(self.bottomFrame, text='Email:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creates a label for the member Email field 
    self.lbl_email.place(x=40,y=120) # creates an entry box to enter the member Email
    self.ent_email=Entry(self.bottomFrame,width=30,bd=4)
    self.ent_email.insert(0, 'Please Member Email') # placeholder text
    self.ent_email.place(x=150,y=125)  # positions the entry below the label

  #Button to member
    button = Button(self.bottomFrame, text = ' Add Member', command=self.addMember) # creates the actual button                        # add after 
    button.place(x=300, y=165)  # places button in the desired postition

  def addMember(self):
    name = self.ent_name.get() # get the text entered into the name entry box 
    phone = self.ent_phone.get() # get the text entered into the author entry box
    email = self.ent_email.get() # get the text entered into the name pages box

    if (name and phone and email != ""): # check if entry fields are not empty
      try:
        query="INSERT INTO 'members' (member_name, member_phone, member_email) VALUES(?,?,?)" # SQL query to insert new book 
        cur.execute(query, (name, phone, email)) # execute query with input values
        con.commit() # save changes
        messagebox.showinfo("Success", "Successfully added to database",icon='info') # popup message for successful insert 

      except:
        messagebox.showerror("Error", "Cant add to database", icon='warning') # catch errors with insert
    else:  
      messagebox.showerror("Error", "Fields cant be empty", icon='warning')   # popup if fields are empty 

