import tkinter as tk
from tkinter.ttk import *
from textwrap import TextWrapper

class LicencesFrame(LabelFrame):
  def __init__(self, master):
    super().__init__(master)
    self['text'] = 'Licences'

    Button(self, text='Licence', style="Licence.TButton", command=lambda: self.wait_window(LicenceDetails().top)).grid(row=0, column=0, padx=5, pady=5)
    Button(self, text='Copyright', style="Licence.TButton", command=lambda: self.wait_window(Copyright().top)).grid(row=1, column=0, padx=5, pady=5)

    self.grid(row=5, column=0, padx=5, pady=5)

class LicenceDetails(Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    self.top = tk.Toplevel(master, relief='ridge')
    self.top.geometry("256x256")
    self.top.resizable(0,0)
    self.top.title('The licence')
    self.top.attributes('-topmost', True)

class Copyright(Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    self.top = tk.Toplevel(master, relief='ridge')
    self.top.geometry("320x256")
    self.top.resizable(0,0)
    self.top.title('Copyrights')
    self.top.attributes('-topmost', True)

    self.text_wrapper = TextWrapper()
    self.text_wrapper.wrap = "This page is licensed under the Python Software Foundation License Version 2. Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License. All rights reserved."
    self.text_wrapper.initial_indent = ''
    self.text_wrapper.width = 35

    self.frame_one = Frame(self.top, relief='flat')
    self.frame_one.grid(row=0, column=0, padx=4, pady=2)

    self.text_f = tk.Text(self.frame_one, width=38, height=12)
    self.text_f.pack(fill='both', expand=1)
    self.text_f.insert(1.0, "This page is licensed under the Python Software Foundation License Version 2. \n\nExamples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License. \n\nAll rights reserved.")
    self.text_f['state'] = 'disabled'
    
    self.frame_two = Frame(self.top, relief='flat')
    self.frame_two.grid(row=1, column=0, pady=16)
    Label(self.frame_two, text='©2023. Mapenzi Mudimba').pack()
