from tkinter.ttk import Style

# Styles
def Stylings(root):
  style = Style(root)
  style.map("Signup.TButton",
    foreground=[('pressed', 'green'), ('active', '#111139')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', '#3fa8a5')]
  )
  style.map("Delete.TButton",
    foreground=[('pressed', 'red'), ('active', 'red')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', 'red')]
  )
  style.map("Decrypt.TButton",
    foreground=[('pressed', 'green'), ('active', 'green')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', 'green')]
  )
  style.map("Licence.TButton",
    foreground=[('pressed', 'green'), ('active', 'green')],
    background=[('pressed', '!disabled', '#3fa8a5'), ('active', 'green')]
  )
  style.configure("Success.TLabel", font = "Verdana 8",
    foreground='green', background="#111139")
  style.configure("Error.TLabel", font = "Verdana 8",
    foreground='red', background="#111139")
  style.configure("Warning.TLabel", font = "Verdana 8",
    foreground='orange', background="#111139")
  
  # Color Schemes
  style.configure("Notebook.TNotebook", relief="flat")
  style.configure("Notebook.TFrame", relief="flat", background="#111139")

  style.configure("NotebookLabel.TLabel", relief="flat", background="#111139", foreground="white")

  style.configure("NotebookCheckbutton.TCheckbutton", relief="flat", background="#111139", foreground="white")
