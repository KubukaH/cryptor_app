from tkinter.ttk import Style

# Styles
def Stylings(root):
  style = Style(root)
  style.map("Signup.TButton",
    foreground=[('pressed', 'green'), ('active', '#c08be7')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#fff')]
  )
  style.map("Delete.TButton",
    foreground=[('pressed', 'red'), ('active', 'red')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#fff')]
  )
  style.map("Decrypt.TButton",
    foreground=[('pressed', 'green'), ('active', 'green')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#fff')]
  )
  style.map("Licence.TButton",
    foreground=[('pressed', 'green'), ('active', 'green')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#fff')]
  )
  style.map("Lougout.TButton",
    foreground=[('pressed', 'orange'), ('active', 'orange')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#fff')]
  )
  style.configure(
    "TButton",
    relief='raised',
    background="#b2c",
    foreground='#010'
  )

  style.configure("Success.TLabel", font = "Verdana 8",
    foreground='#a7f182', background="#c08be7")
  style.configure("Error.TLabel", font = "Verdana 8",
    foreground='#da2319', background="#c08be7")
  style.configure("Warning.TLabel", font = "Verdana 8",
    foreground='#f1d982', background="#c08be7")
  style.configure(
      'Clock.TLabel',
      background='black',
      foreground='red')
  
  # Color Schemes
  style.configure("Notebook.TNotebook", relief="flat")
  style.configure("Notebook.TFrame", relief="flat", background="#c08be7")

  style.configure("NotebookLabel.TLabel", relief="flat", background="#c08be7", foreground="white")

  style.configure("NotebookCheckbutton.TCheckbutton", relief="flat", background="#c08be7", foreground="white")
