import tkinter as tk
from tkinter import ttk
import Tabs

class RootClass:

    def __init__(self,root):
        self.root=root
        self.notebook=ttk.Notebook(self.root)
        self.notebook.grid(row=2,column=0,columnspan=3,padx=10,pady=10,sticky='nesw')

        #Creating menubar
        self.menubar=tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.file_menu=tk.Menu(self.menubar,tearoff=0)
        self.file_menu.add_command(label='Open File',command=self.add_tab)
        self.file_menu.add_command(label='Delete Current Tab',command=self.delete_tab)
        self.menubar.add_cascade(label="File",menu=self.file_menu)

        #General Search Entry
        self.general_search_frame = tk.Frame(self.root)
        self.general_search_label = tk.Label(self.general_search_frame,text="Search:")
        self.general_search_label.pack(side=tk.LEFT)
        self.general_search_entry = tk.Entry(self.general_search_frame,width=24)
        self.general_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.general_search_frame.grid(row=0, column=0, padx=18, pady=(0, 10), columnspan=3, sticky="w")

        #pid entry
        self.pid_frame = tk.Frame(self.root)
        self.pid_label = tk.Label(self.pid_frame, text="PID:")
        self.pid_label.pack(side=tk.LEFT)
        self.pid_search_entry = tk.Entry(self.pid_frame)
        self.pid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pid_frame.grid(row=1, column=2, padx=20, pady=(0, 10), sticky="w")

        #tid entry
        self.tid_frame = tk.Frame(self.root)
        self.tid_label = tk.Label(self.tid_frame, text="TID:")
        self.tid_label.pack(side=tk.LEFT)
        self.tid_search_entry = tk.Entry(self.tid_frame)
        self.tid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.tid_frame.grid(row=1, column=3, padx=20, pady=(0, 10), sticky="w")

        #flag entry
        self.menu= tk.StringVar()
        self.menu.set("Flag")
        self.drop= tk.OptionMenu(self.root, self.menu,"All", "VERBOSE (V)","DEBUG (D)","INFO (I)","WARN (W)","ERROR (E)","FATAL (F)",command=self.search_using_flag)
        self.drop.grid(row=0, column=3, padx=20, pady=(0, 10), sticky="w")
        

        #Search Button frame
        self.search_frame=tk.Frame(self.root)
        self.search_frame.grid(row=1, column=0, columnspan=20, padx=22, pady=(0, 10), sticky="w")

        # search in current file 
        self.search_button = tk.Button(self.search_frame, text="Search in file",command=self.search_string)
        self.search_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # search in all
        self.search_all_button=tk.Button(self.search_frame,text="Search All",command=self.search_all)
        self.search_all_button.pack(side=tk.LEFT, fill=tk.X, expand=True)



        #To make the window responsive and scale according to size
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.tabs_object=[]
        self.active_tab=None


    def add_tab(self):
        new_tab=Tabs.Tab(self.notebook)
        self.tabs_object.append(new_tab)
        new_tab.open_file()

    def delete_tab(self):
        self.active_tab=self.notebook.select()
        self.tabs_object.remove(self.tabs_object[self.notebook.index(self.active_tab)])
        self.notebook.forget(self.active_tab)

    def search_string(self):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        flagValue=self.menu.get()
        match flagValue:
            case "Flag":
                flagValue=""
            case "All":
                flagValue=""
            case "VERBOSE (V)":
                flagValue="V"
            case "DEBUG (D)":
                flagValue="D"
            case "INFO (I)":
                flagValue="I"
            case "WARN (W)":
                flagValue="W"
            case "ERROR (E)":
                flagValue="E"
            case "FATAL (F)":
                flagValue="F"
        self.active_tab=self.notebook.select()
        Tabs.Tab.searchBtnClick(self.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue)

    def search_all(self):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        flagValue=self.menu.get()
        match flagValue:
            case "Flag":
                flagValue=""
            case "All":
                flagValue=""
            case "VERBOSE (V)":
                flagValue="V"
            case "DEBUG (D)":
                flagValue="D"
            case "INFO (I)":
                flagValue="I"
            case "WARN (W)":
                flagValue="W"
            case "ERROR (E)":
                flagValue="E"
            case "FATAL (F)":
                flagValue="F"
        
        for object in self.tabs_object :
            Tabs.Tab.searchBtnClick(object,general_search,pid,tid,flagValue)
    
    def search_using_flag(self,flagValue):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()

        match flagValue:
            case "Flag":
                flagValue=""
            case "All":
                flagValue=""
            case "VERBOSE (V)":
                flagValue="V"
            case "DEBUG (D)":
                flagValue="D"
            case "INFO (I)":
                flagValue="I"
            case "WARN (W)":
                flagValue="W"
            case "ERROR (E)":
                flagValue="E"
            case "FATAL (F)":
                flagValue="F"

        self.active_tab=self.notebook.select()
        Tabs.Tab.searchBtnClick(self.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue)



def del_tab(obj):
    pass




