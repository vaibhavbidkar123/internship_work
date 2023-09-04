from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Tab:
    def __init__(self,new_tab_object):
        self.tab_frame=ttk.Frame(new_tab_object)
        self.text_widget=tk.Text(self.tab_frame,wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT,fill=tk.X,expand=True)
        self.tab_frame.grid(row=4,column=0)
        self.file_path=""
        self.file_name="..."
        self.notebook=new_tab_object

        new_tab_object.add(self.tab_frame,text=self.file_name)
    
    def open_file(self):
        self.file_path=filedialog.askopenfilename(filetypes=[("Log Files","*.log")])
        self.file_path_name=self.file_path
        self.file_path_name=self.file_path_name.split("/")
        self.file_name=self.file_path_name[-1]
        content=True
        if self.file_path:
            #Changing tab name
            self.notebook.add(self.tab_frame,text=self.file_name)
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete("1.0",tk.END)
            try:
                with open(self.file_path,'r',encoding="ANSI",errors="replace") as file:
                    while content:
                        content=file.readline()
                        self.text_widget.insert(tk.INSERT,content)
                self.text_widget.config(state=tk.DISABLED)
            except(Exception):
                self.text_widget.delete("1.0",tk.END)
        else:
            #DELETE TAB HAS TO BE CALLED HERE
            self.notebook.add(self.tab_frame,text="Empty File")
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete("1.0",tk.END)
            self.text_widget.config(state=tk.DISABLED)
    
    def searchBtnClick(self,general_search_string,pid,tid,flagValue):
        self.general_search(general_search_string,pid,tid,flagValue)
    
    def general_search(self,searchText,pid,tid,flagValue):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0",tk.END)
        pid_list=pid.split(",")
        tid_list=tid.split(",")
        content=True
        try:
            with open(self.file_path,"r", encoding="ANSI", errors="replace") as f:
                while content:
                    content=f.readline()
                    content_split=content.split()
                    if(len(content_split)>4):
                        temp = content.split(":")
                        content_split=[":".join(temp[0:3])] + temp[3:]
                        content_split_first_part=content_split[0].split()
                        # content_time=content_split_first_part[1]
                        # content_time_obj=datetime.strptime(content_time,time_to_check_format).time()
                        content_pid=content_split_first_part[2]
                        content_tid=content_split_first_part[3]
                        content_flagValue=content_split_first_part[4]

                        if pid or tid or searchText or flagValue:
                            if (not pid or content_pid in pid_list) and (not tid or content_tid in tid_list) and (searchText.casefold() in content.casefold()) and (content_flagValue==flagValue or flagValue==""):
                                self.text_widget.insert(tk.INSERT,content)
                        #No entry in any field, display entire contents
                        else:
                            # if content in list(cfg.breakpointsLineNum.keys()):
                            #     startIndex=cfg.text_widget.index(INSERT)
                            #     endIndex=startIndex.split(".")[0]+".end"
                            #     cfg.breakpointsLineNum[content]=[startIndex,endIndex]
                            #     cfg.existingBreakPoints.append(content)
                            self.text_widget.insert(tk.INSERT,content)
                    else:
                        #If content is not in default LOG line format, control come here
                        #All fields should be empty except general search for this to execute
                        if not pid and not tid and flagValue=="" and searchText in content:
                            # if content in list(cfg.breakpointsLineNum.keys()):
                            #     startIndex=cfg.text_widget.index(INSERT)
                            #     endIndex=startIndex.split(".")[0]+".end"
                            #     cfg.breakpointsLineNum[content]=[startIndex,endIndex]
                            #     cfg.existingBreakPoints.append(content)
                            self.text_widget.insert(tk.INSERT,content)
                    

        except(Exception):
            messagebox.showerror("Error", "Some error occured")
        self.text_widget.config(state=tk.DISABLED)


    

            
    



