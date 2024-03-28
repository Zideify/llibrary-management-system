from tkinter import *
from tkinter import ttk
import sqlite3
import addbook, addmember, givebook, deletebook, returnbook, deletemember
from tkinter import messagebox

con=sqlite3.connect('library.db')
cur=con.cursor()

class Main(object): # class to represent main window
  def __init__(self, master):
    self.master = master

    def displayStatistics(evt):
      count_books = cur.execute("SELECT count(book_id) FROM books").fetchall() # get the total count of books 
      count_members = cur.execute("SELECT count(member_id) FROM members").fetchall() # get total counr of members
      taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall() # amount of books taken out
      print(count_books)
      # updaing each label with the corresponding information and respective text before and after
      self.lbl_book_count.config(text="Total: " + str(count_books[0][0]) + ' books in library') # counts amount of books in library
      self.lbl_member_count.config(text="Total members: " + str(count_members[0][0])) # amount of members in library
      self.lbl_taken_count.config(text="Taken books: " + str(taken_books[0][0])) # amount of borrowed books
      displayBooks(self) # refreshing the list
      displayMembers(self) # refreshing the list
      borrowedBooks(self) # refreshing the list

    def displayBooks(self):
      books=cur.execute("Select * FROM books").fetchall() # executes query to select all book records
      count = 0 # creates a counter variable 

      self.list_books.delete(0, END) # clears current details
      for book in books: # loop through the list of book records
        print(book) # print each book record
        self.list_books.insert(count, str(book[0]) + "-" + book[1]) # concatenates book ID with a dash + book name
        count+=1 # increments counter by one after every loop

      def bookInfo(evt):
        value=str(self.list_books.get(self.list_books.curselection())) # get ID & title of selected book
        id=value.split('-')[0] # split the string to only get the ID
        book = cur.execute("SELECT * FROM books WHERE book_id=?",(id,)) # query for full book details based on ID
        book_info=book.fetchall()
        print(book_info)
        self.list_Details.delete(0, 'end') # clears details currently in Listbox
      # fills Listbox with the book details
        self.list_Details.insert(0, "Book Name: " + book_info[0][1]) # book name
        self.list_Details.insert(1, "Author: " + book_info[0][2]) # book author  
        self.list_Details.insert(2, "Page: " + book_info[0][3]) # book pages
        self.list_Details.insert(3, "Language: " + book_info[0][4]) # book lang
        if book_info[0][5] == 0: # checks if book is available or not
          self.list_Details.insert(4, "Status : Available")
        else:
          self.list_Details.insert(4, "Status : Not Available")

      def doubleClick(evt):
        global given_id # global variable to store selected books ID
        value = str(self.list_books.get(self.list_books.curselection())) # getting selected book's info
        given_id = value.split('-')[0] # getting ID from selected book 
        give_book=GiveBook() # creating an instance of the give_book class

      self.list_books.bind('<<ListboxSelect>>', bookInfo) # bind event to refresh details on selection 
      self.tabs.bind('<<NotebookTabChanged>>', displayStatistics)
      self.list_books.bind('<Double-Button-1>', doubleClick)        

 #frames
    mainFrame=Frame(self.master)
    mainFrame.pack()
    #top
    topFrame = Frame(mainFrame, width=1500, height = 70, bg='#f8f8f8', padx=20, relief=SUNKEN, borderwidth=2)
    topFrame.pack(side=TOP,fill=X)
    #centre 
    centreFrame = Frame(mainFrame,width=1500, relief=RIDGE, bg='#e0f0f0', height=680)
    centreFrame.pack(side=TOP)
    #centre left
    centreLeftFrame = Frame(centreFrame, width=1050, height=700, bg='#f0f0f0', borderwidth=2, relief=SUNKEN)
    centreLeftFrame.pack(side=LEFT)
    #centre right
    centreRightFrame = Frame(centreFrame, width=600, height=700, bg='#f0f0f0', borderwidth=2, relief=SUNKEN)
    centreRightFrame.pack()

    #search bar
    search_bar = LabelFrame(centreRightFrame, width=590, height=150, text='Search', bg='#9bc9ff') # search area
    search_bar.pack(fill=BOTH)
    self.lbl_search=Label(search_bar, text = 'Search :', font = ' arial 12 bold', bg='#9bc9ff', fg = 'white') #text
    self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
    self.ent_search = Entry(search_bar, width = 30, bd = 10) # text box
    self.ent_search.grid(row=0,column=1, columnspan=3,padx=10,pady=10)
    self.btn_search=Button(search_bar, text = 'Search', font = ' arial 12', bg='#fcc324', fg = 'white', command = self.searchBooks) # button
    self.btn_search.grid(row=0, column =4, padx =20, pady =10)

    #####tool bar########  
    #sort bar
    sort_bar = LabelFrame(centreRightFrame, width =440, height= 175, text='Sort Box', bg= '#fcc324') # creates frame for sort bar
    sort_bar.pack(fill=BOTH)
    lbl_sort=Label(sort_bar, text = 'Sort By', font='arial 14 bold', fg='#3488ff', bg='#fcc324') # Adds text sayinh "Sort By"
    lbl_sort.grid(row=0,column=2) # specifies placing of the texy
    self.sortChoice=IntVar()
    rb1=Radiobutton(sort_bar, text='All Books', var=self.sortChoice, value=1, bg = '#fcc324') # creates a radiobutton (circle thing whre u can select)
    rb1.grid(row=1, column=0) # actually places the radibutton
    rb2=Radiobutton(sort_bar, text='In Library', var=self.sortChoice, value=2, bg = '#fcc324')
    rb2.grid(row=1, column=1) #same as other radiobutton
    rb3=Radiobutton(sort_bar, text='Borrowed Books', var=self.sortChoice, value=3, bg = '#fcc324')
    rb3.grid(row=1, column=2)  #same as other radiobutton
    btn_sort=Button(sort_bar, text='List Books', bg='#2488ff', fg = 'white', font='aria 12', command=self.listBooks) #add button to confirm sort  
    btn_sort.grid(row=1, column=3,padx=40,pady=10) #places button

   # add book
    self.iconbook=PhotoImage(file='icons/add_book.png') # load image to use as icon
    self.btnbook= Button(topFrame, text = 'Add Book', image=self.iconbook, compound=LEFT,font='arial 12 bold', command=self.addbook) # creates the actual button, and 
    self.btnbook.pack(side=LEFT, padx=5) #places button and specifys location


  #add membber
    self.iconmember= PhotoImage(file = 'icons/adduser.png') # load image to use as icon
    self.btnmember= Button(topFrame, text = 'Add Member', font='arial 12 bold', padx = 10,  command=self.addmember)  # creates the actual button
    self.btnmember.configure(image=self.iconmember, compound = LEFT)
    self.btnmember.pack(side=LEFT) #places button and specifys location


  #give book
    self.icongive=PhotoImage(file= 'icons/givebook1.png') # load image to use as icon
    self.btngive= Button(topFrame, text = 'Give Book', font='arial 12 bold', padx = 10, image=self.icongive, compound=LEFT, command=self.giveBook)  # creates the actual button
    self.btnmember.configure(image=self.iconmember, compound = LEFT)
    self.btngive.pack(side=LEFT) #places button and specifys location

  # return book
    self.iconreturn = PhotoImage(file='icons/book_return.png') # load image to use as icon
    self.btnreturn = Button(topFrame, text='Return Book', image=self.iconreturn, compound=LEFT, font='arial 12 bold', command=self.returnbook) # creates the actual button
    self.btnreturn.pack(side=LEFT, padx=5)  #places button and specifys location

  # delete book 
    self.icondelete = PhotoImage(file='icons/book_remove.png') # load image to use as icon
    self.btndelete = Button(topFrame, text='Delete Book', image=self.icondelete, compound=LEFT, font='arial 12 bold', command=self.deletebook) # creates the actual button
    self.btndelete.pack(side=LEFT, padx=5)  #places button and specifys location

  # delete member
    self.icondeletemem = PhotoImage(file='icons/delete_member.png') # load image to use as icon
    self.btndeletemem = Button(topFrame, text='Delete Member', image=self.icondeletemem, compound=LEFT, font='arial 12 bold', command=self.deletemember)  # creates the actual button
    self.btndeletemem.pack(side=LEFT, padx=5) #places button and specifys location


    
# title and image
    image_bar=Frame(centreRightFrame, width=440,height=350) # creates new frame
    image_bar.pack(fill=BOTH)
    self.title_right=Label(image_bar, text='Welcome To The Library', font = 'arial 16 bold') # adds text and makes the above frame the parent, its placed there
    self.title_right.grid(row=0)
    self.img_library=PhotoImage(file='icons/library2.png') # picks the image that will be displayed
    self.lblImg=Label(image_bar, image=self.img_library) # creates a label that will hold the image
    self.lblImg.grid(row=1)

# tabs (stats + library management)
    self.tabs= ttk.Notebook(centreLeftFrame,width=900, height=660) # creates a notebook - to create the actual tabs
    self.tabs.pack()
    self.tab1_icon=PhotoImage(file='icons/books.png') # loads an image for the first tab
    self.tab2_icon=PhotoImage(file='icons/stats.png') # loads an image for the second tab
    self.tab1=ttk.Frame(self.tabs)
    self.tab2=ttk.Frame(self.tabs)
    self.tabs.add(self.tab1,text='Library Management' , image=self.tab1_icon, compound=LEFT) # adds the first tab with title, icon and position
    self.tabs.add(self.tab2,text='Statistics' , image=self.tab2_icon, compound=LEFT) # adds the second tab with title, icon and position

    self.tab3_icon=PhotoImage(file='icons/member_info.png') # loads an image for the third tab
    self.tab3 = ttk.Frame(self.tabs)    
    self.tabs.add(self.tab3, text='Member Info', image=self.tab3_icon, compound=LEFT)

    self.member_tree = ttk.Treeview(self.tab3, columns=('ID', 'Name', 'Phone', 'Email'), show='headings') # treeview widget to display member information
    # column headings for treeview widget
    self.member_tree.heading('ID', text='Member ID')
    self.member_tree.heading('Name', text='Name')
    self.member_tree.heading('Phone', text='Phone')
    self.member_tree.heading('Email', text='Email')
    self.member_tree.pack(fill=BOTH, expand=True) # displaying the widget

    def displayMembers(self): # function that will display the members of the library
      self.member_tree.delete(*self.member_tree.get_children()) # clearing exisitng members - to prevent repetition
      members = cur.execute("SELECT * FROM members").fetchall() # fetching all members from the database
      for member in members:
        self.member_tree.insert('', END, values=member) # inserting each member into the member treeview widget

    self.tab4_icon=PhotoImage(file='icons/book_borrowed.png') # loads an image for the fourth tab
    self.tab4 = ttk.Frame(self.tabs)    
    self.tabs.add(self.tab4, text='Books Borrowed', image=self.tab4_icon, compound=LEFT) 

    self.borrowed_tree = ttk.Treeview(self.tab4, columns=('book', 'member'), show='headings') # treeview widget to display borrowed books
  # column headings for treeview widget
    self.borrowed_tree.heading('book', text='Book')
    self.borrowed_tree.heading('member', text='Member')
    self.borrowed_tree.column('book', width=300)
    self.borrowed_tree.column('member', width=300)
    self.borrowed_tree.pack(side=LEFT, fill=BOTH, expand=True) # displaying the widget

    def borrowedBooks(self): # function to display borrowed books
      borrowed_books = cur.execute("SELECT bbook_id, bmember_id FROM borrows").fetchall() #etching all records of borrowed books from the database
      self.borrowed_tree.delete(*self.borrowed_tree.get_children()) # clearing existing data
      for book_name, member_name in borrowed_books:
        self.borrowed_tree.insert('', END, values=( book_name, member_name)) # inserting each borrowed book into the borrowed book treeview widget   

  #list books :
    self.list_books= Listbox(self.tab1,width=40,height=30,bd=5,font='times 12 bold') # creates Listbox to hold book lists
    self.sb=Scrollbar (self.tab1,orient=VERTICAL) # creates a vertical scrollbar
    self. list_books.grid(row=0,column=0, padx=(10,0) ,pady=10,sticky=N) # gridding Listbox
    self.sb.config(command=self.list_books. yview) # link scrollbar to scroll Listbox 
    self. list_books.config(yscrollcommand=self.sb.set) # link Listbox to update scrollbar
    self.sb.grid(row=0,column=0,sticky=N+S+E) # gridding scrollbar

  #list details 
    self. list_Details=Listbox(self.tab1,width=80,height=30,bd=5,font='times 12 bold') # creating Listbox to display book details
    self. list_Details. grid(row=0,column=1,padx=(10,0) ,pady=10,sticky=N)

#statistics
    self.lbl_book_count= Label(self.tab2,text="", pady=20, font='verdana 14 bold') # creating label to show book count
    self.lbl_book_count. grid(row=0)
    self.lbl_member_count=Label(self.tab2,text="", pady=20, font='verdana 14 bold') # creating label to show member count
    self.lbl_member_count.grid(row=1,sticky=W)
    self.lbl_taken_count=Label(self.tab2,text="", pady=20, font='verdana 14 bold') # creating label to show taken books count
    self.lbl_taken_count.grid(row=2,sticky=W)    

    displayBooks(self) # calling the dispayBooks method
    displayStatistics(self) # calling the dispayStatistics method
    displayMembers(self) # calling the dispayMembers method

  def addbook(self): # creating method, got from other files
    add=addbook.AddBook()

  def addmember(self):
    member=addmember.AddMember() 

  def deletebook(self):
    delete = deletebook.deleteBook()  

  def returnbook(self):
    return_book = returnbook.ReturnBook()    

  def deletemember(self):
    delete = deletemember.deleteMember()      

  def searchBooks(self):
    value = self.ent_search.get() # get search text from user
    search = cur.execute("SELECT * FROM books WHERE book_name Like ?",('%'+value+'%',)).fetchall()
    print(search)
    self.list_books.delete(0, END) # clear current book list
    count = 0
    for book in search: # going through search results
      self.list_books.insert(count, str(book[0])+ "-"+book[1])
      count =+ 1

# SortBooks + REMEMBER COMMAND ON LINE 93
  def listBooks(self):
    value = self.sortChoice.get() # gets the value depending on the radiobutton clicked
    if value == 1: # value 1 = show all books
      allbooks = cur.execute("SELECT * FROM books").fetchall() # query for all books
      self.list_books.delete(0, END) # clears current listings

      count = 0 # starts looking for books from the beginning (or 0)
      for book in allbooks: # all books are listed
        self.list_books.insert(count,str(book[0]) + "-" + book[1])
        count += 1

    elif value == 2: # value 2 = show available books 
      books_in_library = cur.execute("SELECT * FROM books WHERE book_status =?", (0,)).fetchall() # gets available books
      self.list_books.delete(0, END)

      count = 0
      for book in books_in_library: # all books that are avaialable are listed
        self.list_books.insert(count,str(book[0]) + "-" + book[1])
        count += 1      
 
    else: # techically value 4 = show books that are taken out
      taken_books = cur.execute("SELECT * FROM books WHERE book_status =?", (1,)).fetchall() # gets books taken out
      self.list_books.delete(0, END)

      count = 0
      for book in taken_books:
        self.list_books.insert(count,str(book[0]) + "-" + book[1]) # all books that are taken are listed
        count += 1 

  def giveBook(self):
    give_book = givebook.GiveBook()  

class GiveBook(Toplevel):
  def __init__(self):
    Toplevel.__init__(self)
    self.geometry("650x750+550+300") # set dimensions of window
    self.title("Lend Book") # title of window
    self.resizable(False, False)

    global given_id # accessing global variable to get ID
    self.book_id=int(given_id) # storing ID of selected book
   # retrieving all books from the database and creating a list of book IDs and titles
    query = "SELECT * FROM books"
    books = cur.execute(query).fetchall()
    book_list = []
    for book in books:
      book_list.append(str(book[0])+ "-" + book[1])

    # retrieving all members from the database and creating a list of member IDs and names
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
    self.book_name = StringVar() # variable to store the selected book name
    self.lbl_name=Label(self.bottomFrame, text='Book:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324')  # creating label
    self.lbl_name.place(x=40,y=40) # placement for label
    self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.book_name) # combobox for selecting book name
    self.combo_name['values']=book_list # assigning book names to the combobox
    self.combo_name.current(self.book_id-1) # selecting the current book based on book_id
    self.combo_name.place(x=150, y=45) # placement of combobox

  #Member Name
    self.member_name = StringVar() # variable to store the selected member name
    self.lbl_phone=Label(self.bottomFrame, text='Member:', font = 'arial 15 bold', fg = 'white', bg = '#fcc324') # creating label
    self.lbl_phone.place(x=40,y=80)# placement for label
    self.combo_member = ttk.Combobox(self.bottomFrame, textvariable = self.member_name) # combobox for selecting book name
    self.combo_member['values']=member_list  # assigning book names to the combobox
    self.combo_member.place(x=150, y=85) # placement of combobox

    #button
    button = Button(self.bottomFrame, text = 'Lend Book', command = self.lendBook) # creating button that will lend book
    button.place(x=270, y=120) # button is placed
    
  def lendBook(self):
    member_name = self.member_name.get() # getting selected member
    book_name = self.book_name.get() # getting selected book

    if (book_name and member_name) != "": # checking of fields are not empty
      try:
        query = "INSERT INTO 'borrows' (bbook_id, bmember_id) VALUES(?,?)" # inserting the borrowed book record into the 'borrows' table
        cur.execute(query, (book_name, member_name))
        con.commit()
        messagebox.showinfo("Success", "Successfully added to database!", icon = 'info') # showing success message and updating book status in the database
        cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id))
        con.commit()
      except:
        messagebox.showerror("Error", "Cannot add to database", icon = 'warning')  # error message in case of failure

    else:
      messagebox.showerror("Error", "Fields cannot be empty", icon = 'warning')   # showing error if fields are empty

def main():
  root = Tk()
  app = Main(root) # instance of Main class
  root.title("Pahi's Library Management System") # title
  root.geometry("1500x750") #  dimensions 
  root.iconbitmap("icons/icon.ico") # icon of window
  root.mainloop()

if __name__ == '__main__':
  main()
  
