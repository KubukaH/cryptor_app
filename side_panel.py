import tkinter as tk

class SidePanel(tk.Canvas):
	def __init__(self, *args, **kwargs):
		tk.Canvas.__init__(self, *args, **kwargs)
		self.textwidget = None

	def attach(self, text_widget):
		self.textwidget = text_widget