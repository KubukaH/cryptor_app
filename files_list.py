import tkinter as tk
from tkinter.ttk import *
from models import retrieveFiles, verifyCookie
from datetime import datetime

lifont = ('Times', 17, 'italic')
class file_list(Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.pack()
    session_cookie = verifyCookie()
    self.all_files = retrieveFiles(session_cookie[2])
    self.doc_id = tk.StringVar()
    self.deleted_id = tk.StringVar()

    self.note = tk.Toplevel(master, relief='flat', takefocus=True)
    self.note.geometry("860x400")
    self.note.attributes('-topmost', True)

    try:
      self.note.wm_iconbitmap("cryp.ico") 
    except: 
      pass
    
    self.note.title('Session for {}'.format(session_cookie[2].decode('utf-8').capitalize()))

    Label(self.note, text=f"Documents for {session_cookie[2].decode('utf-8').capitalize()} : total = {len(self.all_files)}", font=lifont, relief='ridge', padding=4).pack(side='top', fill='x')

    self.list_frame = Frame(self.note)
    self.list_frame["borderwidth"] = 4
    self.list_frame["relief"] = "groove"
    self.list_frame["padding"] = 4
    self.list_frame.pack(fill='both', expand=1)

    # use treeview for making a list
    self.lst_files = Treeview(self.list_frame, selectmode='browse')

    # attach scrollbar
    self.lst_scrbar = Scrollbar(self.list_frame, command=self.lst_files.yview)
    self.lst_scrbar.pack(side='right', fill='y')

    self.lst_files['yscrollcommand'] = self.lst_scrbar.set

    # list columns
    self.lst_files['columns'] = ('file_id', 'owner_name', 'created', 'updated')

    # formatting columns
    self.lst_files.column('#0', width=0, stretch='no')
    self.lst_files.column('file_id', width=188, anchor='center')
    self.lst_files.column('owner_name', width=10, anchor='center')
    self.lst_files.column('created', width=20, anchor='center')
    self.lst_files.column('updated', width=20, anchor='center')

    # format headings
    self.lst_files.heading('#0', text='', anchor='center')
    self.lst_files.heading('file_id', text='File ID', anchor='center')
    self.lst_files.heading('owner_name', text='File Owner', anchor='center')
    self.lst_files.heading('created', text='Created', anchor='center')
    self.lst_files.heading('created', text='Updated', anchor='center')

    # populate the treeview table
    global count
    count = 0
    for item in self.all_files:
      self.lst_files.insert(parent='', index='end', iid=count, text='', values=(item[0].decode('utf-8'), item[1].decode('utf-8'), datetime.fromisoformat(item[6]).strftime('%d-%m-%Y %X'), datetime.fromisoformat(item[7]).strftime('%d-%m-%Y %X') ))
      count += 1

    # BUTTON FRAME
    self.btns_frame = Frame(self.note, padding=(32,2))
    self.read_btn = Button(self.btns_frame, cursor='hand2', text="Read", style='Decrypt.TButton')
    self.read_btn.state(['disabled'])
    self.read_btn.grid(row=0, column=0, pady=2, padx=2)
    self.del_btn = Button(self.btns_frame, cursor='hand2', text="Delete", style='Delete.TButton')
    self.del_btn.state(['disabled'])
    self.del_btn.grid(row=0, column=1, pady=2, padx=2)
    self.btns_frame.pack(side=tk.BOTTOM, fill=tk.X)
    Button(self.btns_frame, cursor='hand2', style="Lougout.TButton", text="Close", command=lambda : self.note.destroy()).grid(row=0, column=2, padx=(128,4))

    def select_record(event):
      widget = event.widget
      value = widget.focus()

      values = self.lst_files.item(value, 'values')

      self.del_btn['state'] = 'normal'
      self.read_btn['state'] = 'normal'

      self.read_btn['command'] = lambda : self.get_doc_id(get_id=values[0])
      self.del_btn['command'] = lambda : self.delete_doc(delete_id=values[0])

    # bind the treeview selection mode
    self.lst_files.bind('<<TreeviewSelect>>', select_record)

    self.lst_files.pack(fill='both', expand=True)

  def get_doc_id(self, get_id):
    self.doc_id.set(get_id)
    self.note.destroy()
  
  def delete_doc(self, delete_id):
    self.deleted_id.set(delete_id)
    self.note.destroy()
