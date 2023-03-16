from tkinter.ttk import Style

# Styles
def Stylings(root):
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
  