import tkinter as tk
from gui import picasApp

if __name__ == '__main__':
    root = tk.Tk() # main window
    app = picasApp(root) # init app
    root.mainloop()  # event loop