import concurrent.futures
import csv
import multiprocessing as mp
import os
import re
import time
import tkinter
import webbrowser
import sys
from multiprocessing import freeze_support
from logging import PlaceHolder
from pathlib import Path
from tkinter import *  # type: ignore
from tkinter import filedialog, messagebox, ttk

import pandas as pd
import pyautogui as gui
from validate_email import validate_email


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def information():
    global inf_
    inf_ = Toplevel()
    inf_.title("Information")
    inf_.geometry("550x400")
    icon_select= resource_path("icons/select.ico")
    inf_.iconbitmap(icon_select)

    high = ttk.Treeview(inf_)
    low = ttk.Treeview(inf_)

    high.config(height=5)
    low.config(height=5)
    
    high['columns'] = ("NUM_emails", "Time")
    low['columns'] = ("NUM_emails", "Time")

    high.column("#0", width=0, stretch=NO)
    high.column("NUM_emails", anchor=W, width=105,)
    high.column("Time", anchor=CENTER, width=75)
    
    low.column("#0", width=0, stretch=NO)
    low.column("NUM_emails", anchor=W, width=105,)
    low.column("Time", anchor=CENTER, width=60)
    
    high.heading("#0", text="", anchor=W)
    high.heading("NUM_emails", text="Num. of emails", anchor=W)
    high.heading("Time", text="Time", anchor=CENTER)

    low.heading("#0", text="", anchor=W)
    low.heading("NUM_emails", text="Num. of emails", anchor=W)
    low.heading("Time", text="Time", anchor=CENTER)
    
    data_high = [
        ["1.000", "4-5 M"],
        ["5.000", "17-20 M"],
        ["10.000", "32 M"],
        ["50.000", "3 H"],
        ["100.000", "6 H"]
    ]

    data_low = [
        ["1.000", "N/A"],
        ["5.000", "N/A"],
        ["10.000", "N/A"],
        ["50.000", "N/A"],
        ["100.000", "N/A"]
    ]
     
    count=0
    for record in data_high:
        high.insert(parent='', index="end", iid=count, text = "high", values=(record[0], record[1]))
        count +=1

    count_=0
    for _record in data_low:
        low.insert(parent='', index="end", iid=count_, text = "low", values=(_record[0], _record[1]))
        count_ +=1

    high_label = Label(inf_, text="8 cores, 16 Logical Processors", padx=3, pady=2, anchor=CENTER)
    high_label.grid(column=0, row=1)

    low_label = Label(inf_, text="4 cores, 8 Logical Processors", padx=3, pady=2, anchor=CENTER)
    low_label.grid(column=1, row=1)   

    high.grid(column=0, row=2)
    low.grid(column=1, row=2)

    cpu_n = int(mp.cpu_count())
    main_inf = Label(inf_, text=f"""*** Email validator 2022 ***


This is a open source project made by me Superjoa10 (github by the same name)
that uses tkinter as the GUI, Pandas, and the PY3-validate-email libraries.
The way it works is it takes either csv or excel files, divides it by the 
number of logical processors (your machine having {cpu_n} processors)
and for each one, a process is created that checks the emails concurrently

It takes this amount of time per size of the file:
""", anchor=CENTER)
    main_inf.grid(column=0, row=0, columnspan = 2, sticky=N)

def callback(url):
    webbrowser.open_new(url)    

def choose_file(): #this is the second page
    global inf
    inf = Toplevel()
    inf.title("Choose file")
    inf.geometry("750x710")
    icon_email_search= resource_path("icons/email_search.ico")
    inf.iconbitmap(icon_email_search)
    screen_width = inf.winfo_screenwidth()
    screen_height = inf.winfo_screenheight()

    frame = Frame(inf, highlightbackground="black", highlightthickness=2.)
    frame.grid(column=0, row=0, padx=5, pady=5)

    # Create a Treeview widget
    global tree
    tree = ttk.Treeview(frame)
    tree.pack(ipady=175, ipadx=80)
    
    global frame_inf
    frame_inf = Frame(inf, highlightbackground="gray", highlightthickness=2.)
    frame_inf.grid(column=0, row=1, ipady=10, ipadx=0)

    #select arquivo e treeview
    open_btn = Button(frame_inf, text="Select file to search", command=select_file, padx=3, pady=2, anchor= CENTER)
    open_btn.grid(column= 0, row=0, padx=10, pady=5)

    global frame_inf2
    frame_inf2 = LabelFrame(inf, text="Informations from file", highlightbackground="gray", highlightthickness=1.)
    frame_inf2.grid(column=1, row=0, padx=5, ipady=70, ipadx=25)

    global label
    label = Label(frame_inf2, anchor=W, text='''
Status: Please select a file!
this program accepts either Excel or CSV.''')
    label.pack()

    global label_doc
    label_doc = Label(frame_inf2, anchor=W, text=f"")
    label_doc.pack()

    global label_size
    label_size = Label(frame_inf2, anchor=W, text=f"")
    label_size.pack()

    label_WARNING = Label(frame_inf2, anchor=W, text="""
THIS PAGE WON'T WORK
WHILE THE SEARCH IS RUNNING""",
font="bold")
    label_WARNING.pack()

    label_cool = Label(frame_inf2, anchor=E, text="""
There is currently no way to check the 
progress of the search, other than the console
due to the limitations of the Tkinter program.
""")
    label_cool.pack(side = BOTTOM)

    label_cool = Label(frame_inf2, anchor=E, text="""
If you close this program while it's
running, it'll leave behind some throw away 
files, result from the division of the original
file. If you wait for it to end it'll delete
them automatically
""")
    label_cool.pack(side = BOTTOM)

def select_file():
    #adds file to screan
    global filename
    filename = filedialog.askopenfilename(title="Open a File", filetype=(("All Files", "*.*"), ("xlrd files", ".*xlrd"), ("xlxs files", ".*xlsx")))
    if filename:
            try:
                global df
                filename = r"{}".format(filename)
                df = pd.read_csv(filename, sep=';', engine= 'python' ,encoding='cp860')
    
                number_lines = int(sum(1 for row in (open(filename, encoding='cp860'))))
                label_doc.config(text=f"Type of doc: CSV")
                label.config(text="Status: File found")
                label_size.config(text=f"Number of lines: {number_lines}")

                run_btn = Button(frame_inf, text="search", command=lambda:run_main(filename) , padx=3, pady=2, anchor= CENTER)
                run_btn.grid(column=1, row=0, padx=10, pady=5, sticky=E)

            except ValueError:
                df = pd.read_excel(filename)
                label.config(text="Status: File found")
                label_doc.config(text="Type of doc: Excel")
                inf.geometry("1000x710")

                run_btn = Button(frame_inf, text="search", command=lambda:run_main(filename) , padx=3, pady=2, anchor= CENTER)
                run_btn.grid(column=1, row=0, padx=10, pady=5, sticky=E)
            except FileNotFoundError:
                label.config(text="File Not Found")
    clear_treeview()
    # Add new data in Treeview widget
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = (df.to_numpy().tolist())
    for row in df_rows:
        tree.insert("", "end", values=row)
    tree.pack()

def clear_treeview():
    tree.delete(*tree.get_children())

def doc_type(filename):
    regex_csv = re.compile(r'.*\.(csv)$')
    regex_xlsx = re.compile(r'.*\.(xlsx)$')
    if re.fullmatch(regex_csv, filename):
        return True
    elif re.fullmatch(regex_xlsx, filename):
        return False
    else:
        raise TypeError("Not a valid file type")

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False

def correct_csv(correct_emails):
    global SAVEinfo
    crrc_email = pd.DataFrame(correct_emails)
    directory = filedialog.askdirectory()
    crrc_file = str(directory + "/correct_emails.csv")
    crrc_email.to_csv(crrc_file, 
        encoding="utf-8", 
        index = False,
        header= False)
    SAVEinfo = Label(end, text="correct emails file saved at chosen directory", padx=3, pady=2, anchor=W)
    SAVEinfo.grid(column=0, row=4, columnspan=2)
    
def incorrect_csv(incorrect_emails):
    global SAVEinfo
    incrrc_email = pd.DataFrame(incorrect_emails)
    directory = filedialog.askdirectory()
    incrrc_file = str(directory + "/incorrect_emails.csv")
    incrrc_email.to_csv(incrrc_file, 
        encoding="utf-8", 
        index = False,
        header= False)
    SAVEinfo = Label(end, text="Incorrect emails file saved at chosen directory", padx=3, pady=2, anchor=W)
    SAVEinfo.grid(column=0, row=4, columnspan=2)

def main(prompt):
        valid_email = []
        invalid_email = []
        line_count= 0 
        start_ = time.perf_counter()
        email_num = pd.read_csv(prompt)
        for x, emoil in email_num.iterrows():
                if line_count == 0:  
                    line_count += 1   
                else:
                    line_count += 1
                    email = emoil[0]
                    #is_valid = isValid(email)
                    isexist= validate_email(email, smtp_timeout=1)
                    print(f"""
------------------------------------------------------------------------------------
email: {email}
valido = {isexist}
place = {line_count}/{rowsize}
------------------------------------------------------------------------------------""")
                    
                    if isexist == True:
                        valid_email.append(email)
                    elif isexist == None:
                        invalid_email.append(email)
                    elif isexist == False:
                        invalid_email.append(email)

                    elif isexist == 'True':
                        valid_email.append(email)
                    elif isexist == 'None':
                        invalid_email.append(email)
                    elif isexist == 'False':
                        invalid_email.append(email)

                    else:
                        invalid_email.append(email)
        finish_ = time.perf_counter()
        for o in range(10):
            print("--------------------------------------------------------------------------------------------------------------------")
        print(f"finish time for file:{prompt} time: {finish_-start_}")
        if(os.path.exists(prompt) and os.path.isfile(prompt)):
            os.remove(prompt)
            print("file deleted")
        else:
            print("file not found")
        #find way to return invalid_email and append
        cleber = [valid_email, invalid_email]
        return cleber

def run_main(filename):#this has the result page
    global rowsize
    global names_list
    doc = doc_type(filename)
    cpu_n = int(mp.cpu_count())
    messagebox.showinfo("Logical cores info", f"""Your computer has {cpu_n} Logical Processors!
Take in mind that this software divides your file by the number of logical processors to divide the task in to each one!
Meaning that the more logical processors, the faster the search is going to be""")
    l = int(gui.prompt("In which column are the e-mails?")) - 1  # type: ignore
    
    if doc == True:
        number_lines = int(sum(1 for row in (open(filename))))
        rowsize = int(round(number_lines / cpu_n))
        names_list = []
        for i in range(1,number_lines, rowsize):
            df = pd.read_csv(filename,
                sep=';',
                usecols=[l],
                header = 0,
                nrows = rowsize,
                skiprows = i)
            df.set_axis(["email"],axis=1, inplace=True) # type: ignore
            df.head()
            out_csv= 'email' + str(i) + '.csv'
            names_list.append(out_csv)
            df.to_csv(out_csv,  # type: ignore
                index=False,
                header=None,  # type: ignore
                mode='a',#append data to csv file
                chunksize=rowsize,)#size of data to append for each loop 

    elif doc == False:
        #turns excel to csv for easy access
        read_file = pd.read_excel(filename)
        read_file.to_csv ("excel_trol.csv", 
                        index = None,
                        header=True)
        number_lines = int(sum(1 for row in (open("excel_trol.csv"))))
        rowsize = int(round(number_lines / cpu_n))
        names_list = []
        for i in range(1,number_lines, rowsize):
            df = pd.read_csv("excel_trol.csv",
                sep=',',
                usecols=[l],
                header = 0,
                nrows = rowsize,
                skiprows = i)
            df.set_axis(["email"],axis=1, inplace=True) # type: ignore
            df.head()
            out_csv= 'email' + str(i) + '.csv'
            names_list.append(out_csv)
            df.to_csv(out_csv,  # type: ignore
                index=False,
                header=None,  # type: ignore
                mode='a',#append data to csv file
                chunksize=rowsize,)#size of data to append for each loop 
        if(os.path.exists("excel_trol.csv") and os.path.isfile("excel_trol.csv")):
            os.remove("excel_trol.csv")
            print("file deleted")
        else:
            print("file not found")

    incorrect_emails= []
    correct_emails= []

    start__ = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        freeze_support()
        results = executor.map(main, names_list)

    for result in results:
        for _ in result[0]:
            correct_emails.append(_)
        for __ in result[1]:
            incorrect_emails.append(__)
    finish__ = time.perf_counter()
    final_time = round(int(finish__- start__) / 60)
    messagebox.showwarning("Done", " The search is done")

    
    #page defining
    global end
    inf.destroy()
    end = Toplevel()
    end.title("Return")
    end.geometry("600x350")
    icon_result= resource_path("icons/result_icon.ico")
    end.iconbitmap(icon_result)

    valueinfo = Label(end, text="Yay! your query is done!", padx=3, pady=2, anchor=N, font=("Times New Roman", 25))
    valueinfo.grid(column=0, row=0, columnspan = 3, ipadx=100, ipady=50)
    valueinfo = Label(end, text=f"Your email file has {number_lines} emails, and took {final_time} minutes to check", padx=3, pady=2, anchor=W)
    valueinfo.grid(column=0, row=1, columnspan = 3)

    vldinfo = Label(end, text=f"From {number_lines}, there were {len(correct_emails)} valid emails", padx=3, pady=2, anchor=W)
    vldinfo.grid(column=0, row=2)
    invldinfo = Label(end, text=f"From {number_lines}, there were {len(incorrect_emails)} invalid emails", padx=3, pady=2, anchor=W)
    invldinfo.grid(column=1, row=2)

    open_btn = Button(end, text="get valid email csv", bg='green', command=lambda:correct_csv(correct_emails), padx=3, pady=2, anchor= S)
    open_btn.grid(column = 0, row = 3, pady=5, sticky=N)
    open_btn = Button(end, text="get invalid email csv", bg='red', command=lambda:incorrect_csv(incorrect_emails), padx=3, pady=2, anchor= S)
    open_btn.grid(column = 1, row = 3, pady=5, sticky=N)

    SAVEinfo = Label(end, text="", padx=3, pady=2, anchor=CENTER)
    SAVEinfo.grid(column=0, row=4, columnspan=2)
    
def validate_one():#this has the search one page
    global val, result_label, search_entry
    val = Toplevel()
    val.title("Information")
    val.geometry("450x90")
    val.minsize(450, 90)
    val.maxsize(450, 90)
    val_one = resource_path("icons/one_selec.ico")
    val.iconbitmap(val_one)

    search_label = Label(val, text="Search email: ")
    search_label.grid(row=0, column=0, pady=5)
    search_entry = Entry(val)
    search_entry.grid(row=0, column=1, ipadx=50)
    result_btn = Button(val, text="Search", command= search_one, anchor= CENTER)
    result_btn.grid(row=0, column=2, padx= 5)

    result_label = Label(val, text="Result:")
    result_label.grid(row=1, column=0)

def search_one():
    email = search_entry.get()
    isexist= validate_email(email, smtp_timeout=1.5, dns_timeout=5)
    if isexist == True:
        result_label.config(text="Result: True")
    elif isexist == None:
        result_label.config(text="Result: False")
    elif isexist == False:
        result_label.config(text="Result: False")

    elif isexist == 'True':
        result_label.config(text="Result: True")
    elif isexist == 'None':
        result_label.config(text="Result: False")
    elif isexist == 'False':
        result_label.config(text="Result: False")

    else:
        result_label.config(text="Result: False")

root = Tk()
root.title("Email validator V1")
root.geometry("550x375")
root.minsize(550, 375)
root.maxsize(550, 375)
icon_mail_box= resource_path("icons/mail_box.ico")
root.iconbitmap(icon_mail_box)

#Style 
style = ttk.Style()
style.theme_use('default')

main_title = Label(root, text="Email validator 2022", padx=3, pady=2, anchor=CENTER, font=("Times New Roman", 25))
main_title.grid(column=0, row=0, columnspan = 3, ipadx=100, ipady=50)

open_btn = Button(root, text="Choose you file", command=choose_file, anchor= CENTER)
open_btn.grid(column=0, row=1, columnspan=3, ipadx=10)

one_btn = Button(root, text="Validate one", command=validate_one, anchor= CENTER)
one_btn.grid(column=0, row=2, columnspan=3, ipadx=10, pady=10)
 
open_btn = Button(root, text="Informations", command=information, anchor=CENTER)
open_btn.grid(column=2, row=3, sticky=E, pady=70, padx=50)

credit = Label(root, text="Made by Superjoa10 (Click to access my github)", padx=3, pady=2, anchor=CENTER, font=("Times New Roman", 7),fg="blue", cursor="hand2")
credit.grid(column=0, row=3)
credit.bind("<Button-1>", lambda e: callback("https://github.com/Superjoa10"))

mainloop()
input()