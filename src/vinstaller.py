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
from os import listdir, path
from os.path import isfile, join
import requests
import zipfile


class BaseGUI:
    def __init__(self):
        """Main stuff"""
        # Main window
        self.root = tkinter.Tk()
        self.root.title('Valheim+ Installer')
        # self.root.wm_iconbitmap('vplus.ico')
        self.root.resizable(False, False)
        self.opened = False

        self.URL_latest = 'https://github.com/valheimPlus/ValheimPlus/releases/latest/download/WindowsClient.zip'
        self.install_location = ''
        self.installed_plugins = None
        self.download_supported_plugins()
        self.plugins = []
        self.get_supported_plugins()

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
        self.path_name = StringVar()
        self.get_install_path()
        self.path_name.set(self.install_location)
        self.path_name.trace('w', lambda name, index, mode, sv=self.path_name: self.set_install_path())
        self.path_entry = Entry(self.main_frame_path, textvariable=self.path_name,
                                width=55)
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

        """Plugin Manager"""
        self.frame_pm_main = Frame(self.plugins_tab, width=400)
        self.frame_pm_main.grid(row=0, column=0)

        # Plugin Selector
        # Frame
        self.frame_pm_selector = Frame(self.frame_pm_main, width=180, height=380)
        self.frame_pm_selector.grid(row=0, column=0, padx=10, pady=10)
        self.frame_pm_selector.grid_propagate(False)

        # List of available plugins
        self.label_available_plugins = Label(self.frame_pm_selector, text='Available plugins:')
        self.label_available_plugins.grid(row=0, column=0)
        self.frame_available_plugins = Frame(self.frame_pm_selector)
        self.frame_available_plugins.grid(row=1, column=0)

        Label(self.frame_pm_selector, text=' ').grid(row=2, column=0)

        # List of installed plugins
        self.label_installed_plugins = Label(self.frame_pm_selector, text='Installed plugins:')
        self.label_installed_plugins.grid(row=3, column=0)
        self.btn_installed_plugins = Button(self.frame_pm_selector, text='Load installed plugins',
                                            command=self.exec_load_installed_plugins)
        self.btn_installed_plugins.grid(row=4, column=0)
        self.frame_installed_plugins = Frame(self.frame_pm_selector)
        self.frame_installed_plugins.grid(row=5, column=0, sticky=W)

        # SEPARATOR
        ttk.Separator(self.plugins_tab, orient=VERTICAL).place(relx=0.5, y=20, height=260)

        # Plugin controller
        # Frame
        self.frame_pm_controller = Frame(self.frame_pm_main, width=180, height=380)
        self.frame_pm_controller.grid(row=0, column=1, padx=10, pady=10)
        self.frame_pm_controller.grid_propagate(False)

        # Install selected
        self.b_install_selected = Button(self.frame_pm_controller, text='Install Selected',
                                         command=self.exec_install_selected)
        self.b_install_selected.grid(row=0, column=0, pady=2.5)

        # Remove selected
        self.b_remove_selected = Button(self.frame_pm_controller, text='Remove Selected',
                                        command=self.exec_remove_selected)
        self.b_remove_selected.grid(row=1, column=0, pady=2.5)

        # Update supported plugins
        self.b_update_supported = Button(self.frame_pm_controller, text='Update Supported Plugins',
                                         command=self.download_supported_plugins)
        self.b_update_supported.grid(row=2, column=0, pady=2.5)

        """Background of window"""
        self.tab_control.grid(row=0, column=0)
        self.tab_control.grid_propagate(False)
        self.main_frame_main.pack(padx=20, pady=20)
        self.exec_load_available_plugins()
        self.root.mainloop()

    def exec_remove_selected(self):
        if self.check_dir(self.install_location):
            faults = []
            for plugin in self.installed_plugins:
                plugin_path = f"{self.install_location}/BepInEx/plugins/{plugin[0]}.dll"
                if plugin[1].get() is True:
                    if path.exists(plugin_path):
                        try:
                            os.remove(plugin_path)
                        except Exception as e:
                            print(e)
                            faults.append(plugin[0])
                    else:
                        faults.append(f'{plugin[0]} (file not found)')
            if len(faults) == 0:
                mbx.showinfo('Success', 'All selected plugins have been removed.')
            else:
                nl = '\n'
                mbx.showerror('Failure', f'Some ({len(faults)}) plugins have not been removed:\n{nl.join(faults)}')
            self.exec_load_installed_plugins()
        else:
            mbx.showerror('Incorrect path',
                          'The installation path entered does not contain a Valheim installation.')

    def exec_install_selected(self):
        if self.check_dir(self.install_location):
            faults = []
            for plugin in self.plugins:
                plugin_path = f"{self.install_location}/BepInEx/plugins/{path.basename(plugin['url'])}"
                if plugin['check'].get() is True:
                    if self.download(plugin['url'], plugin_path):
                        continue
                    else:
                        faults.append(plugin['name'])
            if len(faults) == 0:
                mbx.showinfo('Success', 'All plugins have been installed.')
            else:
                nl = '\n'
                mbx.showerror('Failure', f'Some ({len(faults)}) plugins have not been installed:\n{nl.join(faults)}')
            self.exec_load_installed_plugins()
        else:
            mbx.showerror('Incorrect path',
                          'The installation path entered does not contain a Valheim installation.')

    def exec_load_installed_plugins(self):
        # Check valheim installation
        if self.check_dir(self.install_location):
            # Update our list of installed plugins
            plugins_path = f"{self.install_location}/BepInEx/plugins"
            self.installed_plugins = []
            for file in listdir(plugins_path):
                if isfile(join(plugins_path, file)):
                    self.installed_plugins.append([file.split('.')[0], BooleanVar()])

            # Sort plugins
            self.installed_plugins.sort()

            # Clear frame
            for widget in self.frame_installed_plugins.winfo_children():
                widget.destroy()

            # Put plugin names in frame
            counter = 0
            for plugin in self.installed_plugins:
                if plugin[0] == 'ValheimPlus':
                    continue
                else:
                    Checkbutton(self.frame_installed_plugins, text=plugin[0],
                                variable=plugin[1], onvalue=True, offvalue=False).grid(row=counter, column=0, sticky=W)
                    counter += 1
            self.btn_installed_plugins.grid_forget()
        else:
            mbx.showerror('Incorrect path',
                          'The installation path entered does not contain a Valheim installation.')

    def exec_load_available_plugins(self):
        # Sort plugins
        self.plugins = sorted(self.plugins, key=lambda l: l['name'])

        # Put them in frame
        counter = 0
        for plugin in self.plugins:
            Checkbutton(self.frame_available_plugins, text=plugin['name'],
                        variable=plugin['check'], onvalue=True, offvalue=False).grid(row=counter, column=0, sticky=W)
            counter += 1

    @staticmethod
    def text_changer(tb, text):
        tb.configure(state=tkinter.NORMAL)
        tb.insert(tkinter.END, text)
        tb.configure(state=tkinter.DISABLED)
        tb.see(END)

    def run_injector(self):
        path_ = self.install_location
        if self.check_dir(path_):
            if path.exists(path_ + '/valheim_Data'):
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
        path_ = self.install_location
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
    def check_dir(check_path):
        if os.path.exists(check_path) and os.path.exists(check_path + '/valheim.exe') and \
                os.path.exists(check_path + '/steam_appid.txt'):
            return True
        else:
            return False

    def run_installer(self):
        if self.check_dir(self.install_location):
            if self.download(self.URL_latest, self.install_location + '/WindowsClient.zip'):
                mbx.showinfo('Success', 'File downloaded succesfully')
                self.unzip()
                os.remove(self.install_location + '/WindowsClient.zip')
                return True
        else:
            self.submit_text.set('Error')
            mbx.showerror('Incorrect path',
                          'The installation path entered does not contain a Valheim installation.')
            return False

    @staticmethod
    def download(url, path_put):
        try:
            response = requests.get(url)
            with open(path_put, 'wb') as file:
                file.write(response.content)
        except:
            return False
        return True

    def unzip(self):
        with zipfile.ZipFile(self.install_location + '/WindowsClient.zip', 'r') as zip_ref:
            zip_ref.extractall(self.install_location)

    def get_supported_plugins(self):
        self.plugins = []
        with open('supported_plugins.vinstaller') as file:
            for line in file:
                part = line.replace('\n', '').split(',')
                if len(part) > 2:
                    self.plugins.append({'name': part[0], 'url': part[1], 'dep': part[2].split(';'),
                                         'check': BooleanVar()})
                else:
                    self.plugins.append({'name': part[0], 'url': part[1], 'dep': [],
                                         'check': BooleanVar()})

    @staticmethod
    def download_supported_plugins():
        url = 'https://raw.githubusercontent.com/toooch/vinstaller/main/src/supported_plugins.vinstaller'
        try:
            response = requests.get(url)
            with open('supported_plugins.vinstaller', 'wb') as file:
                file.write(response.content)
        except:
            pass

    def get_install_path(self):
        try:
            with open('vinstaller.cfg') as cfg:
                self.install_location = cfg.readline().replace('\n', '')
        except:
            with open('vinstaller.cfg', 'w') as cfg:
                cfg.write('C:/Program Files (x86)/Steam/steamapps/common/Valheim')
            self.install_location = 'C:/Program Files (x86)/Steam/steamapps/common/Valheim'

    def set_install_path(self):
        new_path = self.path_entry.get()
        with open('vinstaller.cfg', 'w') as cfg:
            cfg.write(new_path)
        self.install_location = new_path


base = BaseGUI()
