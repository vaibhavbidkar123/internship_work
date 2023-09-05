import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from datetime import time
import Tabs

class RootClass:

    def __init__(self,root):
        self.root=root
        self.notebook=ttk.Notebook(self.root)
        self.notebook.grid(row=2,column=0,columnspan=5,padx=10,pady=10,sticky='nesw')

        #Creating menubar
        self.menubar=tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.file_menu=tk.Menu(self.menubar,tearoff=0)
        self.file_menu.add_command(label='Open File',command=self.add_tab)
        self.file_menu.add_command(label='Delete Current Tab',command=self.delete_tab)
        self.file_menu.add_command(label='Exit',command=self.root.destroy)
        self.menubar.add_cascade(label="File",menu=self.file_menu)

        #General Search Entry
        self.general_search_frame = tk.Frame(self.root)
        self.general_search_label = tk.Label(self.general_search_frame,text="Search:")
        self.general_search_label.pack(side=tk.LEFT)
        self.general_search_entry = tk.Entry(self.general_search_frame,width=24)
        self.general_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.general_search_frame.grid(row=0, column=0, padx=18, pady=(0, 10), columnspan=2, sticky="w")

        #PID entry
        self.pid_frame = tk.Frame(self.root)
        self.pid_label = tk.Label(self.pid_frame, text="PID:")
        self.pid_label.pack(side=tk.LEFT)
        self.pid_search_entry = tk.Entry(self.pid_frame)
        self.pid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pid_frame.grid(row=1, column=2, padx=20, pady=(5, 15), sticky="w")

        #TID entry
        self.tid_frame = tk.Frame(self.root)
        self.tid_label = tk.Label(self.tid_frame, text="TID:")
        self.tid_label.pack(side=tk.LEFT)
        self.tid_search_entry = tk.Entry(self.tid_frame)
        self.tid_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.tid_frame.grid(row=1, column=3, padx=(25,20), pady=(5, 15), sticky="w")

        #Flag entry
        self.menu= tk.StringVar()
        self.menu.set("Flag")
        self.drop= tk.OptionMenu(self.root, self.menu,"All", "VERBOSE (V)","DEBUG (D)","INFO (I)","WARN (W)","ERROR (E)","FATAL (F)",command=self.search_using_flag)
        self.drop.grid(row=0, column=4, padx=50, pady=(20, 10), sticky="w")
        

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
        self.search_button = tk.Button(self.search_frame, text="Search in file",command=self.search_string)
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

        self.tabs_object=[]
        self.active_tab=None

    #Adding a new tab
    def add_tab(self):
        new_tab=Tabs.Tab(self.notebook)
        self.tabs_object.append(new_tab)
        new_tab.open_file()

    #Deleting a tab
    def delete_tab(self):
        self.active_tab=self.notebook.select()
        self.tabs_object.remove(self.tabs_object[self.notebook.index(self.active_tab)])
        self.notebook.forget(self.active_tab)

    #Searching a string on search in file button click
    def search_string(self):
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
            Tabs.Tab.searchBtnClick(self.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)

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
        
        for object in self.tabs_object:
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
            Tabs.Tab.searchBtnClick(self.tabs_object[self.notebook.index(self.active_tab)],general_search,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)

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



def del_tab(obj):
    pass




