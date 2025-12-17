import tkinter as tk
from gui import picasApp

# Run the app
if __name__ == '__main__':
    root = tk.Tk() # main window
    app = picasApp(root) # init app
    root.mainloop()  # event loop