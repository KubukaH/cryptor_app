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

    self.note = tk.Toplevel(master, relief='flat')
    self.note.resizable(0, 0)
    self.note.maxsize(height=600, width=640)
    self.note.attributes('-toolwindow', True)

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

    if len(self.all_files) == 0:
      self.list_var = tk.Variable(value=["No documents"])
    else:
      self.list_var = tk.Variable(value=[
        (
          doc[0].decode('utf-8'),
          doc[1].decode('utf-8').capitalize(), 
          f"Last updated {datetime.fromisoformat(doc[7]).strftime('%d/%m/%Y %X')}"
        ) for doc in self.all_files
      ])

    self.list_box = tk.Listbox(
      self.list_frame,
      listvariable=self.list_var,
      height=8,
      selectmode=tk.BROWSE
    )

    self.vbar = tk.Scrollbar(self.list_frame, orient='vertical', command=self.list_box.yview)

    self.list_box['yscrollcommand'] = self.vbar.set
    self.vbar.pack(side='right', fill='y')
    self.list_box.pack(fill='both', expand=1)

    def selected_items(event):
      widget = event.widget
      selection = widget.curselection()
      value = widget.get(selection[0])

      if (value) is not None:
        self.del_btn['state'] = 'normal'
        self.read_btn['state'] = 'normal'

        self.read_btn['command'] = lambda : self.get_doc_id(get_id=value[0])
        self.del_btn['command'] = lambda : self.delete_doc(delete_id=value[0])

    # BUTTON FRAME
    self.btns_frame = Frame(self.note)
    self.read_btn = Button(self.btns_frame, cursor='hand2', text="Read", style='Decrypt.TButton', command=selected_items)
    self.read_btn.state(['disabled'])
    self.read_btn.grid(row=0, column=0, pady=2, padx=2)
    self.del_btn = Button(self.btns_frame, cursor='hand2', text="Delete", style='Delete.TButton')
    self.del_btn.state(['disabled'])
    self.del_btn.grid(row=0, column=1, pady=2, padx=2)
    self.btns_frame.pack(side=tk.BOTTOM, fill=tk.X)

    self.list_box.bind('<<ListboxSelect>>', selected_items)

  def get_doc_id(self, get_id):
    self.doc_id.set(get_id)
    self.note.destroy()
  
  def delete_doc(self, delete_id):
    self.deleted_id.set(delete_id)
    self.note.destroy()
