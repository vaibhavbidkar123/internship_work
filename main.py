import tkinter as tk
import ctypes
import Root

#For DPI Scaling
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root=tk.Tk()
root.title(" Visteon Log File Viewer")
root.tk.call('tk','scaling',1.6)
root.geometry("1200x800")

#Create root object and call mainloop
root_object=Root.RootClass(root)
root.mainloop()