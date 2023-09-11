import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
from datetime import time
import Tabs
import json
import os
import cfg

class RootClass:
    
    # stores the adresses of all Tab objects , declared as static 
    tabs_object=[]
    RootObject=None

    def __init__(self,root):
        self.root=root
        RootClass.RootObject=self

        #note initialised 
        self.notebook=ttk.Notebook(self.root)
        self.notebook.grid(row=2,column=0,columnspan=5,padx=10,pady=10,sticky='nesw')

        #Creating menubar
        self.menubar=tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.file_menu=tk.Menu(self.menubar,tearoff=0)
        self.package_menu=tk.Menu(self.menubar,tearoff=0)
        self.file_menu.add_command(label='Open File',command=lambda: self.add_tab(1),accelerator="Shift+O")
        self.file_menu.add_command(label='Open Multiple Files',command=lambda: self.add_multiple_tab(1),accelerator="Ctrl+Shift+O")
        self.file_menu.add_command(label='Delete Current Tab',command=lambda: self.delete_tab(1),accelerator="Shift+W")
        self.file_menu.add_command(label='Delete All Tabs',command=lambda: self.delete_all_tabs(1),accelerator="Ctrl+Shift+W")
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit',command=self.root.destroy)
        self.menubar.add_cascade(label="File",menu=self.file_menu)
        self.menubar.add_cascade(label="Packages",menu=self.package_menu)
        self.package_menu.add_command(label="Select Packages",command=self.select_package,accelerator="Shift+P")
        self.package_menu.add_command(label="Import Package File",command=self.import_package)

        #General Search Entry
        
        self.general_search_frame = tk.Frame(self.root)
        self.general_search_label = tk.Label(self.general_search_frame,text="Search:")
        self.general_search_label.grid(row=0,column=0)
        self.general_search_entry = tk.Entry(self.general_search_frame,width=24)
        self.general_search_entry.grid(row=0,column=1)
        self.general_search_frame.grid(row=0, column=0, padx=18, pady=(15, 0), columnspan=2, sticky="w")
        self.package_status_label=tk.Label(self.general_search_frame,text="")
        self.package_status_label.grid(row=1,column=1,sticky="w")

        #PID entry
        self.pid_frame = tk.Frame(self.root)
        self.pid_label = tk.Label(self.pid_frame, text="PID:")
        self.pid_label.pack(side=tk.LEFT)
        self.pid_search_entry = tk.Entry(self.pid_frame)
        self.pid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pid_frame.grid(row=1, column=2, pady=(5, 15), sticky="w")

        #Breakpoint button
        self.breakpoint_button = tk.Button(self.root, text="Add/Del Breakpoint",command=lambda: self.call_add_del_breakpoint(1))
        self.breakpoint_button.grid(row=0, column=2, sticky="w")

        #TID entry
        self.tid_frame = tk.Frame(self.root)
        self.tid_label = tk.Label(self.tid_frame, text="TID:")
        self.tid_label.pack(side=tk.LEFT)
        self.tid_search_entry = tk.Entry(self.tid_frame)
        self.tid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.tid_frame.grid(row=1, column=3, padx=(25,20), pady=(5, 15), sticky="w")

        #Flag entry
        self.flag_package_frame=tk.Frame(self.root)
        self.flag_package_frame.grid(row=0, column=4, pady=(20, 10), sticky="w")
        self.menu= tk.StringVar()
        self.menu.set("Flag")
        self.drop= tk.OptionMenu(self.flag_package_frame, self.menu,"All", "VERBOSE (V)","DEBUG (D)","INFO (I)","WARN (W)","ERROR (E)","FATAL (F)",command=self.search_using_flag)
        self.drop.grid(row=0, column=0, pady=(20, 10), sticky="w")        

        #clear button
        self.clear_button_frame=tk.Frame(self.root)
        self.clear_button_frame.grid(row=1,column=4,sticky="w")
        self.clear_button=tk.Button(self.clear_button_frame,text="Clear All",command=self.clear_all)
        self.clear_button.grid(row=0,column=0,sticky="w")
        
        #reset button
        self.reset_button=tk.Button(self.clear_button_frame,text="Reset ",command=self.call_reset)
        self.reset_button.grid(row=0,column=1,padx=30,sticky="w")

        #Timestamp Entry
        self.timestamp_frame=tk.Frame(self.root)
        self.timestamp_frame.grid(row=0,column=3,sticky="w",pady=10,padx=5)
        self.timestamp_label=tk.Label(self.timestamp_frame,text="Time Stamp")
        self.timestamp_label.grid(row=0,column=0,sticky="sw",padx=70,columnspan=2)

        self.timestamp_from_label=tk.Label(self.timestamp_frame,text="From:")
        self.timestamp_from_label.grid(row=1,column=0)
        self.timestamp_to_label=tk.Label(self.timestamp_frame,text="To:")
        self.timestamp_to_label.grid(row=2,column=0,sticky="e",padx=(0,2))

        self.timestamp_from_entry=tk.Entry(self.timestamp_frame)
        self.timestamp_from_entry.grid(row=1,column=1)
        self.timestamp_to_entry=tk.Entry(self.timestamp_frame)
        self.timestamp_to_entry.grid(row=2,column=1)

        #Search Button frame
        self.search_frame=tk.Frame(self.root)
        self.search_frame.grid(row=1, column=0, columnspan=2, padx=22, pady=(0, 10), sticky="w")

        #Search in current file button
        self.search_button = tk.Button(self.search_frame, text="Search in file",command=lambda: self.search_string(1))
        self.search_button.grid(row=0, column=0, sticky="w",padx=(0,20))
        
        #Search in all file button
        self.search_all_button=tk.Button(self.search_frame,text="Search All",command=self.search_all)
        self.search_all_button.grid(row=0, column=1, sticky="e",padx=(63,0))

        #To make the window responsive and scale according to size
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.root.bind("<Shift-O>",self.add_tab)
        self.root.bind("<Control-Shift-KeyPress-O>",self.add_multiple_tab)

        if(len(RootClass.tabs_object)==0):
            self.disable_binds()

        self.active_tab=None

    def select_package(self):
        self.package_menu.entryconfig("Select Packages",state="disabled")
        relative_path_package="cfg\package.json"
        # cfg.user_selected_packages=[]

        package_path=os.path.normpath(os.path.join(cfg.absolute_path, relative_path_package))
        self.child_window=tk.Toplevel(self.root)
        self.child_window.protocol("WM_DELETE_WINDOW",self.update_package_status)
        self.child_window.geometry("300x400")
        self.child_window.title("Packages")
        self.child_window_label=tk.Label(self.child_window,text="Select Packages:")
        self.child_window_label.grid(row=0,column=0)
        self.packages_listbox=tk.Listbox(self.child_window,selectmode="multiple")
        self.packages_listbox.grid(row=1,column=0)
        self.select_button=tk.Button(self.child_window,text="Done",command=self.get_selected_package_value)
        self.select_button.grid(row=2,column=0)

        try:
            with open(package_path,"r") as f:
                try:
                    cfg.user_package=json.load(f)
                except(Exception):
                    messagebox.showerror("Error","Package file error.\n(Please check the package file)")
        except(Exception):
            messagebox.showerror("Error","Package file error.\n(Please check the package file)")
        
        cfg.user_package_keys=[key for key in list(cfg.user_package.keys())]

        for index in range(len(cfg.user_package_keys)):
            self.packages_listbox.insert(tk.END,cfg.user_package_keys[index])

        for index in cfg.user_package_selected_indices:
            self.packages_listbox.selection_set(index)
    
    def import_package(self):
        relative_path_package="cfg"
        package_path=os.path.normpath(os.path.join(cfg.absolute_path, relative_path_package))
        os.startfile(package_path)
        
    def get_selected_package_value(self):
        cfg.user_selected_packages=[]
        selection=self.packages_listbox.curselection()
        cfg.user_package_selected_indices=list(selection)
        for index in cfg.user_package_selected_indices:
            cfg.user_selected_packages.append(cfg.user_package_keys[index])
        self.update_package_status()
    
    def update_package_status(self):
        if cfg.user_selected_packages:
            self.package_status_label.config(text="Package Search is active.",foreground="forest green")
        else:
            self.package_status_label.config(text="")
        self.package_menu.entryconfig("Select Packages",state="active")
        self.child_window.destroy()

        
    def go_to_next_element(self,event):
        event.widget.tk_focusNext().focus()
    
    #To disable binds when no tabs are present
    def disable_binds(self):
        #Disable enter binds
        self.general_search_entry.unbind('<Return>')
        self.tid_search_entry.unbind('<Return>')
        self.pid_search_entry.unbind('<Return>')
        self.timestamp_from_entry.unbind('<Return>')
        self.timestamp_to_entry.unbind('<Return>')
        self.root.unbind("<F2>")
        self.root.unbind("<F1>")
        #Disable all buttons
        self.search_button.config(state="disabled")
        self.search_all_button.config(state="disabled")
        self.menu.set("Flag")
        self.drop.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.breakpoint_button.config(state="disabled")
        self.file_menu.entryconfig("Delete Current Tab",state="disabled")
        self.file_menu.entryconfig("Delete All Tabs",state="disabled")
        self.root.unbind("<Shift-W>")
        self.root.unbind("<Control-Shift-KeyPress-W>")

    #To re enable binds
    def enable_binds(self):
        #Enable all buttons
        self.search_button.config(state="active")
        self.search_all_button.config(state="active")
        self.drop.config(state="active")
        self.clear_button.config(state="active")
        self.reset_button.config(state="active")
        self.breakpoint_button.config(state="active")
        self.file_menu.entryconfig("Delete Current Tab",state="active")
        self.file_menu.entryconfig("Delete All Tabs",state="active")
        #Enable enter binds
        self.general_search_entry.bind('<Return>', self.search_string)
        self.tid_search_entry.bind('<Return>', self.search_string)
        self.pid_search_entry.bind('<Return>', self.search_string)
        self.timestamp_from_entry.bind('<Return>', self.go_to_next_element)
        self.timestamp_to_entry.bind('<Return>', self.search_string)
        self.root.bind("<F2>",self.call_F2Bind)
        self.root.bind("<F1>",self.call_add_del_breakpoint)
        self.root.bind("<Shift-W>",self.delete_tab)
        self.root.bind("<Control-Shift-KeyPress-W>",self.delete_all_tabs)

    #Adding a new tab
    def add_tab(self,event):
        new_tab=Tabs.Tab(self.notebook)
        RootClass.tabs_object.append(new_tab)
        new_tab.open_file()
        if(len(RootClass.tabs_object)>0):
            self.enable_binds()
    
    # selecting multiple files/tabs
    def add_multiple_tab(self,event):
        files_name_list=filedialog.askopenfilenames(filetypes=[("Log Files","*.log")])
        for file_name in files_name_list:
            new_tab=Tabs.Tab(self.notebook)
            RootClass.tabs_object.append(new_tab)
            new_tab.open_multiple_files(file_name)
        if(len(RootClass.tabs_object)>0):
            self.enable_binds()

    #Deleting a tab
    def delete_tab(self,event): 
        self.active_tab=self.notebook.select()
        RootClass.tabs_object.remove(RootClass.tabs_object[self.notebook.index(self.active_tab)])
        self.notebook.forget(self.active_tab)
        if(len(RootClass.tabs_object)==0):
            self.disable_binds()
    
    def delete_all_tabs(self,event):
        while(len(RootClass.tabs_object)>0):
            self.active_tab=self.notebook.select()
            RootClass.tabs_object.remove(RootClass.tabs_object[self.notebook.index(self.active_tab)])
            self.notebook.forget(self.active_tab)
        
        if(len(RootClass.tabs_object)==0):
            self.disable_binds()



    def clear_all(self):
        #Clears all entries from all fields
        self.general_search_entry.delete(0,'end')
        self.pid_search_entry.delete(0,'end')
        self.tid_search_entry.delete(0,'end')
        self.timestamp_from_entry.delete(0,'end')
        self.timestamp_to_entry.delete(0,'end')
        self.menu.set("Flag")
        self.search_string(1)
    
    #Call reset of Tabs
    def call_reset(self):
        cfg.user_package_selected_indices=[]
        cfg.user_selected_packages=[]
        self.active_tab=self.notebook.select()
        Tabs.Tab.reset(RootClass.tabs_object[self.notebook.index(self.active_tab)])
        self.update_package_status()

    #Call F2Bind of Tabs
    def call_F2Bind(self,event):
        self.active_tab=self.notebook.select()
        Tabs.Tab.F2Bind(RootClass.tabs_object[self.notebook.index(self.active_tab)],1)

    #Call add_del_breakpoint of Tabs
    def call_add_del_breakpoint(self,event):
        self.active_tab=self.notebook.select()
        Tabs.Tab.addBreakpoint(RootClass.tabs_object[self.notebook.index(self.active_tab)],1)
            

    #Searching a string on search in file button click
    def search_string(self,event):
        #Get all values
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        flagValue=self.menu.get()
        is_timestamp_ok=True
        timestamp_from=self.timestamp_from_entry.get()
        timestamp_to=self.timestamp_to_entry.get()

        #Match for flag value
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

        #Filtering Timestamp
        #either one is empty ERROR condition
        if((timestamp_from!="" and timestamp_to=="") or (timestamp_from=="" and timestamp_to!="")):
            timestamp_from_obj=""
            timestamp_to_obj=""
            messagebox.showerror("Error", "Please enter From/To time.")
            is_timestamp_ok=False
        #both are empty OK condition
        elif(timestamp_from=="" and timestamp_to==""):
            timestamp_from_obj=""
            timestamp_to_obj=""
        #both are filled OK condition
        else:
            #get time format whether in HH:MM:SS or HH:MM:SS.MS format
            time_format_1=self.getTimeFormat(timestamp_from)
            time_format_2=self.getTimeFormat(timestamp_to)

            try:
                timestamp_from_obj = datetime.strptime(timestamp_from,time_format_1).time()
                timestamp_to_obj=datetime.strptime(timestamp_to,time_format_2).time()
                if(timestamp_to_obj.microsecond==000000 and time_format_2=='%H:%M:%S'):
                    timestamp_to_obj=self.addMilliseconds(timestamp_to_obj)
                    
            #Timestamp not in valid format ERROR condition
            except(ValueError):
                timestamp_from_obj=""
                timestamp_to_obj=""
                messagebox.showerror("Error", "Please enter a valid time format.")
                is_timestamp_ok=False

        self.active_tab=self.notebook.select()
        if(is_timestamp_ok):
            Tabs.Tab.searchBtnClick(RootClass.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)

    #Searching in all files
    def search_all(self):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        flagValue=self.menu.get()
        is_timestamp_ok=True
        timestamp_from=self.timestamp_from_entry.get()
        timestamp_to=self.timestamp_to_entry.get()
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
        
        #Filtering Timestamp
        #either one is empty ERROR condition
        if((timestamp_from!="" and timestamp_to=="") or (timestamp_from=="" and timestamp_to!="")):
            timestamp_from_obj=""
            timestamp_to_obj=""
            messagebox.showerror("Error", "Please enter From/To time.")
            is_timestamp_ok=False
        #both are empty OK condition
        elif(timestamp_from=="" and timestamp_to==""):
            timestamp_from_obj=""
            timestamp_to_obj=""
        #both are filled OK condition
        else:
            #get time format whether in HH:MM:SS or HH:MM:SS.MS format
            time_format_1=self.getTimeFormat(timestamp_from)
            time_format_2=self.getTimeFormat(timestamp_to)

            try:
                timestamp_from_obj = datetime.strptime(timestamp_from,time_format_1).time()
                timestamp_to_obj=datetime.strptime(timestamp_to,time_format_2).time()
                if(timestamp_to_obj.microsecond==000000 and time_format_2=='%H:%M:%S'):
                    timestamp_to_obj=self.addMilliseconds(timestamp_to_obj)
                    
            #Timestamp not in valid format ERROR condition
            except(ValueError):
                timestamp_from_obj=""
                timestamp_to_obj=""
                messagebox.showerror("Error", "Please enter a valid time format.")
                is_timestamp_ok=False
        
        for object in RootClass.tabs_object:
            if(is_timestamp_ok):
                Tabs.Tab.searchBtnClick(object,general_search,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)
    
    #Searching when flag value is updated
    def search_using_flag(self,flagValue):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        is_timestamp_ok=True
        timestamp_from=self.timestamp_from_entry.get()
        timestamp_to=self.timestamp_to_entry.get()

        #Switch-case for assigning flag value according to selected value
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
        
        #Filtering Timestamp
        #either one is empty ERROR condition
        if((timestamp_from!="" and timestamp_to=="") or (timestamp_from=="" and timestamp_to!="")):
            timestamp_from_obj=""
            timestamp_to_obj=""
            messagebox.showerror("Error", "Please enter From/To time.")
            is_timestamp_ok=False
        #both are empty OK condition
        elif(timestamp_from=="" and timestamp_to==""):
            timestamp_from_obj=""
            timestamp_to_obj=""
        #both are filled OK condition
        else:
            #get time format whether in HH:MM:SS or HH:MM:SS.MS format
            time_format_1=self.getTimeFormat(timestamp_from)
            time_format_2=self.getTimeFormat(timestamp_to)

            try:
                timestamp_from_obj = datetime.strptime(timestamp_from,time_format_1).time()
                timestamp_to_obj=datetime.strptime(timestamp_to,time_format_2).time()
                if(timestamp_to_obj.microsecond==000000 and time_format_2=='%H:%M:%S'):
                    timestamp_to_obj=self.addMilliseconds(timestamp_to_obj)
                    
            #Timestamp not in valid format ERROR condition
            except(ValueError):
                timestamp_from_obj=""
                timestamp_to_obj=""
                messagebox.showerror("Error", "Please enter a valid time format.")
                is_timestamp_ok=False

        self.active_tab=self.notebook.select()
        if(is_timestamp_ok):
            Tabs.Tab.searchBtnClick(RootClass.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)

    #To find the time format of timestampTo and timestampFrom
    def getTimeFormat(self,timeobject):
        partsFrom=timeobject.split(".")
        if(len(partsFrom)==1):
            time_format = '%H:%M:%S'
        else:
            time_format = '%H:%M:%S.%f'
        return time_format
    

    #To add .999 to timestampTo field if HH:MM:SS format format
    def addMilliseconds(self,timestampTo_obj):
        timestampTo_hour=timestampTo_obj.hour
        timestampTo_minute=timestampTo_obj.minute
        timestampTo_second=timestampTo_obj.second
        timestampTo_obj=time(timestampTo_hour,timestampTo_minute,timestampTo_second,999999)
        return timestampTo_obj