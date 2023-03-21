import tkinter as tk
from tkinter.ttk import *
from models import verifyCookie
from datetime import datetime

lifont = ('Times', 12, 'italic')
class cookie_monitor(Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    session_cookie = verifyCookie()

    self.cookie_box = tk.Toplevel(master, relief='flat')
    self.cookie_box.geometry("360x100")
    self.cookie_box.attributes('-toolwindow', True)

    try:
      self.cookie_box.wm_iconbitmap("cryp.ico") 
    except: 
      pass
    
    self.cookie_box.title('Session for {}'.format(session_cookie[2].decode('utf-8').capitalize()))

    Label(self.cookie_box, text=f"Session Cookie Expires at: {session_cookie[4]}", font=lifont, relief='ridge', padding=4).pack(side='top', fill='x')

    Label(self.cookie_box, text="Do you want to continue logged in", font=lifont, relief='flat', padding=4).pack(fill='x')

    # BUTTON FRAME
    self.btns_frame = Frame(self.cookie_box, padding=(16,2))
    self.read_btn = Button(self.btns_frame, cursor='hand2', text="Yes", style='Decrypt.TButton')
    self.read_btn.state(['!disabled'])
    self.read_btn.grid(row=0, column=0, pady=2, padx=2)
    self.del_btn = Button(self.btns_frame, cursor='hand2', text="Logout", style='Delete.TButton')
    self.del_btn.state(['!disabled'])
    self.del_btn.grid(row=0, column=1, pady=2, padx=2)
    self.btns_frame.pack(side=tk.BOTTOM, fill=tk.X)
    Button(self.btns_frame, cursor='hand2', text="Close", command=lambda : self.cookie_box.destroy()).grid(row=0, column=2, padx=(64,4))
