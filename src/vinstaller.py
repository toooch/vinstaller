"""
Simple Valheim+ Installer with optional mods
Author: Tooch
Date: 14-12-2022
"""

import tkinter
from tkinter import filedialog, ttk
from tkinter import messagebox as mbx
from tkinter import *
import os
import requests
import zipfile
import sys


class BaseGUI:
    def __init__(self):
        self.URL_latest = 'https://github.com/valheimPlus/ValheimPlus/releases/latest/download/WindowsClient.zip'

        """Main stuff"""
        # Main window
        self.root = tkinter.Tk()
        self.root.title('Valheim+ Installer')
        self.root.resizable(False, False)
        self.opened = False

        # Tab Control
        self.tab_control = ttk.Notebook(self.root, width=400, height=300)

        # Main installer tab
        self.main_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.main_tab, text="Main Installer")

        # Plugins tab
        self.plugins_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.plugins_tab, text="Plugin Manager")

        # Injecting tab
        self.inject_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.inject_tab, text='Injection Options')

        """Main Installer Tab"""
        # Main frame
        self.main_frame_main = Frame(self.main_tab)
        self.main_frame_main.place(anchor="center", relx=.5, rely=.5)

        # Path frame
        self.main_frame_path = Frame(self.main_frame_main)
        self.main_frame_path.grid(row=0, column=0)

        # # Path label
        self.path_label = Label(self.main_frame_path, text='Valheim installation location', pady=5)
        self.path_label.grid(row=1, column=0)

        # # Path dialog
        self.path_name = tkinter.StringVar()
        self.path_entry = Entry(self.main_frame_path, textvariable=self.path_name,
                                width=55)
        self.path_name.set('C:/Program Files (x86)/Steam/steamapps/common/Valheim')
        self.path_entry.grid(row=2, column=0)

        self.browse_button = Button(self.main_frame_path, text="Browse",
                                    command=self.browse)
        self.browse_button.grid(row=3, column=0, pady=10)

        ttk.Separator(self.main_frame_main, orient=HORIZONTAL).grid(row=1, column=0, sticky=E + W, pady=5)

        # Downloading frame
        self.main_frame_downloading = Frame(self.main_frame_main, width=300)
        self.main_frame_downloading.grid(row=2, column=0)

        # # Downloading link
        self.download_link = StringVar()
        self.download_link_entry = Entry(self.main_frame_downloading,
                                         textvariable=self.download_link,
                                         width=55)
        self.download_link_entry.insert(0, self.URL_latest)
        self.download_link_entry.configure(state=DISABLED)
        self.download_link_entry.grid(row=0, column=0, pady=10)

        ttk.Separator(self.main_frame_main, orient=HORIZONTAL).grid(row=3, column=0, sticky=E + W, pady=5)

        # Submit frame
        self.main_frame_submit = Frame(self.main_frame_main)
        self.main_frame_submit.grid(row=4, column=0)

        # # Submit button
        self.submit_button = Button(self.main_frame_submit, text='Submit',
                                    command=self.run_installer)
        self.submit_button.grid(row=0, column=0, pady=10)

        # # Submit message
        self.submit_text = StringVar()
        self.submit_msg = Label(self.main_frame_submit, textvariable=self.submit_text)
        self.submit_msg.grid(row=1, column=0)

        """Injection Tab"""
        # Main frame
        self.main_frame_inj = Frame(self.inject_tab)
        self.main_frame_inj.place(anchor="center", relx=.5, rely=.5)

        # Info label
        self.inj_info_label = Label(self.main_frame_inj, text='Injecting this installer into your Valheim installation '
                                                              'enables the program to detect new versions whenever you '
                                                              'start the game.', wraplength=300)
        self.inj_info_label.grid(row=0, column=0)

        # Inject button
        self.inj_button = Button(self.main_frame_inj, text='Inject!',
                                 command=self.run_injector)
        self.inj_button.grid(row=1, column=0)

        # Uninstall button
        self.un_button = Button(self.main_frame_inj, text='Uninstall',
                                command=self.uninstall_updater)
        self.un_button.grid(row=2, column=0, pady=10)

        """Background of window"""
        self.tab_control.grid(row=0, column=0)
        self.tab_control.grid_propagate(False)
        self.main_frame_main.pack(padx=20, pady=20)
        self.root.mainloop()

    @staticmethod
    def text_changer(tb, text):
        tb.configure(state=tkinter.NORMAL)
        tb.insert(tkinter.END, text)
        tb.configure(state=tkinter.DISABLED)
        tb.see(END)

    def run_injector(self):
        path_ = self.path_entry.get()
        if self.check_dir(path_):
            if os.path.exists(path_ + '/valheim_Data'):
                # normal injection
                # rename valheim.exe
                os.rename(path_ + '/valheim.exe', path_ + '/valheim_game.exe')
                # rename valheim_Data
                os.rename(path_ + '/valheim_Data', path_ + '/valheim_game_Data')
                # install our injector from GitHub
                response = requests.get('https://github.com/toooch/vinstaller/releases/latest/download/updater.exe')
                with open(path_ + '/valheim.exe', 'wb') as file:
                    file.write(response.content)
            else:
                mbx.showerror('Injector', 'Your Valheim installation might be messed up. Verify your files through '
                                          'Steam and try again')

        else:
            mbx.showerror('Injector',
                          'Installation location in the Main tab does not contain a Valheim installation. ' +
                          'Specify a valid location before running the injector')

    def uninstall_updater(self):
        path_ = self.path_entry.get()
        if self.check_dir(path_):
            if os.path.exists(path_ + '/valheim_game_Data') and os.path.exists(path_ + '/valheim_game.exe'):
                # normal uninstall
                # remove our updater
                os.remove(path_ + '/valheim.exe')
                # rename game exe back
                os.rename(path_ + '/valheim_game.exe', path_ + '/valheim.exe')
                # rename data folder back
                os.rename(path_ + '/valheim_game_Data', path_ + '/valheim_Data')
            else:
                mbx.showerror('Injector', 'Your Valheim installation might be messed up. Repair your files by '
                                          'verifying them through Steam')

    def browse(self):
        path_dialog = filedialog.askdirectory()
        self.path_name.set(path_dialog)

    @staticmethod
    def check_dir(path):
        if os.path.exists(path) and os.path.exists(path + '/valheim.exe') and os.path.exists(path + '/steam_appid.txt'):
            print('Valid valheim installation folder')
            return True
        else:
            return False

    def run_installer(self):
        if self.check_dir(self.path_entry.get()):
            if self.download():
                mbx.showinfo('Success', 'File downloaded succesfully')
                self.unzip()
                os.remove(self.path_entry.get() + '/WindowsClient.zip')
                return True
        else:
            self.submit_text.set('Error')
            mbx.showerror('Incorrect path',
                          'The installation path entered does not contain a Valheim installation.')
            return False

    def download(self):
        try:
            response = requests.get(self.URL_latest)
            with open(self.path_entry.get() + '/WindowsClient.zip', 'wb') as file:
                file.write(response.content)
        except:
            return False
        return True

    def unzip(self):
        with zipfile.ZipFile(self.path_entry.get() + '/WindowsClient.zip', 'r') as zip_ref:
            zip_ref.extractall(self.path_entry.get())


base = BaseGUI()
