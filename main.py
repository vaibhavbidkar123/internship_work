import tkinter as tk
import ctypes
import Root


ctypes.windll.shcore.SetProcessDpiAwareness(1)

root=tk.Tk()
root.tk.call('tk','scaling',1.6)
root.geometry("1200x800")

root_object=Root.RootClass(root)
root.mainloop()