# vinstaller

vinstaller makes it super easy to keep your Valheim+ up-to-date!
Installing the latest version is possible from the main program, however automatic updating can be enabled by injecting the auto-updater into your Valheim installation.

## How to use
Download vinstaller.exe from the latest release or by clicking [here](https://github.com/toooch/vinstaller/releases/latest/download/updater.exe), or build it yourself

In the upper part of the main screen, specify the path of you Valheim installation. If there is no Valheim instance found in this directory, the program will display an error message.
In the lower part, the download link to the latest Valheim+ release is displayed. This cannot be altered.
The submit button will start the installation of the latest Valheim+ release.

![The Main Installer page](https://media.discordapp.net/attachments/629610955906744349/1055207142963023892/image.png)

In the Injection Options screen, you can inject the auto-updater into your Valheim installation. This still needs you to specify the path in the main screen. The updater will run every time you start the game and install the latest update if it is not installed yet.

![The Injection Options page](https://media.discordapp.net/attachments/629610955906744349/1055210493482119228/image.png)

## State of the program
- [x] Manual installation of the latest version
- [x] Standalone auto-updater
- [x] Injection of the auto-updater
- [ ] Multiple version select
- [ ] Additional plugin manager

## How to build
In case you're unsure regarding the security of the programs, you can build them yourself.
For the main vinstaller.exe:
1. Download [vinstaller.py](src/vinstaller.py) and [updater.py](src/updater.py)
2. Pack both Python files using [pyinstaller](https://pypi.org/project/pyinstaller/)
3. Upload the exe formed from updater.py to a web location accesible to be downloaded from using [requests](https://pypi.org/project/pyinstaller/)
Note: you might need to install some dependencies on your machine in order to package the files.

## Contact
[Tooch#4004](https://discordapp.com/users/424576199038337034/) on Discord
