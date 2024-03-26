from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()

class deleteMember(Toplevel):

  def __init__(self):
    Toplevel.__init__(self)
    self.geometry("650x750+550+200")
    self.title("Delete Member")
    self.resizable(False, False)

    #####frames#######

    # top frame
    self.topFrame=Frame(self,height=150, bg='white')
    self.topFrame.pack(fill=X)
    #bottom frame
    self.bottomFrame=Frame(self,height=600, bg='#fcc324')
    self.bottomFrame.pack(fill=X) 
    #heading, image
    self.top_image= PhotoImage(file='icons/delete_member.png')
    top_image_lbl=Label(self.topFrame,image=self.top_image, bg = 'white')
    top_image_lbl.place(x=200,y=43)
    heading= Label(self.topFrame, text='Delete Member', font = 'arial 22 bold', fg = 'black', bg = 'white')
    heading.place(x=270, y=60)
      
      # Get list of members
    query = "SELECT * FROM members"
    members = cur.execute(query).fetchall()
    member_list = []
    for member in members:
        member_list.append(str(member[0])+ "-" + member[1])

      # Widgets
    self.lbl_name = Label(self.bottomFrame, text="Select Member:", font="arial 15 bold", fg = 'white', bg = '#fcc324')
    self.lbl_name.place(x=40, y=42)

    self.combo_name = ttk.Combobox(self.bottomFrame, values=member_list)
    self.combo_name.place(x=200, y=45)

    self.btn_delete = Button(self.bottomFrame, text="Delete", command=self.deleteMember)  
    self.btn_delete.place(x=270, y=120)


  def deleteMember(self):
      member_id = self.combo_name.get().split('-')[0]
      
      # Confirm delete
      confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this member?")

      if confirm and (member_id != ""):
          try:
              cur.execute("DELETE FROM members WHERE member_id=?", (member_id,)) 
              con.commit()
              messagebox.showinfo("Success", "Member deleted from database")
          except:
              messagebox.showerror("Error", "Error deleting from database")
      else:
         messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning')
                
      