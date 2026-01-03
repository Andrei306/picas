import tkinter as tk
from gui import PicasApp
# Run the app
if __name__ == '__main__':
    root = tk.Tk() # main window
    app = PicasApp(root) # init app
    root.mainloop()  # event loop