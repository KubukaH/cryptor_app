import tkinter as tk
from tkinter.ttk import *
from subprocess import run, PIPE, STDOUT
from threading import Thread
from libraries import missing_libs

class Download_Module(Thread):
  def __init__(self, url):
    super().__init__()

    self.url = url
    self.file_d = None

  def run(self):
    self.file_d = self.url

class Progress_Frame(tk.Tk):
  def __init__(self):
    super().__init__()
    #self.pack()

    # self.note = tk.Toplevel(master, relief='flat', takefocus=True)
    self.geometry("300x50")
    self.attributes('-alpha', True)
    self.title("Downloading modules ...")

    self.progress_frame = Frame(self)
    self.progress_frame.columnconfigure(0, weight=1)
    self.progress_frame.rowconfigure(0, weight=1)

    self.progress_bar = Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='indeterminate')
    self.progress_bar.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
    self.progress_frame.pack(fill=tk.X);

    # packages to be conditionally installed with exact version
    missing = missing_libs()
    
    if missing:
      self.handle_download(self.run_cmd(f'pip install --ignore-installed {" ".join([*missing])}'))

  def run_cmd(self, cmd):
    ps = run(cmd, stdout=PIPE, stderr=STDOUT, shell=True, text=True)
    print(ps.stdout)

  def start_downloading(self):
    self.progress_frame.tkraise()
    self.progress_bar.start(30)

  def stop_downloading(self):
    self.progress_bar.stop()

  def handle_download(self, thread):
    self.start_downloading()
    download_thread = Download_Module(thread)
    download_thread.start()

    self.monitor(download_thread)

  def monitor(self, download_thread):
    if download_thread.is_alive():
      self.after(100, lambda: self.monitor(download_thread))
    else:
      self.stop_downloading()
      self.destroy()

if __name__ == '__main__':
    app = Progress_Frame()
    app.mainloop()