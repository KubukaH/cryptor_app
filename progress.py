import tkinter as tk
from tkinter.ttk import *
from subprocess import run, PIPE, STDOUT
import pkg_resources
from threading import Thread
from styles import Stylings

class Download_Module(Thread):
  def __init__(self, url):
    super().__init__()

    self.url = url
    self.file_d = None

  def run(self):
    self.file_d = self.url
    return

class Progress_Frame(tk.Tk):
  def __init__(self):
    super().__init__(None)
    Stylings(self)

    self.geometry("300x80")
    self.attributes('-alpha', True)
    self.title("Downloading modules ...")
    self.resizable(0,0)

    self.progress_frame = Frame(self)
    self.progress_frame.columnconfigure(0, weight=1)
    self.progress_frame.rowconfigure(0, weight=1)

    self.progress_bar = Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='indeterminate')
    self.progress_bar.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
    self.progress_frame.pack(fill=tk.X);

    # Buttons
    self.buttons = Frame(self)
    self.buttons.pack(side='bottom')

    self.YesBtn = Button(self.buttons, text="Download Modules")
    self.YesBtn['command'] = self.check_window
    self.YesBtn.grid(row=0,column=0, sticky='w', padx=(2,64), pady=4)

    SkipBtn = Button(self.buttons, text='Skip', command=self.destroy)
    SkipBtn.grid(row=0, column=1, sticky='e')
    
    # packages to be conditionally installed with exact version
    self.required_modules = {'tkinter', 'datetime', 'sqlite3', 'hashlib', 'hmac', 'secrets', 'sys', 'subprocess', 'pkg_resources'}
    self.installed_modules = {f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set}

    self.missing_modules = self.required_modules - self.installed_modules

    #self.check_window()

  def check_window(self):
    if self.missing_modules is True:
      self.YesBtn['state'] = "normal"
      self.handle_download()
    else:
      self.YesBtn['state'] = "disabled"
      self.destroy()

  def start_downloading(self):
    self.progress_frame.tkraise()
    self.progress_bar.start(1)

  def stop_downloading(self):
    self.progress_bar.stop()

  def handle_download(self):
    self.start_downloading()
    thread = run(f'pip install --ignore-installed {" ".join([*self.missing_modules])}', stdout=PIPE, stderr=STDOUT, shell=True, text=True)
    download_thread = Download_Module(thread)
    download_thread.start()

    self.monitor(download_thread)

  def monitor(self, download_thread):
    if download_thread.is_alive():
      self.after(100, lambda: self.monitor(download_thread))
    else:
      self.stop_downloading()
      self.destroy()
