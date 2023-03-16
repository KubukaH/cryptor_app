#! /usr/bin/python3.11
import tkinter as tk
from tkinter.ttk import Frame, Button, Label, Notebook, Entry, Style, Checkbutton
from datetime import timedelta, datetime
from models import insertUser, insertCookie, searchUser, insertFile, retrieveFiles, verifyCookie, logout_func, retrieveSingleFile, updateFile, deleteFile
from tkinter.messagebox import showinfo, showerror, askokcancel, askyesno
from hashlib import blake2b
from hmac import compare_digest
import secrets
from tkinter.scrolledtext import ScrolledText
from line_numbers import TextLineNumbers
from side_panel import SidePanel
from files_list import file_list
import sqlite3
from label_frame import LicencesFrame, Copyright
from subprocess import run, PIPE, STDOUT
import pkg_resources
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from models import generate_keys, check_key

con = sqlite3.connect('notebookserver.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()
cur.executescript('''
  BEGIN;
  CREATE TABLE IF NOT EXISTS lockedfiles(
    file_id PRIMARY KEY UNIQUE,
    owner_name TEXT,
    data_file TEXT,
    cipher_aes TEXT,
    tag TEXT,
    session_key TEXT,
    ts TIMESTAMP,
    last_updated TIMESTAMP
  );
  CREATE TABLE IF NOT EXISTS users(
    user_id PRIMARY KEY UNIQUE,
    user_name TEXT UNIQUE,
    password TEXT,
    ts timestamp,
    last_updated DATE,
    cookie BOOLEAN
  );
  CREATE TABLE IF NOT EXISTS cookies(
    cookie_id PRIMARY KEY UNIQUE, 
    cookie_owner_id TEXT, 
    cookie_owner_username TEXT, 
    ts TIMESTAMP, 
    cookie_expire_time DATE,
    cookie_owner_ts TIMESTAMP,
    cookie_owner_last_updated DATE,
    cookie_expired BOOLEAN
  );
  CREATE TABLE IF NOT EXISTS keys(
		key_id PRIMARY KEY UNIQUE,
		key_data TEXT,
    session_key TEXT
	);
  COMMIT;
''')

AUTH_SIZE = 32
ERROR = 'Error.TLabel'
SUCCESS = 'Success.TLabel'
WARNING = 'Warning.TLabel'
f = ('Times', 14)

def welcome_frame(root):
  root.geometry('256x298')

  welcome_fr = Frame(root)

  notebook = Notebook(welcome_fr)
  notebook.pack(fill='both', pady=2, padx=2, expand=1)
  sign_in_tab(notebook, root)
  sign_up_tab(notebook, root)

  return welcome_fr

#HASHLIB SIGNATURE MAKING
def hash_sign(cookie, secret):
  h = blake2b(digest_size=AUTH_SIZE, key=secret)
  h.update(cookie)
  return h.hexdigest().encode('utf-8')

def verify(cookie, sig, secret):
  good_sig = hash_sign(cookie, secret)
  return compare_digest(good_sig, sig)

def hashed_id(pid):
  h = blake2b(digest_size=24)
  h.update(pid)
  return h.hexdigest().encode('utf-8')

def logout(root, cookie):
  logout_func(cookie_id=cookie)
  root.destroy()
  create_main_app()
  
def sign_in_tab(notebook, root):
  # function to get user data for confirmation
  def getIn():
    uname = email_tf.get().encode('utf-8')
    pwd = pwd_tf.get().encode('utf-8')

    expire_d = timedelta(minutes= 50)
    expt = datetime.now() + expire_d

    if uname != ''.encode('utf-8') and pwd != ''.encode('utf-8'):
      user = searchUser(uname)

      if user != "ERROR" and user is not None and verify(cookie=user.user_name, sig=user.password, secret=pwd) == True:
        insertCookie(
          cookie_id=hashed_id(secrets.token_bytes(24)), cookie_owner_id = user.user_id, cookie_owner_username = user.user_name, ts = datetime.now(), cookie_owner_ts = user.ts, cookie_expire_time = expt.isoformat(), cookie_owner_last_updated=user.last_updated
        )
        email_tf.delete(0, 'end')
        pwd_tf.delete(0, 'end')
        root.destroy()
        create_main_app()
      else:
        showerror('Login Status', 'Invalid username or password')
    else:
      showerror('', 'Blank Form!')

  root.title('Welcome... ')
  signin_frame = Frame(notebook, padding=16)
  Label(signin_frame, text="Username:", ).grid(row=0, column=0, sticky='w', pady=(16, 0))

  Label(
      signin_frame, 
      text="Password:", 
      ).grid(row=2, column=0, sticky='w', pady=(16, 0))
  email_tf = Entry(
      signin_frame, 
      font=f
      )
  email_tf.focus()
  email_tf.grid(row=1, column=0)
  pwd_tf = Entry(
      signin_frame,
      font=f,
      show='*'
      )
  pwd_tf.grid(row=3, column=0)
  login_btn = Button(
      signin_frame,
      text='Login',
      command=getIn,
      style='Signup.TButton',
      )
  login_btn.grid(row=4, column=0, pady=(32,8), sticky='w')

  signin_frame.pack(fill='both', expand=1)
  notebook.add(signin_frame, text="Existing account, sign in")

def sign_up_tab(notebook, root):
  # Sign Up Function to connect to DB
  pwd_label = tk.StringVar()
  confirm_pwd_label = tk.StringVar()
  terms_var = tk.IntVar()

  def set_message(message, type=None):
    message_label['text'] = message
    if type:
      message_label['style'] = type

  def validate(*args):
    password = pwd_label.get()
    confirm_password = confirm_pwd_label.get()
    if confirm_password == password:
      set_message('Good!', SUCCESS)
      signup_btn['state'] = 'normal'
      return
    if password.startswith(confirm_password):
      set_message('Incomplete!', WARNING)
      return
    set_message("Password no match!", ERROR)
    signup_btn['state'] = 'disabled'

  def save():
    uname = email_tf.get().encode('utf-8')
    secret = pwd_tf.get().encode('utf-8')
    upwd = hash_sign(cookie=uname, secret=secret)

    if uname != ''.encode('utf-8') and secret != ''.encode('utf-8'):
      if terms_var.get() != 0:
        mode = insertUser(user_id=hashed_id(secrets.token_bytes(24)), username=uname, password=upwd, timestamp=datetime.now())
        if mode == 'success':
          email_tf.delete(0, 'end')
          pwd_tf.delete(0, 'end')
          cpwd_tf.delete(0, 'end')
          showinfo('', 'Successfully saved account.')
          notebook.select(0)
        else:
          showerror('', mode)
      else:
        showerror('', 'Accept the terms to proceed.')
    else:
      showerror('', 'Blank form!')

  confirm_pwd_label.trace('w', validate)

  signup_frame = Frame(notebook, padding=(24,8,8,12))

  Label(signup_frame, text="Username:", ).grid(row=0, column=0, pady=(4, 0), sticky='w')
  email_tf = Entry(
    signup_frame, 
    font=f
    )
  email_tf.grid(row=1, column=0, sticky='w')

  Label(
    signup_frame, 
    text="Password:", 
    ).grid(row=2, column=0, pady=(4,0), sticky='w')
  pwd_tf = Entry(
    signup_frame,
    font=f,
    show='*',
    textvariable=pwd_label
    )
  pwd_tf.grid(row=3, column=0, sticky='w')

  password_label_frame = Frame(signup_frame, padding=(0,4,0,0))
  password_label_frame.grid(row=4, column=0, sticky='w')

  Label(
    password_label_frame, 
    text="Confirm Password:", 
    ).grid(row=0, column=0, pady=0, padx=0, sticky='w')
  message_label = Label(
    password_label_frame,
    style='Success.TLabel'
    )
  message_label.grid(row=0, column=1, pady=0, padx=0, sticky='w')
  cpwd_tf = Entry(
    signup_frame,
    font=f,
    show='*',
    textvariable=confirm_pwd_label
    )
  cpwd_tf.grid(row=5, column=0, sticky='w')

  terms_frame = Frame(signup_frame, padding=(0,4,0,0))
  terms_frame.grid(row=6, column=0, sticky='w')
  Checkbutton(terms_frame, text='Accept terms found here:', variable=terms_var).grid(row=0, column=0, pady=0, padx=0, sticky='w')
  Button(terms_frame, text='terms', command=lambda: signup_frame.wait_window(Copyright().top)).grid(row=1, column=0, pady=0, padx=16, sticky='w')

  signup_btn = Button(
    signup_frame,
    text='Sign up',
    style='Signup.TButton',
    command=save
    )
  signup_btn['state'] = 'disabled'
  signup_btn.grid(row=7, column=0, pady=(24,0), sticky='w')
  signup_frame.pack(fill='both', expand=True)
  notebook.add(signup_frame, text="New user, sign up")

def lock_file(session_cookie, upd_id, text_message, mode):
  res = None

  if len(text_message) > 5:
    pk = b'public_key'

    new_key_pair = check_key(pk)

    if new_key_pair is None:
      item = generate_keys()
      showerror(item)
      new_key_pair = check_key(pk)
    else:
      new_key_pair = check_key(pk)
    
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(new_key_pair.session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(text_message.encode("utf-8"))

    if mode == 'create':
      response = insertFile(file_id=hashed_id(secrets.token_bytes(24)), owner_name=session_cookie[2], data_file=ciphertext, cipher_aes=cipher_aes.nonce, tag=tag, session_key=new_key_pair.session_key, ts=datetime.now())
      res = response

    if mode == 'update':
      response = updateFile(
        file_id=upd_id.get().encode('utf-8'), 
        data_file=ciphertext,
        tag=tag,
        cipher_aes=cipher_aes.nonce,
        last_updated=datetime.now()
      )
      res = response

  else:
    res = 'The text editor is blank or the characters are less than the required minimum number. Type something first to continue.'

  return res

# MODE DECRYPT MESSAGE
def decrypt(doc_id):
  msg = ''
  if len(doc_id.get()) > 1:
    docfile = retrieveSingleFile(doc_id.get().encode('utf-8'))

    if docfile != None:
      bytes_k = check_key('private_key'.encode("utf-8"))
      private_key = RSA.import_key(bytes_k[1])

      # Decrypt Session Key
      cipher_rsa = PKCS1_OAEP.new(private_key)
      session_key = cipher_rsa.decrypt(bytes_k[2])

      # Decrypt the data with the AES session key
      cipher_aes = AES.new(session_key, AES.MODE_EAX, docfile[3])
      msg = cipher_aes.decrypt_and_verify(docfile[2], docfile[4])

    else:
      showerror("Empty Document")
  else:
    showerror("Can't perform search.")

  return msg

### Opening Frame
def base_frame_tab(root, session_cookie):
  root.geometry('976x512')
  upd_id = tk.StringVar()

  base_frame = Frame(root, width=976, height=512)
  base_frame.columnconfigure(0, weight=1)

  text_scroll = ScrolledText(base_frame, padx=5, pady=4, wrap='word', relief='groove', background='#f3ba6c2f4', foreground='#eee2e8')

  line_number = TextLineNumbers(base_frame, width=30, relief='groove', bg='#6d2bc4')
  line_number.attach(text_scroll)
  line_number.pack(side='left', fill='y')

  def _on_change(event):
    line_number.redraw()
  
  text_scroll.bind("<<Change>>", _on_change)
  text_scroll.bind("<Configure>", _on_change)
  text_scroll.event_generate("<<Paste>>")
  text_scroll.event_generate("<<Copy>>")
  text_scroll.event_generate("<<Cut>>")
  text_scroll.event_generate("<<Redo>>")
  text_scroll.event_generate("<<Undo>>")

  side_pane = SidePanel(base_frame, width=50, relief='raised')
  side_pane.attach(text_scroll)
  side_pane.pack(side='right', fill='y')
  
  def file_locker():
    lockm = lock_file(session_cookie, upd_id=None, text_message=text_scroll.get(1.0, 'end'), mode='create')
    if lockm != 'okay':
      showerror('', lockm)
      text_scroll.focus()
    else:
      new_doc()
      showinfo('', 'New document was stored!')

  def open_file_selector():
    pop_up = file_list(base_frame)
    base_frame.wait_window(pop_up.note)
    docid = pop_up.doc_id
    delid = pop_up.deleted_id
    upd_id.set(docid.get())

    if len(delid.get()) > 1:
      my_del = askokcancel('Delete file', f'Deleting : {delid.get()}.\nIrreversible action.\n\n\t\tDo you want to continue?')
      if my_del:
        deleted = deleteFile(delid.get().encode('utf-8'))
        print('Action: ', deleted)
        delid.set('')
      my_delete()
    else:
      pass

    if len(docid.get()) > 1:
      message = decrypt(docid)
      text_scroll.delete(1.0, 'end')
      text_scroll.insert(1.0, message)
      lock_btn['state'] = 'disabled'
      savebtn['state'] = 'normal'
      docid.set('')
      text_scroll.focus()
    else:
      return 'break'

  def my_delete():
    open_file_selector()

  def file_update():
    lockm = lock_file(session_cookie, upd_id, text_message=text_scroll.get(1.0, 'end'), mode='update')
    if lockm != 'okay':
      showerror('', lockm)
      text_scroll.focus()
    else:
      showinfo('', 'Document updated successfully!')

  lock_btn = Button(side_pane, text="Lock file", command=file_locker)
  savebtn = Button(side_pane, text="Save file", command=file_update)

  def new_doc():
    upd_id.set('')
    text_scroll.delete(1.0, 'end')
    savebtn['state'] = 'disabled'
    lock_btn['state'] = 'normal'
    text_scroll.focus()

  Button(side_pane, text="New file", command=new_doc).grid(row=0, column=0, padx=5, pady=10)
  lock_btn.grid(row=1, column=0, padx=5, pady=10)
  savebtn['state'] = 'disabled'
  savebtn.grid(row=2, column=0, padx=5, pady=10)
  Button(side_pane, text='Open file', command=open_file_selector).grid(row=3, column=0, padx=5, pady=10)
  Button(side_pane, text="Logout", command=lambda : logout(root, session_cookie[0])).grid(row=4, column=0, padx=5, pady=(192,3))
  LicencesFrame(side_pane)

  text_scroll.pack(fill='both', expand=1)
  
  return base_frame

def Run_Cookie(root):
  cookie = verifyCookie()
  if cookie is not None:
    if datetime.fromisoformat(cookie.cookie_expire_time) < datetime.now():
      logout_func(cookie[0])
      root.destroy()
      create_main_app()
      return
  else:
    print('Session is logged out.')
    return

def create_main_app():
  def run_cmd(cmd):
    ps = run(cmd, stdout=PIPE, stderr=STDOUT, shell=True, text=True)
    print(ps.stdout)

  # packages to be conditionally installed with exact version
  required = {'tkinter', 'datetime', 'sqlite3', 'hashlib', 'hmac', 'secrets', 'sys', 'subprocess', 'pkg_resources'}
  installed = {f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set}
  missing = required - installed

  if missing:
    run_cmd(f'pip install --ignore-installed {" ".join([*missing])}')

  session_cookie = verifyCookie()
  root = tk.Tk()
  root.title('Cryptor App')
  root.resizable(0, 0)
  
  # Styles
  style = Style(root)
  style.map("Signup.TButton",
      foreground=[('pressed', 'green'), ('active', 'blue')],
      background=[('pressed', '!disabled', 'black'), ('active', 'white')]
      )
  style.map("Delete.TButton",
      foreground=[('pressed', 'red'), ('active', 'red')],
      background=[('pressed', '!disabled', 'black'), ('active', 'red')]
      )
  style.map("Decrypt.TButton",
      foreground=[('pressed', 'green'), ('active', 'green')],
      background=[('pressed', '!disabled', 'black'), ('active', 'green')]
      )
  style.map("Licence.TButton",
      font="Consolas 6",
      foreground=[('pressed', 'green'), ('active', 'green')],
      background=[('pressed', '!disabled', 'black'), ('active', 'green')]
      )
  style.configure("Success.TLabel", font = "Verdana 8",
      foreground='green')
  style.configure("Error.TLabel", font = "Verdana 8",
      foreground='red')
  style.configure("Warning.TLabel", font = "Verdana 8",
      foreground='orange')

  # The icon 
  try: 
    root.wm_iconbitmap("cryp.ico") 
  except: 
    pass

  def lgt():
    if session_cookie is not None:
      logout_func(cookie_id=session_cookie[0])

      if askyesno('Exiting...', 'The programme is shutting down now. All unsaved data may be lost permanently. You will be logged out automatically. \n\n\t\tDo you wish to proceed?'):
        root.destroy()
    else:
      root.destroy()

  def check_run():
    Run_Cookie(root)

  root.columnconfigure(0, weight=1)
  # root.protocol("WM_DELETE_WINDOW", lgt)

  if session_cookie is not None:
    base = base_frame_tab(root, session_cookie)
    base.after(300, check_run)
    base.pack(fill='both', expand=1)
  else:
    welcome = welcome_frame(root)
    welcome.pack(fill='both', expand=1)

  root.mainloop()

#### RUN THE __MAIN__ ######
if __name__ == "__main__":
  create_main_app()
