from os import path, getcwd, system, remove
from sys import argv, exit
from requests import get
from pefile import PE
from zipfile import ZipFile
from time import sleep


def check_dir(path_):
    if path.exists(path_) and path.exists(path_ + '/valheim.exe') and path.exists(path_ + '/steam_appid.txt'):
        print('\33[32mValid valheim installation folder\33[0m')
        return True
    else:
        return False


def unzip(install_dir):
    with ZipFile(install_dir + '/WindowsClient.zip', 'r') as zip_ref:
        zip_ref.extractall(install_dir)


def download(install_dir):
    try:
        print('Downloading file...')
        response = get('https://github.com/valheimPlus/ValheimPlus/releases/latest/download/WindowsClient.zip')
        with open(install_dir + '/WindowsClient.zip', 'wb') as file:
            file.write(response.content)

    except:
        print('\33[31mError in file downloading\33[0m')
        return False
    print('\33[32mFile downloaded\33[0m')
    return True


def run_installer(install_dir):
    if check_dir(install_dir):
        if download(install_dir):
            unzip(install_dir)
            remove('WindowsClient.zip')
            return True
        else:
            return False


def main():
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'

    print(f'{CBOLD}{CGREEN}Started Update Checker{CEND}')

    install_dir = getcwd()
    print(f'Installation Directory: {CYELLOW}{install_dir}{CEND}')

    print(f'Getting latest version from GitHub...')
    response = get('https://api.github.com/repos/valheimPlus/ValheimPlus/releases/latest')
    latest_version = response.json()['tag_name']
    print(f'Latest version: {CYELLOW}{latest_version}{CEND}')

    print(f'Getting installed version from files...')
    if path.exists(getcwd() + '/BepInEx/plugins/ValheimPlus.dll'):
        pe = PE(r'BepInEx/plugins/ValheimPlus.dll')
        info = pe.dump_info()
        location = info.find('ProductVersion: ')
        installed_version = info[location + 16:location + 25].strip()
        print(f'Installed version: {CYELLOW}{installed_version}{CEND}')
    else:
        print(f'{CRED}No ValheimPlus.dll found. Installing latest release anyway{CEND}')
        installed_version = '0.0.0.0'

    if latest_version == installed_version:
        print(f'{CGREEN}Version match{CEND}')

        def starter():
            print(f'{CYELLOW}Starting game...{CEND}')
            if '-console' in argv:
                system('start valheim_game.exe -console')
            else:
                system('start valheim_game.exe')

        starter()
        exit()
    else:
        print(f'{CRED}Version mismatch{CEND}')
        print(f'Attempting to install latest version...')
        if run_installer(install_dir):
            def starter():
                print(f'{CYELLOW}Starting game...{CEND}')
                if '-console' in argv:
                    system('start valheim_game.exe -console')
                else:
                    system('start valheim_game.exe')

            starter()
            exit()


main()
