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
    
    #static variables
    tabs_object=[]     # stores the adresses of all Tab objects , declared as static 
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
        self.help_menu=tk.Menu(self.menubar,tearoff=0)
        self.view_menu=tk.Menu(self.menubar,tearoff=0)
        self.file_menu.add_command(label='Open File',command=lambda: self.add_tab(1),accelerator="Ctrl+O")
        self.file_menu.add_command(label='Open Multiple Files',command=lambda: self.add_multiple_tab(1),accelerator="Ctrl+Shift+O")
        self.file_menu.add_command(label='Delete Current Tab',command=lambda: self.delete_tab(1),accelerator="Ctrl+W")
        self.file_menu.add_command(label='Delete All Tabs',command=lambda: self.delete_all_tabs(1),accelerator="Ctrl+Shift+W")
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit',command=self.root.destroy)
        self.menubar.add_cascade(label="File",menu=self.file_menu)
        self.menubar.add_cascade(label="Packages",menu=self.package_menu)
        self.menubar.add_cascade(label="View",menu=self.view_menu)
        self.menubar.add_cascade(label="Help",menu=self.help_menu)
        
        self.package_menu.add_command(label="Select Packages",command=lambda: self.select_package(1),accelerator="Ctrl+P")
        self.package_menu.add_command(label="Import Package File",command=self.import_package)
        self.help_menu.add_command(label="User Manual",command=self.open_user_manual_window)
        self.view_menu.add_command(label="Show Breakpoints",command=self.show_breakpoints)

        #Initialize packages child window to None
        self.child_window=None

        #General Search Entry
        self.general_search_frame = tk.Frame(self.root)
        self.general_search_label = tk.Label(self.general_search_frame,text="Search:")
        self.general_search_label.grid(row=0,column=0)
        self.general_search_entry = tk.Entry(self.general_search_frame,width=24)
        self.general_search_entry.grid(row=0,column=1)
        self.general_search_frame.grid(row=0, column=0, padx=18, pady=(15, 0), sticky="w")
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
        self.tid_label = tk.Label(self.tid_frame, text="  TID:")
        self.tid_label.pack(side=tk.LEFT)
        self.tid_search_entry = tk.Entry(self.tid_frame)
        self.tid_search_entry.pack(side=tk.RIGHT)
        self.tid_frame.grid(row=1, column=3, pady=(5, 15), sticky="w")
  

        #flag entry
        self.flag_frame=tk.Frame(self.root)
        self.flag_frame.grid(row=0, column=4, pady=(20, 10), sticky="w")
        self.flag_entry_menu=tk.Menubutton(self.flag_frame,text="Select Flag",relief="raised")
        self.flag_entry_menu.grid(row=0, column=0)
        self.flag_entry_menu.menu=tk.Menu(self.flag_entry_menu,tearoff=0)
        self.flag_entry_menu["menu"]=self.flag_entry_menu.menu
        
        # initialising each flag
        self.verbose=tk.IntVar()
        self.debug=tk.IntVar()
        self.info=tk.IntVar()
        self.warn=tk.IntVar()
        self.error=tk.IntVar()
        self.fatal=tk.IntVar()
        
        # initially set all flags true
        self.verbose.set(1)
        self.debug.set(1)
        self.info.set(1)
        self.warn.set(1)
        self.error.set(1)
        self.fatal.set(1)    

        # checkbuttons for flags
        self.flag_entry_menu.menu.add_checkbutton(label="VERBOSE (V)", variable=self.verbose)
        self.flag_entry_menu.menu.add_checkbutton(label="DEBUG (D)", variable=self.debug)
        self.flag_entry_menu.menu.add_checkbutton(label="INFO (I)", variable=self.info)
        self.flag_entry_menu.menu.add_checkbutton(label="WARN (W)", variable=self.warn)
        self.flag_entry_menu.menu.add_checkbutton(label="ERROR (E)", variable=self.error)
        self.flag_entry_menu.menu.add_checkbutton(label="FATAL (F)", variable=self.fatal)

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
        self.timestamp_frame.grid(row=0,column=3,sticky="w")
        self.timestamp_label=tk.Label(self.timestamp_frame,text="Time Stamp")
        self.timestamp_label.pack(side=tk.TOP)
        
        self.timestamp_from_frame=tk.Frame(self.timestamp_frame)
        self.timestamp_from_frame.pack(side=tk.TOP)
        self.timestamp_from_label=tk.Label(self.timestamp_from_frame,text="From:")
        self.timestamp_from_label.pack(side=tk.LEFT)
        self.timestamp_to_frame=tk.Frame(self.timestamp_frame)
        self.timestamp_to_frame.pack(side=tk.TOP)
        self.timestamp_to_label=tk.Label(self.timestamp_to_frame,text="    To:")
        self.timestamp_to_label.pack(side=tk.LEFT)

        self.timestamp_from_entry=tk.Entry(self.timestamp_from_frame)
        self.timestamp_from_entry.pack(side=tk.RIGHT,fill=tk.X,)
        self.timestamp_to_entry=tk.Entry(self.timestamp_to_frame)
        self.timestamp_to_entry.pack(side=tk.RIGHT,fill=tk.X)

        #Search Button frame
        self.search_frame=tk.Frame(self.root)
        self.search_frame.grid(row=1, column=0, padx=22, pady=(0, 10), sticky="w")

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

        #Binds for root window, set to on by default
        self.root.bind("<Control-o>",self.add_tab)
        self.root.bind("<Control-p>",self.select_package)
        self.root.bind("<Control-Shift-KeyPress-O>",self.add_multiple_tab)
        self.root.bind("<Control-f>",lambda event : self.control_f_bind(1))

        #Disable all binds if no tab is present
        if(len(RootClass.tabs_object)==0):
            self.disable_binds()

        self.active_tab=None

    #Shifts the focus to general search entry on Ctrl+F
    #Called from self.root.bind in __init__
    def control_f_bind(self,event):
        self.general_search_entry.focus_set()
    
    #Opens a child window and shows the selected breakpoints in the current tab.
    #Called from menubar (Show Breakpoints)
    def show_breakpoints(self):
        breakpoints_window=tk.Toplevel(self.root)
        breakpoints_window.title("Current Breakpoints")
        breakpoints_window.iconbitmap(cfg.icon_path)
        breakpoints_window.geometry("1200x500")

        #Gets list of breakpoints for the current tab
        self.active_tab=self.notebook.select()
        list_of_breakpoints=Tabs.Tab.getBreakpoints(RootClass.tabs_object[self.notebook.index(self.active_tab)])

        breakpoints_textwidget=tk.Text(breakpoints_window,wrap="word")
        breakpoints_textwidget.tag_config("breakpointadd", foreground="red")
        
        breakpoints_scrollbar=tk.Scrollbar(breakpoints_window,orient='vertical')
        breakpoints_scrollbar.config(command=breakpoints_textwidget.yview)
        breakpoints_scrollbar.pack(pady=10,side=tk.RIGHT,fill=tk.Y)
        breakpoints_textwidget.config(yscrollcommand=breakpoints_scrollbar.set)

        breakpoints_textwidget.pack(pady=10,side=tk.LEFT,fill=tk.BOTH,expand=True)

        breakpoints_textwidget.config(state=tk.NORMAL) #set text widget to edit mode
        breakpoints_textwidget.delete("1.0",tk.END) #delete all previous contents of text widget
        for breakpoint in list_of_breakpoints:
            breakpoints_textwidget.insert(tk.INSERT,breakpoint) #Insert all breakpoints in the text widget

        breakpoints_textwidget.tag_add("breakpointadd", "1.0",tk.END) 
        breakpoints_textwidget.config(state=tk.DISABLED)


    # opens user manual
    # Called from menubar (user manual)
    def open_user_manual_window(self):

        self.user_manual_window=tk.Toplevel(self.root)
        self.user_manual_window.iconbitmap(cfg.icon_path)
        self.user_manual_window.geometry("1000x600")
        self.user_manual_window.title("User Manual")

        self.user_manual_frame=tk.Frame(self.user_manual_window)
        self.user_manual_frame.pack(expand=True, fill=tk.BOTH,pady=(20,0))

        self.manual_widget=tk.Text(self.user_manual_frame,wrap="word")
        self.manual_widget.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.user_manual_scrollbar=tk.Scrollbar(self.user_manual_frame)
        self.user_manual_scrollbar.pack(expand=True, fill=tk.BOTH)
        self.manual_widget.config(yscrollcommand=self.user_manual_scrollbar.set)
        self.user_manual_scrollbar.config(command=self.manual_widget.yview)

        self.close_manual_button=tk.Button(self.user_manual_window,text="Close",command=self.user_manual_window.destroy)
        self.close_manual_button.pack(pady=20)

        user_manual_relative_path="cfg/help/help.txt"
        user_manual_path=os.path.normpath(os.path.join(cfg.absolute_path, user_manual_relative_path))

        try:    
                # opens user manual in text widget
                with open(user_manual_path, 'r') as file:
                    content = file.read()
                    self.manual_widget.delete(1.0, tk.END)
                    self.manual_widget.insert(tk.END, content)
                    self.manual_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
                self.manual_widget.delete(1.0, tk.END)
                self.manual_widget.insert(tk.END, "User Manual not found!")
                self.manual_widget.config(state=tk.DISABLED)



    def select_package(self,event):

        #Used to check for any erorrs in json parsing
        error_flag=0

        #Disable binds to allow only one child window to spawn
        self.package_menu.entryconfig("Select Packages",state="disabled")
        self.root.unbind('<Control-p>')
        relative_path_package="cfg\package.json"    #Path of the .json file
        package_path=os.path.normpath(os.path.join(cfg.absolute_path, relative_path_package)) #Path of package file joined with absolute path

        #Load the packages.json file to packages listbox
        try:
            with open(package_path,"r") as f:
                try:
                    cfg.user_package=json.load(f)
                except(Exception):
                    messagebox.showerror("Error","Package file error.\n(Please check the package file)")
                    error_flag=1
                    self.update_package_status()
        except(Exception):
            messagebox.showerror("Error","Package file error.\n(Please check the package file)")
            error_flag=1
            self.update_package_status()
            
        if(error_flag==0):
            #Child window spawned
            self.child_window=tk.Toplevel(self.root)
            self.child_window.iconbitmap(cfg.icon_path)
            self.child_window.protocol("WM_DELETE_WINDOW",self.update_package_status)
            self.child_window.geometry("400x400")
            self.child_window.resizable(True,False)
            self.child_window.title("Packages")
            self.child_window_label=tk.Label(self.child_window,text="Select Packages",font=("Arial",8,"bold"))
            self.child_window_label.pack(side=tk.TOP,pady=10)

            #Listbox frame
            self.listbox_frame=tk.Frame(self.child_window)
            self.listbox_frame.pack(side=tk.TOP)

            #Listbox of user packages
            self.packages_listbox=tk.Listbox(self.listbox_frame,selectmode="multiple",height=14,width=25)
            self.packages_listbox.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

            #Scrollbar for listbox
            self.child_window_scrollbar=tk.Scrollbar(self.listbox_frame)
            self.child_window_scrollbar.pack(expand=True, fill=tk.BOTH)
            self.packages_listbox.config(yscrollcommand=self.child_window_scrollbar.set)
            self.child_window_scrollbar.config(command=self.packages_listbox.yview)

            #Done button
            self.select_button=tk.Button(self.child_window,text="Done",command=self.get_selected_package_value)
            self.select_button.pack(side=tk.TOP,pady=10)

            #List of keys from the json file
            cfg.user_package_keys=[key for key in list(cfg.user_package.keys())]

            #Put the keys into the packages listbox
            for index in range(len(cfg.user_package_keys)):
                self.packages_listbox.insert(tk.END,cfg.user_package_keys[index])

            #Reload previous selection of packages(history)
            for index in cfg.user_package_selected_indices:
                self.packages_listbox.selection_set(index)
    
    #Opens the folder directory to import cfg file
    #Called when import package is clicked
    def import_package(self):
        relative_path_package="cfg"
        package_path=os.path.normpath(os.path.join(cfg.absolute_path, relative_path_package))
        user_choice=messagebox.askokcancel("Info","You will be redirected to the packages.json directory.\nPlease restart the application once you update the package file.")
        if(user_choice):
            os.startfile(package_path)

    #Gets packages that have been selected by the user
    #Called when DONE is clicked from select_package
    def get_selected_package_value(self):
        cfg.user_selected_packages=[]
        selection=self.packages_listbox.curselection()
        cfg.user_package_selected_indices=list(selection)
        for index in cfg.user_package_selected_indices:
            cfg.user_selected_packages.append(cfg.user_package_keys[index])
        self.update_package_status()
    
    #Updates package status label below searchbar
    #Rebinds the disabled binds which were disabled when child window was spawned
    #Called when DONE is pressed or CLOSE button is clicked from select_package
    def update_package_status(self):
        if cfg.user_selected_packages:
            self.package_status_label.config(text="Package Search is active.",foreground="forest green")
        else:
            self.package_status_label.config(text="")
        self.package_menu.entryconfig("Select Packages",state="active")
        self.root.bind("<Control-p>",self.select_package)
        if(self.child_window!=None): #Destroy called only when child window is present
            self.child_window.destroy()

    #Used to move focus from Timestamp To to Timestamp From
    #Called when Enter is pressed in Timestamp To entry.
    def go_to_next_element(self,event):
        event.widget.tk_focusNext().focus()
    
    #To disable binds when no tabs are present
    #Called when no files are opened
    def disable_binds(self):
        #Disable enter binds
        self.general_search_entry.unbind('<Return>')
        self.tid_search_entry.unbind('<Return>')
        self.pid_search_entry.unbind('<Return>')
        self.timestamp_from_entry.unbind('<Return>')
        self.timestamp_to_entry.unbind('<Return>')
        self.root.unbind("<F2>")
        self.root.unbind("<F1>")
        self.root.unbind("<Control-w>")
        self.root.unbind("<Control-Shift-KeyPress-W>")
        #Disable all buttons
        self.search_button.config(state="disabled")
        self.search_all_button.config(state="disabled")
        self.flag_entry_menu.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.breakpoint_button.config(state="disabled")
        self.file_menu.entryconfig("Delete Current Tab",state="disabled")
        self.file_menu.entryconfig("Delete All Tabs",state="disabled")
        self.view_menu.entryconfig("Show Breakpoints",state="disabled")

    #To re enable binds
    #Called when atleast one file is present
    def enable_binds(self):
        #Enable all buttons
        self.search_button.config(state="active")
        self.search_all_button.config(state="active")
        self.flag_entry_menu.config(state="active")
        self.clear_button.config(state="active")
        self.reset_button.config(state="active")
        self.breakpoint_button.config(state="active")
        self.file_menu.entryconfig("Delete Current Tab",state="active")
        self.file_menu.entryconfig("Delete All Tabs",state="active")
        self.view_menu.entryconfig("Show Breakpoints",state="active")
        #Enable enter binds
        self.general_search_entry.bind('<Return>', self.search_string)
        self.tid_search_entry.bind('<Return>', self.search_string)
        self.pid_search_entry.bind('<Return>', self.search_string)
        self.timestamp_from_entry.bind('<Return>', self.go_to_next_element)
        self.timestamp_to_entry.bind('<Return>', self.search_string)
        self.root.bind("<F2>",self.call_F2Bind)
        self.root.bind("<F1>",self.call_add_del_breakpoint)
        self.root.bind("<Control-w>",self.delete_tab)
        self.root.bind("<Control-Shift-KeyPress-W>",self.delete_all_tabs)

    #Adding a new tab
    #Called when open a file is pressed
    def add_tab(self,event):
        new_tab=Tabs.Tab(self.notebook)
        RootClass.tabs_object.append(new_tab)
        new_tab.open_file("singlefile")
        if(len(RootClass.tabs_object)>0):
            self.enable_binds()
    
    # selecting multiple files/tabs
    #Called when open multiple files is pressed
    def add_multiple_tab(self,event):
        files_name_list=filedialog.askopenfilenames(filetypes=[("Log Files","*.log"),("Gz Files","*.gz")])
        for file_name in files_name_list:
            new_tab=Tabs.Tab(self.notebook)
            RootClass.tabs_object.append(new_tab)
            new_tab.open_file(file_name)
        if(len(RootClass.tabs_object)>0):
            self.enable_binds()

    #Deleting a tab
    #Called when delete tab is pressed
    def delete_tab(self,event): 
        self.active_tab=self.notebook.select()
        RootClass.tabs_object.remove(RootClass.tabs_object[self.notebook.index(self.active_tab)])
        self.notebook.forget(self.active_tab)
        if(len(RootClass.tabs_object)==0):
            self.disable_binds()
    
    #Delete all tabs
    #Called when delete all tabs is presssed
    def delete_all_tabs(self,event):
        while(len(RootClass.tabs_object)>0):
            self.active_tab=self.notebook.select()
            RootClass.tabs_object.remove(RootClass.tabs_object[self.notebook.index(self.active_tab)])
            self.notebook.forget(self.active_tab)
        
        if(len(RootClass.tabs_object)==0):
            self.disable_binds()

    #Clears all the fields and calls empty search
    #Called when clear all button is pressed
    def clear_all(self):
        #Clears all entries from all fields
        self.general_search_entry.delete(0,'end')
        self.pid_search_entry.delete(0,'end')
        self.tid_search_entry.delete(0,'end')
        self.timestamp_from_entry.delete(0,'end')
        self.timestamp_to_entry.delete(0,'end')
        self.verbose.set(1)
        self.debug.set(1)
        self.info.set(1)
        self.warn.set(1)
        self.error.set(1)
        self.fatal.set(1)
        self.search_string(1)

    
    #Clears all fields+breakpoint+packages
    #Called when reset button is pressed
    def call_reset(self):
        cfg.user_package_selected_indices=[]
        cfg.user_selected_packages=[]
        self.active_tab=self.notebook.select()
        Tabs.Tab.reset(RootClass.tabs_object[self.notebook.index(self.active_tab)])
        self.update_package_status()

    #Call F2Bind of Tabs object
    #Called when F2 is pressed
    def call_F2Bind(self,event):
        self.active_tab=self.notebook.select()
        Tabs.Tab.F2Bind(RootClass.tabs_object[self.notebook.index(self.active_tab)],1)

    #Call addDelBreakpoint of Tabs object
    #Called when F1 is pressed
    def call_add_del_breakpoint(self,event):
        self.active_tab=self.notebook.select()
        Tabs.Tab.addDelBreakpoint(RootClass.tabs_object[self.notebook.index(self.active_tab)],1)
    
    #Getting all the input fields values and passing it to searchBtnClick
    #Called when search in file is pressed
    def search_string(self,event):
        #Get all values
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        is_timestamp_ok=True
        timestamp_from=self.timestamp_from_entry.get()
        timestamp_to=self.timestamp_to_entry.get()

        # selected flag value appended in selected_flag_list
        selected_flag_list=[]
        if self.verbose.get():
            selected_flag_list.append("V")
        if self.debug.get():
            selected_flag_list.append("D")
        if self.info.get():
            selected_flag_list.append("I")
        if self.warn.get():
            selected_flag_list.append("W")
        if self.error.get():
            selected_flag_list.append("E")
        if self.fatal.get():
            selected_flag_list.append("F")
        # if nothing is selected in flag entry
        if(len(selected_flag_list)==0):
            selected_flag_list.append(" ")        

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
            Tabs.Tab.searchBtnClick(RootClass.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,selected_flag_list,timestamp_from_obj,timestamp_to_obj)

    #Searching in all files
    #Called when search all is pressed
    def search_all(self):
        general_search=self.general_search_entry.get()
        pid=self.pid_search_entry.get()
        tid=self.tid_search_entry.get()
        is_timestamp_ok=True
        timestamp_from=self.timestamp_from_entry.get()
        timestamp_to=self.timestamp_to_entry.get()

        # selected flag enteries appended here
        selected_flag_list=[]
        if self.verbose.get():
            selected_flag_list.append("V")
        if self.debug.get():
            selected_flag_list.append("D")
        if self.info.get():
            selected_flag_list.append("I")
        if self.warn.get():
            selected_flag_list.append("W")
        if self.error.get():
            selected_flag_list.append("E")
        if self.fatal.get():
            selected_flag_list.append("F")

        # if nothing is selected 
        if(len(selected_flag_list)==0):
            selected_flag_list.append(" ")
                
       
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
                Tabs.Tab.searchBtnClick(object,general_search,pid,tid,selected_flag_list,timestamp_from_obj,timestamp_to_obj)
    


    #To find the time format of timestampTo and timestampFrom
    #Called from search function
    def getTimeFormat(self,timeobject):
        splitted_timeobject=timeobject.split(".")
        if(len(splitted_timeobject)==1):
            time_format = '%H:%M:%S'
        else:
            time_format = '%H:%M:%S.%f'
        return time_format
    

    #To add .999 to timestampTo field if it is in HH:MM:SS format
    #Called from search function
    def addMilliseconds(self,timestampTo_obj):
        timestampTo_hour=timestampTo_obj.hour
        timestampTo_minute=timestampTo_obj.minute
        timestampTo_second=timestampTo_obj.second
        timestampTo_obj=time(timestampTo_hour,timestampTo_minute,timestampTo_second,999999)
        return timestampTo_obj