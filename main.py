import tkinter as tk
import ctypes
import cfg
import Root

#For DPI Scaling
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root=tk.Tk()
root.title("Visteon Log File Viewer") #title of the root window
root.iconbitmap(cfg.icon_path) #icon of root window
root.tk.call('tk','scaling',1.6)
root.geometry("1200x800") #window size to be opened at start 

#Create root object and call mainloop
root_object=Root.RootClass(root) #root class called
root.mainloop()