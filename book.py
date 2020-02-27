#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from sqlite3 import *

con=sqlite3.connect(database="login") #connection with database

#cursor=con.execute("DROP TABLE mybooks")   #deleting existing table
#con.execute('''CREATE TABLE mybooks(title varchar(50) ,author varchar(50) ,isbn varchar(50) PRIMARY KEY)''')  #creating new table

class Bookdb:
	def __init__(self):
		self.con=con.cursor()
		print("connected!")
		
	def __del__(self):
		self.con.close()

	def view(self):
		cursor=con.execute("SELECT * FROM mybooks")
		rows = cursor.fetchall()
		return rows

	def insert(self,title,author,isbn):
		sql=("INSERT INTO mybooks VALUES (?,?,?)")
		values=[title,author,isbn]
		con.execute(sql,values)
		con.commit()
		messagebox.showinfo(title="Book Database",message="New book added to databse")

	def update(self,title,author,isbn):
		tsql='UPDATE mybooks SET title=?,author=?,isbn=? WHERE isbn=?'
		vals=[title,author,isbn,isbn]
		con.execute(tsql,vals)
		con.commit()
		messagebox.showinfo(title="Book Database",message="Book Updated")

	def delete(self,isbn):
		delquery='DELETE FROM mybooks WHERE isbn = ?'
		con.execute(delquery,[isbn])
		con.commit()
		messagebox.showinfo(title="Book Database",message="Book Deleted")

db = Bookdb()

def get_selected_row(event):
	global selected_tuple
	index = list_bx.curselection()[0]
	selected_tuple = list_bx.get(index)
	title_entry.delete(0,'end')
	title_entry.insert('end',selected_tuple[0])
	author_entry.delete(0,'end')
	author_entry.insert('end',selected_tuple[1])
	isbn_entry.delete(0,'end')
	isbn_entry.insert('end',selected_tuple[2])

def view_records():
	list_bx.delete(0,'end')
	space="                                              "
	for row in db.view():
		list_bx.insert('end',row)
		

def add_book():
	i=1
	db.insert(title_text.get(),author_text.get(),isbn_text.get())		
	list_bx.delete(0,'end')
	list_bx.insert('end',(title_text.get(),author_text.get(),isbn_text.get()))
	title_entry.delete(0,'end')
	author_entry.delete(0,'end')
	isbn_entry.delete(0,'end')
	con.commit()

def delete_records():
	db.delete(isbn_text.get())
	con.commit()

def clear_screen():
	list_bx.delete(0,'end')
	title_entry.delete(0,'end')
	author_entry.delete(0,'end')
	isbn_entry.delete(0,'end')

def update_records():
	
	db.update(title_text.get(),author_text.get(),isbn_text.get())
	title_entry.delete(0,'end')
	author_entry.delete(0,'end')
	isbn_entry.delete(0,'end')
	con.commit()

def on_closing():
	dd=db
	if dd.askokcancel("Quit","Do you want to quit?"):
		messagebox.showinfo("Quit","Do you want to quit?")
		root.destroy()
		del dd

#design of application

root=Tk();
#name of application
root.title("Books Database")

#body
root.configure(background="grey")
root.geometry("850x500")
root.resizable(width=False,height=False)

#input Title,Author & ISBN.
title_label=ttk.Label(root,text="  Title",background="grey",font=("TkDefaultFont",16))
title_label.grid(row=0,column=0,sticky=W)
title_text=StringVar()
title_entry=ttk.Entry(root,width=24,textvariable=title_text)
title_entry.grid(row=0,column=1,sticky=W)

author_label=ttk.Label(root,text="  Author",background="grey",font=("TkDefaultFont",16))
author_label.grid(row=0,column=2,sticky=W)
author_text=StringVar()
author_entry=ttk.Entry(root,width=24,textvariable=author_text)
author_entry.grid(row=0,column=3,sticky=W)

isbn_label=ttk.Label(root,text="  ISBN",background="grey",font=("TkDefaultFont",16))
isbn_label.grid(row=0,column=4,sticky=W)
isbn_text=StringVar()
isbn_entry=ttk.Entry(root,width=24,textvariable=isbn_text)
isbn_entry.grid(row=0,column=5,sticky=W)

#Add Book button.
add_btn=Button(root,text="Add Book",bg="blue",fg="white",font="helvetica 10 bold",command=add_book)
add_btn.grid(row=0,column=6,sticky=W)

# Record list with scroll bar.
list_bx=Listbox(root,height=16,width=40,font="helvetica 13",bg="light blue")
list_bx.grid(row=3,column=1,columnspan=14,sticky=W+E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)


scroll_bar=Scrollbar(root)
scroll_bar.grid(row=1,column=8,rowspan=14,sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

# Extra function buttons
view_btn=Button(root,text="View All Records",bg="black",fg="white",font="helvetica 10 bold",command=view_records)
view_btn.grid(row=15,column=1)

clear_btn=Button(root,text="Clear Screen",bg="red",fg="white",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=15,column=2)

exit_btn=Button(root,text="Exit Application",bg="blue",fg="white",font="helvetica 10 bold",command=root.destroy)
exit_btn.grid(row=15,column=3)

modify_btn=Button(root,text="Modify Record",bg="purple",fg="white",font="helvetica 10 bold",command=update_records)
modify_btn.grid(row=15,column=4)

delete_btn=Button(root,text="Delete Record",bg="green",fg="white",font="helvetica 10 bold",command=delete_records)
delete_btn.grid(row=15,column=5)

root.mainloop()