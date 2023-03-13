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
    self.note.maxsize(height=600, width=560)
    self.note.attributes('-toolwindow', True)
    self.docs = []

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
        (doc[1], datetime.fromisoformat(doc[6]).strftime('%d/%m/%Y %X')) for doc in self.all_files
      ])

    self.txtframe = tk.Listbox(
      self.list_frame,
      listvariable=self.list_var,
      height=8,
      selectmode=tk.EXTENDED
    )

    # self.txtframe = tk.Text(self.list_frame)
    # self.txtframe['state'] = 'normal'
    self.vbar = tk.Scrollbar(self.list_frame, orient='vertical', command=self.txtframe.yview)
    #    Label(self.txtframe, text=doc[1].decode('utf-8'), background='white').grid(row=i, column=0, padx=2, pady=2)
    #    Label(self.txtframe, text=f"Last Saved: {date.strftime('%d-%m-%Y : %X')}", background='white').grid(row=i, column=1, pady=2, padx=2)
    #    Button(self.txtframe, cursor='hand2', text="Read", command=lambda docid=doc[0] : self.get_doc_id(docid), style="Decrypt.TButton").grid(row=i, column=2, pady=2, padx=2)
    #    Button(self.txtframe, cursor='hand2', text="Delete", command=lambda docid=doc[0] : self.delete_doc(docid), style='Delete.TButton').grid(row=i, column=3, pady=2, padx=2)

    self.txtframe['yscrollcommand'] = self.vbar.set
    self.vbar.pack(side='right', fill='y')
    self.txtframe['state'] = 'disabled'
    self.txtframe.pack(fill='both', expand=1)

  def get_doc_id(self, get_id):
    self.doc_id.set(get_id.decode('utf-8'))
    self.note.destroy()
  
  def delete_doc(self, delete_id):
    self.deleted_id.set(delete_id.decode('utf-8'))
    self.note.destroy()
