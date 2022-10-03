'''
    This program bulit GUI of module tracker application. also responsible
    to the perfom diiferent task of this applications with required validations
'''
import os
import requests
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk
from module_cgecker import ModuleFinder
from tkinter import messagebox


class GuiData:
    '''This class is used to display GUI of windows applicatios'''

    def show_list(self):
        '''This function display installed modules of python'''
        os.system("cmd /c pip list >./catch/version.txt")
        with open("./catch/version.txt", 'r') as file_obj:
            data = file_obj.readlines()
        data = data[2:]
        self.text.delete(0, END)
        self.b3.config(state="disabled")
        self.b4.config(state="disabled")
        self.b5.config(state="disabled")
        header = ["Module Name", "Current-Version"]
        self.text.insert(END, self.getPrettyString(header, 40))
        self.text.insert(END, "-"*53)
        for items in data:
            items = items.split(" ")
            items = items[:-1]
            items = list(filter(None, items))

            if len(items) > 1:
                self.text.insert(END, self.getPrettyString(items, 40))

    def check_for_update(self):
        '''This function check updates of new version of installed module'''
        os.system("cmd /c pip list -o >./catch/new_version.txt")
        with open("./catch/new_version.txt", 'r') as file_obj:
            data = file_obj.readlines()
        data = data[2:]
        self.text.delete(0, END)
        self.d = []
        header = ["Name", "Current-Version", "Latest-Version"]
        self.text.insert(END, self.getPrettyString(header, 15))
        self.text.insert(END, "-"*83)
        for items in data:
            items = items.split(" ")
            items = items[:-1]
            items = list(filter(None, items))
            self.d.append(items[0])
            if len(items) > 2:
                self.text.insert(END, self.getPrettyString(items, 20))
        self.b3.config(state="normal")
        self.b4.config(state="normal")
        self.b5.config(state="normal")

    def update(self):
        '''This function update selecetd module with latest version'''
        selected = self.text.curselection()
        update_item = self.text.get(selected[0])
        update_item = update_item.split(" ")

        success = os.system(
            f"cmd /c python -m pip install --upgrade pip {update_item[0]}")
        if success == 0:
            self.popupmsg(f"Module {update_item[0]} updated successfully")
            self.text.delete(selected[0])
            self.d.remove(update_item[0])

    def update_all(self):
        print(self.d)
        '''This function update all modules with latest version'''
        error = []
        for i in self.d:
            success = os.system(
                f"cmd /c python -m pip install --upgrade pip {i}")
            if success == 1:
                error.append(i)

        if len(error) == 0:
            self.text.delete(2, END)
            self.d = []
            self.popupmsg("All Modules are updated successfully")

        else:
            list_of_not_installed = ""
            for i in error:
                list_of_not_installed = list_of_not_installed + i + ",  "
            self.popupmsg(
                f"Error in updation of this modules :  \n  { list_of_not_installed }")

    def show_vulnerability(self):
        '''This function find vulnerability in module'''
        text = ""
        for module in self.d:
            r = requests.get("http://127.0.0.1:5000/" + module)
            text = text + r.text + "  \n"
        if text == "":
            text = "No Python module found "
        self.popupmsg(text)

    def popupmsg(self, msg):
        '''This function display popup message'''
        self.popup = tk.Tk()
        self.popup.wm_title("!")
        self.label = ttk.Label(self.popup, text=msg)
        self.label.pack(side="top", fill="x", pady=10)
        self.B6 = ttk.Button(self.popup, text="Okay",
                             command=self.popup.destroy)
        self.B6.pack()

    def popupinput(self):
        '''This function takes input from user in popup box'''
        self.popup_in = tk.Tk()
        self.popup_in.wm_title("!")
        self.l = Label(self.popup_in, text='Enter name project path')
        self.l.grid(row=1, column=1, pady=30, sticky='E')
        self.e = Entry(self.popup_in)
        self.e.grid(row=1, column=2)
        self.b = Button(self.popup_in, text='Submit', command=self.ans)
        self.b.grid(row=2, column=1, pady=20)

    def ans(self):
        '''This function stores output of popup windows and find vulnerability'''
        self.project_path = self.e.get()
        self.popup_in.destroy()
        MODULE_OBJ = ModuleFinder()
        self.d = MODULE_OBJ.find_modules(self.project_path)
        self.show_vulnerability()
        self.d = []

    def getPrettyString(self, record, space):
        '''This function dispaly list in formated manner'''
        string = ""
        for i in range(len(record)):
            if i == 0:
                string += '{:<45}'.format(record[i])
            elif i == 1:
                string += '{:<45}'.format(record[i])
            elif i == 2:
                string += '{:<45}'.format(record[i])
        return string

    def check_project(self):
        '''This function checks project vulnerability'''
        self.text.delete(0, END)
        self.text.insert(END, " Welcome to module manager...")
        self.d = []
        self.popupinput()
        self.b3.config(state="disabled")
        self.b4.config(state="disabled")
        self.b5.config(state="disabled")

    def __init__(self):
        '''This function is make GUI of application'''
        self.root = Tk()
        self.d = []
        self.root.title("Module Tracker")
        self.text = Listbox(self.root, width=100, height=42, cursor="hand2")
        self.image_url = r".\images"
        self.text.insert(END, " Welcome to module manager...")
        self.text.grid(column=0, rowspan=10, columnspan=2)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "list.png"))
        self.photoimage1 = self.photo.subsample(4, 4)
        self.b1 = Button(self.root, text="   Show List", command=self.show_list, image=self.photoimage1,
                         compound="left", cursor="hand2", width=200, height=66, anchor="w", pady=20)
        self.b1.grid(column=2, row=0)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "dl.png"))
        self.photoimage2 = self.photo.subsample(4, 4)
        self.b2 = Button(self.root,  text="   Check for Updates", command=self.check_for_update, image=self.photoimage2,
                         compound="left", cursor="hand2", width=200, height=66, anchor="w", pady=20)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "update.png"))
        self.photoimage3 = self.photo.subsample(4, 4)
        self.b3 = Button(self.root,  text="    Update", command=self.update, compound="left", image=self.photoimage3,
                         cursor="hand2", width=200, height=66, anchor="w", pady=20)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "update_all.png"))
        self.photoimage4 = self.photo.subsample(4, 4)
        self.b4 = Button(self.root,  text="   Update all", command=self.update_all,  compound="left", image=self.photoimage4,
                         cursor="hand2", width=200, height=66, anchor="w", pady=20)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "vulnerabilities.png"))
        self.photoimage5 = self.photo.subsample(16, 16)
        self.b5 = Button(self.root,  text="   Show Vulnerability", command=self.show_vulnerability,  compound="left", image=self.photoimage5,
                         cursor="hand2", width=200, height=66, anchor="w", pady=20)
        self.photo = PhotoImage(
            file=os.path.join(self.image_url, "download.png"))
        self.photoimage7 = self.photo.subsample(4, 4)
        self.b7 = Button(self.root,  text="    Scan Project", command=self.check_project,  compound="left", image=self.photoimage7,
                         cursor="hand2", width=200, height=66, anchor="w", pady=20)

        self.b2.grid(column=2, row=1)
        self.b3.grid(column=2, row=2)
        self.b4.grid(column=2, row=3)
        self.b5.grid(column=2, row=4)
        self.b7.grid(column=2, row=5)
        self.b3.config(state="disabled")
        self.b4.config(state="disabled")
        self.b5.config(state="disabled")


guidata = GuiData()
guidata.root.mainloop()
