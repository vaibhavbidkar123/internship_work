from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
import re
import cfg
import Root

class Tab:

    logFormat= r'^(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]).*\n$' #regular expression for breakpoint

    def __init__(self,new_tab_object):

        # tab frame created for the notebook
        self.tab_frame=ttk.Frame(new_tab_object)

        #new text widget will be initialised whenever a new file is opened
        self.text_widget_frame=tk.Frame(self.tab_frame)
        self.text_widget_frame.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.text_widget=tk.Text(self.text_widget_frame,wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.tab_frame.grid(row=0,column=0,pady=0)
        
        # breakpoints for a particular tab is stored here 
        self.breakpointCursor=0
        self.breakpoints=[]
        self.breakpointsLineNum={}
        self.existingBreakPoints=[]
        self.text_widget.tag_config("breakpointadd", foreground="red")
        self.text_widget.tag_config("breakpointremove", foreground="black")
        
        # for file name purpose 
        self.file_path=""
        self.file_name="..."
        self.notebook=new_tab_object

        # number of entries found per tab for particular search 
        self.matchesfound=0
        self.matchesfound_label=tk.Label(self.tab_frame,text="")
        self.matchesfound_label.pack(side=tk.LEFT,)
        
        # scrollbar 
        self.scrollbar=tk.Scrollbar(self.text_widget_frame,orient='vertical')
        self.scrollbar.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text_widget.yview)
        self.text_widget.config(yscroll=self.scrollbar.set)

        #file name to be viewed on tab 
        new_tab_object.add(self.tab_frame,text=self.file_name)
     
   #Opening a file and displaying all its contents 
    def open_file(self,file_path_passed):
        if(file_path_passed=="singlefile"):
            self.file_path=filedialog.askopenfilename(filetypes=[("Log Files","*.log")]) #opens only log files 
        else:
            self.file_path=file_path_passed
        self.file_path_name=self.file_path
        self.file_path_name=self.file_path_name.split("/")
        self.file_name=self.file_path_name[-1]  #file name
        content=True
        if self.file_path:
            #Changing tab name
            self.notebook.add(self.tab_frame,text=self.file_name) #tab name updated to file name
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete("1.0",tk.END) #delete previous content
            try:
                with open(self.file_path,'r',encoding="ANSI",errors="replace") as file:
                    while content:
                        content=file.readline()
                        self.text_widget.insert(tk.INSERT,content) #insert entries line by line 
                self.text_widget.config(state=tk.DISABLED)
            except(Exception):
                self.text_widget.delete("1.0",tk.END)
        else:
            #DELETE TAB HAS TO BE CALLED HERE
            self.notebook.add(self.tab_frame,text="Empty File")  # if no file is selected
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete("1.0",tk.END)
            self.text_widget.config(state=tk.DISABLED)
        self.scrollbar.config(command=self.text_widget.yview)
    
    def searchBtnClick(self,general_search_string,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj):
        self.general_search(general_search_string,pid,tid,flagValue,timestamp_from_obj,timestamp_to_obj)

    
    def addBreakpoint(self,event):
        #TRY-CATCH for getting the selection
        try:
            #Get selection and find its line number
            text=self.text_widget.selection_get()
            newlineChars=text.count("\n")
            if(newlineChars>1):
                raise Exception
            if not re.match(Tab.logFormat, text):
                raise Exception
            count=self.text_widget.count("1.0",tk.SEL_FIRST,"lines")
        except(Exception):
            messagebox.showerror("Error", "Invalid breakpoint selection\n(You can only add a log line as a breakpoint.)")
            return
        #TRY-CATCH for getting the line number
        #This logic is used to increment line number by one.
        #By default, line number starts from zero, but we need it from 1 onwards.
        try:
            lineNum=count[0]
        except(Exception):
            lineNum=None
        if(lineNum==None):
            lineNum=1
        else:
            lineNum+=1

        #TRY-CATCH for getting the line number of the selected line.
        try:
            lineNumStart=str(lineNum)+".0"
            lineNumEnd=str(lineNum)+".end"
            #Delete breakpoint if it already exists and reset formatting
            if(text in list(self.breakpointsLineNum.keys())):
                del self.breakpointsLineNum[text]     
                self.existingBreakPoints.remove(text)       
                self.text_widget.tag_add("breakpointremove", lineNumStart, lineNumEnd)
            #Else add the breakpoint
            #Storing into breakpointlinenum dictionary KEY:the log entry VALUE:the start and end
            else:
                self.breakpointsLineNum[text]=[lineNumStart,lineNumEnd]
                self.existingBreakPoints.append(text)
                #Change the particular line number's colour to red
                self.text_widget.tag_remove("breakpointremove",lineNumStart, lineNumEnd)
                self.text_widget.tag_add("breakpointadd", lineNumStart, lineNumEnd)
        except(Exception):
            pass
    
    def F2Bind(self,event):
        #Circular f2 movement
        #try catch since exception is generated if you try to access empty list element
        try:
            listOfValues=[]
            for item in self.existingBreakPoints:
                listOfValues.append(self.breakpointsLineNum[item])
            listOfValues.sort(key=lambda element: float(element[0])) #SORT the list based on line number order.
            currentElementToDisplay=listOfValues[self.breakpointCursor][0]
            self.text_widget.see(currentElementToDisplay)
            self.breakpointCursor+=1
            if(self.breakpointCursor==len(listOfValues)):
                self.breakpointCursor=0
        except(Exception):
            pass

    def reset(self):
    #Resets breakpoints + entry
        self.breakpointsLineNum.clear()
        Root.RootClass.clear_all(Root.RootClass.RootObject)

    def sanitizeOrString(self,input_string):
    #Convert searchtext to list based on '|' split
    #Convert each string to lowercase characters for case insensitive search
        text_list=input_string.split("|")
        new_text_list=[]
        for element in text_list:
            new_element=element.strip()
            new_element=new_element.lower()
            new_text_list.append(new_element)
        return new_text_list

    def checkSearchText(self,content,searchText_list):
        #Return true if content exists in searchText_list
        #Else return false if there is no match
        flag=0
        for element in searchText_list:
            if element in content.casefold():
                flag=1
        return flag

    def appendPackagesToSearchText(self,searchText):
        searchText=searchText.strip('|')
        for key in cfg.user_selected_packages:
            for element in cfg.user_package[key]:
                searchText+="|"+element
        newsearchtext=searchText.strip('|')
        return newsearchtext

    
                    #--MAIN SEARCH ALGORITHM--#
    def general_search(self,searchText,pid,tid,flagValue,timestampFrom,timestampTo):
        self.breakpointCursor=0 #breakpoint cursor set to zero
        self.existingBreakPoints=[] #breakpoint list is empty initially
        self.matchesfound=0  
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0",tk.END)
        timeRecieved=False #time is not recieved 
        time_to_check_format='%H:%M:%S.%f'  #time format to check 
        #if empty time recieved then set the timerecieved to true
        if(timestampFrom!="" and timestampTo!=""):
            timeRecieved=True
        #sanitize general search for piping (or condition)
        searchText=self.appendPackagesToSearchText(searchText)    
        searchText_list=self.sanitizeOrString(searchText)
        pid_list=self.sanitizeOrString(pid) #sanitize pid list
        tid_list=self.sanitizeOrString(tid) #sanitize tid list
        content=True
        if(self.file_path==""):
            pass
        else:
            try:
                with open(self.file_path,"r", encoding="ANSI", errors="replace") as f:
                    while content:
                        content=f.readline()
                        content_split=content.split()
                        if(len(content_split)>4):
                            temp = content.split(":") #split each entry
                            content_split=[":".join(temp[0:3])] + temp[3:] # join first 3 elements of the list 
                            content_split_first_part=content_split[0].split() #first part splitted 
                            content_time=content_split_first_part[1] #time
                            content_time_obj=datetime.strptime(content_time,time_to_check_format).time() #to validate the time 
                            content_pid=content_split_first_part[2] #pid
                            content_tid=content_split_first_part[3] #tid
                            content_flagValue=content_split_first_part[4] #flag
                            

                            #main search filter condition 
                            if pid or tid or searchText or flagValue or timeRecieved:
                                if (not pid or content_pid in pid_list) and (not tid or content_tid in tid_list) and (self.checkSearchText(content,searchText_list)) and (content_flagValue==flagValue or flagValue=="")  and ((timestampFrom=="" and timestampTo=="") or (timestampFrom <= content_time_obj <= timestampTo) ):
                                    if content in list(self.breakpointsLineNum.keys()) and content not in self.existingBreakPoints:
                                        startIndex=self.text_widget.index(tk.INSERT) #EXTRA
                                        endIndex=startIndex.split(".")[0]+".end"
                                        self.breakpointsLineNum[content]=[startIndex,endIndex] #UPTILL HERE FOR ALL
                                        self.existingBreakPoints.append(content)
                                    
                                    self.text_widget.insert(tk.INSERT,content)
                                    self.matchesfound+=1 #increment matches found
                            #No entry in any field, display entire contents
                            else:
                                if content in list(self.breakpointsLineNum.keys()) and content not in self.existingBreakPoints:
                                    startIndex=self.text_widget.index(tk.INSERT)
                                    endIndex=startIndex.split(".")[0]+".end"
                                    self.breakpointsLineNum[content]=[startIndex,endIndex]
                                    self.existingBreakPoints.append(content)
                                self.text_widget.insert(tk.INSERT,content)
                                self.matchesfound+=1
                        else:
                            #If content is not in default LOG line format, control come here
                            #All fields should be empty except general search for this to execute
                            if not pid and not tid and flagValue=="" and timeRecieved==False and self.checkSearchText(content,searchText_list):
                                if content in list(self.breakpointsLineNum.keys()) and content not in self.existingBreakPoints:
                                    startIndex=self.text_widget.index(tk.INSERT)
                                    endIndex=startIndex.split(".")[0]+".end"
                                    self.breakpointsLineNum[content]=[startIndex,endIndex]
                                    self.existingBreakPoints.append(content)
                                self.text_widget.insert(tk.INSERT,content)
                                self.matchesfound+=1
            except(Exception):
                messagebox.showerror("Error", "Some error occured")
        self.scrollbar.config(command=self.text_widget.yview) #adjust scroll bar as per the content size 
        self.text_widget.config(state=tk.DISABLED,yscroll=self.scrollbar.set)
        self.matchesfound_label.config(text="Entries found: "+str(self.matchesfound)) # print matches found 
        #To add colour to the line
        for element in self.existingBreakPoints:
            startIndex=self.breakpointsLineNum[element][0]
            endIndex=self.breakpointsLineNum[element][1]
            self.text_widget.tag_add("breakpointadd", startIndex,endIndex)
