import tkinter as tk
from tkinter.ttk import *
import time

class LicencesFrame(LabelFrame):
  def __init__(self, master):
    super().__init__(master)
    self['text'] = 'Licences'

    Button(self, text='Licence', style="Licence.TButton", command=lambda: self.wait_window(LicenceDetails().top)).grid(row=0, column=0, padx=5, pady=5)
    Button(self, text='Copyright', style="Licence.TButton", command=lambda: self.wait_window(Copyright().top)).grid(row=1, column=0, padx=5, pady=5)

    self.grid(row=6, column=0, padx=5, pady=5)

class LicenceDetails(Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    self.top = tk.Toplevel(master, relief='ridge')
    self.top.geometry("256x256")
    self.top.resizable(0,0)
    self.top.title('The licence')
    self.top.attributes('-topmost', True)

    self.text_fr = tk.Text(self.top, height=12, relief='flat', bg='gray')
    self.text_fr.pack(fill='x', expand=1, side='top')
    self.text_fr.insert(1.0, "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'. \n\nThis is free software, and you are welcome to redistribute it under certain conditions; \ntype `show c' for details.")
    self.text_fr['state'] = 'disabled'

    Label(self.top, text=f"©{time.strftime('%Y')}").pack(side='bottom')

class Copyright(Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    self.top = tk.Toplevel(master, relief='ridge')
    self.top.geometry("320x256")
    self.top.resizable(0,0)
    self.top.title('Copyrights')
    self.top.attributes('-topmost', True)

    self.frame_one = Frame(self.top, relief='flat')
    self.frame_one.grid(row=0, column=0, padx=4, pady=2)

    self.text_f = tk.Text(self.frame_one, width=38, height=12)
    self.text_f.pack(fill='both', expand=1)
    self.text_f.insert(1.0, "This page is licensed under the Python Software Foundation License Version 2. \n\nExamples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License. \n\nAll rights reserved.")
    self.text_f['state'] = 'disabled'
    
    self.frame_two = Frame(self.top, relief='flat')
    self.frame_two.grid(row=1, column=0, pady=16)
    Label(self.frame_two, text=f"©{time.strftime('%Y')}. Mapenzi Mudimba").pack()
