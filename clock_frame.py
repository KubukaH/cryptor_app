import tkinter as tk
from tkinter.ttk import *
import time

class ClockFrame(LabelFrame):
  def __init__(self, master):
    super().__init__(master)
    self['text'] = 'Clock'

    # change the background color to black
    self.label = Label(
      self,
      style='Clock.TLabel',
      text=self.time_string(),
      font=('Digital-7', 16))
    
    self.label.pack(expand=True, fill='both')

    # schedule an update every 1 second
    self.label.after(1000, self.update)

  def time_string(self):
    hr = time.strftime('%H')
    mn = time.strftime('%M')
    sc = time.strftime('%S')
    return f'{hr} hr\n{mn} min\n{sc} s'
  
  def update(self):
    """ update the label every 1 second """

    self.label.configure(text=self.time_string())

    # schedule another timer
    self.label.after(1000, self.update)

    self.grid(row=4, column=0, padx=5, pady=(5,50), ipady=5)
