# tahoma
[UP TO DATE] Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. 
It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch. You can also use ChatGPT to control it and for help.


![Somfy](https://www.voletsdusud.com/wp-content/uploads/2018/04/logo-tahoma.jpg)



[![GitHub license](https://img.shields.io/github/license/pzim-devdata/tahoma?style=plastic)](https://github.com/pzim-devdata/tahoma/blob/main/LICENSE)    ![](https://img.shields.io/badge/Works%20with-Python%203-red?style=plastic)    ![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/tahoma?style=plastic)    [](https://github.com/pzim-devdata/tahoma/issues)    ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/tahoma?style=plastic)    [![Visits Badge](https://badges.strrl.dev/visits/pzim-devdata/tahoma)](https://badges.strrl.dev)    ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/tahoma?style=plastic)    [![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/tahoma/v2.2.0.svg?style=plastic)](https://GitHub.com/pzim-devata/tahoma/commit/)    ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/tahoma/total?style=plastic)
<!---
THIS TAG DOESN'T WORK, DON'T TRUST IT : ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/tahoma/total?style=plastic) 
-->
[![Downloads](https://static.pepy.tech/personalized-badge/tahoma?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20downloads)](https://pepy.tech/project/tahoma) 

<a href="https://github.com/pzim-devdata/tahoma" title="Click here to access the English version of the site"><img src="https://cdn.countryflags.com/thumbs/united-kingdom/flag-round-250.png" width="30" height="30" alt="British flag"></a> <a href="https://github.com/pzim-devdata/tahoma/blob/main/README_FR.md" title="Cliquez ici pour accéder à la version française du site"><img src="https://cdn.countryflags.com/thumbs/france/flag-round-250.png" width="30" height="30" alt="Drapeau français"></a>

# Features

![GifTahoma.gif](GifTahoma.gif)


- Control Somfy Tahoma devices with a simple API written in Python 3
- Create scripts or shortcuts to controle your house from a domestic server or your computer
- With this API, you can integrate Somfy's products with other Matter-compatible devices
- Works with Somfy Connectivity Kit, Connexoon, Cozytouch, and more
- Support various Somfy's devices: alarm, shutter, plug, heater, sensors, scenes, and more
- Compatible with Windows and Linux operating systems
- 100% functional with ChatGPT


## If you want to Test and Install tahoma with tahoma-gpt in a virtual environnement go [there](https://github.com/pzim-devdata/tahoma-gpt)

![Picture tahoma-gpt](https://github.com/pzim-devdata/tahoma/blob/main/picture_tahoma-gpt.png)

##############################################################################

# Install tahoma from this Git
**Note:** This is a portable version for direct downloading. It's not an installed package. To run the app, simply execute `python3 tahoma.py` in your imported folder. If you want to install the package using PyPI (pip version), go to : [How to install tahoma with pip ?](https://github.com/pzim-devdata/tahoma#install-the-main-package-) or directly visit the [PyPI Project Website](https://pypi.org/project/tahoma/#description) for an easier installation process.

If you like this program, please star it on GitHub to improve Tahoma's visibility so that others can also benefit from it. :star:

There is a ChatGPT functionality. See this [documentation](https://github.com/pzim-devdata/tahoma#add-chatgpt-functionalities-)

# Quick Start

#### 1. Download
Download the zip file and extract it to a choosen folder:

[Download :inbox_tray:](https://github.com/pzim-devdata/tahoma/releases/latest/download/tahoma.zip)

#### 2. Install dependencies
Run the following commands in your imported folder:

- `python3 -m pip install -r requirements.txt` in order to install dependencies
and
- `python3 tahoma.py`  to ensure that Tahoma starts.

#### 3. Configure
There are just two commands to execute once to configure Tahoma:

All the details are explained in `python3 tahoma.py --help` and `python3 tahoma.py --info`.


1. Specify your Somfy-connect login information and choose the Somfy server: :

- `python3 tahoma.py --configure` or `python3 tahoma.py -c`

2.  Retrieve the list of your personal Somfy devices: :

- `python3 tahoma.py --getlist` or `python3 tahoma.py -g`

#### 4. Retrieve your PERSONAL commands 
**USAGE:** `python3 tahoma.py [ACTION] [CATEGORY] [NAME]`

For example : `tahoma open shutter kitchen` or `tahoma ouvrir volet cuisine`

To retrieve your personal commands, you can use the following options:

1. List all possible [ACTIONS] for each [CATEGORIES]: 

- `python3 tahoma.py --list-actions` or `tahoma -la`
or
- `python3 tahoma.py --list-actions-french` or `tahoma -laf`
 
2. List available [CATEGORIES]:

- `python3 tahoma.py --list-categories` or `tahoma -lc`
or 
- `python3 tahoma.py --list-categories-french` or `tahoma -lcf`

3. Retrieve the [NAMES] you have assigned to your personal devices in the Somfy's App:

- `python3 tahoma.py --list-names` or `tahoma -ln`
or
- `python3 tahoma.py --list-names-french` or `tahoma -lnf`


Now you are ready to use tahoma

For more info  refer to `python3 tahoma.py -h` or `python3 tahoma.py -i` 



# Use Cases: 
**Usage:** `python3 tahoma.py [ACTION] [CATEGORY] [NAME]`

For example : `tahoma open shutter kitchen` or `tahoma ouvrir volet cuisine`


- You can specify the closing level for shutters or sunscreens with a numeric value as ACTION.

For instance, to close a shutter or a sunsceen to 25% : 

`tahoma 25 shutter kitchen`
`tahoma 25 sunscreen kitchen`.

Please note that this feature only works with IO protocols and not with RTS.

- You can use either a unique word : `bath` or the full name of a device in square brackets `[""]` : `["bath 1st floor"]`) as the NAME parameter.

For example :

`tahoma open shutter garden`

`tahoma arm alarm ["garden door"]`

- Multiple commands can be executed in the same process without restarting Tahoma. 

For example : 

`tahoma arm alarm garden open shutter ["room 6"] confort heater dining off plug office 25 sunscreen kitchen launch scene morning`

- There is also a wait functionality with `wait for <SECOND(S)>` or `sleep for <SECOND(S)>` or `attendre pendant <SECOND(S)>` :

For example : `tahoma open shutter kitchen wait for 20 close shutter kitchen`

- You can also wait for a specific time with `wait for <HOUR:MINUTE>` (24-hour format)

For example : `tahoma wait for 13:32 open shutten kitchen`

- Since it is impossible to stop an RTS device, there is the possibility to cancel the immediate preceding command (without affecting a 'wait for <SECONDS>' command). To do this you can use the command 'cancel last action' or 'annuler precedente commande' just after a command that opens or closes an RTS device.

For example :

`tahoma open shutter kitchen wait for 2 cancel last action` : It will stop the kitchen shutter after 2 seconds

`tahoma open shutter kitchen open shutter room6 cancel last action` : It will only stop the room6 shutter

# Examples :
Here are some example commands :

- tahoma open shutter kitchen
- tahoma 25 shutter Velux3  (Closes the shutter to 25%)
- tahoma get sensor ["Luminance sensor garden"] (You can use the full name of the device with `["<NAME>"]` )
- tahoma get sensor door (Provides information about all sensors named "door" in the house)
- tahoma get sensor ["Front door"] 
- tahoma on plug office
- tahoma open shutter ["room 6"]
- tahoma toggle plug kitchen (For IO devices only)
- tahoma arm alarm garden
- tahoma on light ["kitchen light"]
- tahoma off spotalarm spot
- tahoma comfort heater dining
- tahoma get sensor ['heater dining room']
- tahoma launch scene morning
- tahoma wait for 13:32 open shutten kitchen
- tahoma arm alarm garden wait for 10 open shutter room6 sleep for 7 confort heater dining off plug office 25 sunscreen kitchen launch scene morning get sensor ['heater dining room']
- tahoma comfort heater dining wait for 3 get sensor ["Heater dining room"]
- tahoma open shutter kitchen open shutter room6 wait for 2 cancel last action` (It will stop the room6 shutter after 2 seconds)




# Create a PATH to tahoma :

To be able to run tahoma directly in the terminal, without going to the source package, you should add the tahoma's folder to the PATH :

By doing this, instead of taping `python3 '/place/of/the/folder/tahoma/tahoma.py open shutter kitchen'`,

 you will be able to directly tape in the terminal : `tahoma open shutter kitchen`.


Then execute tahoma just like this : `tahoma arm alarm garden open shutter kitchen close shutter room6 confort heater dining off plug office 25 shutter kitchen` and that's all !


## On Linux :

On Linux, it can be permanently done by executing : `sudo gedit ~/.bashrc` and adding, at the end of the document, this line :

`export PATH=$PATH:/place/of/the/folder/tahoma`


If you want to temporarily test it before, you can just execute this command in the terminal : 

`export PATH=$PATH:/place/of/the/folder/tahoma` 

It will be restored on the next reboot.

You should also need to rename `tahoma.py` to `tahoma`

Then execute tahoma just like this : `tahoma arm alarm garden open shutter kitchen close shutter room6 confort heater dining off plug office 25 shutter kitchen` and that's all !


## On Windows :

[How to create a PATH on Windows](https://www.computerhope.com/issues/ch000549.htm)

Thanks to the ``tahoma.exe`` program, you will be able to execute tahoma just by entering this command : ``tahoma`` instead of ``python3 tahoma.py`` on Windows

Then execute tahoma just like this : `tahoma arm alarm garden open shutter kitchen close shutter room6 confort heater dining off plug office 25 shutter kitchen` and that's all !


# Add ChatGPT functionalities : 

- The best way to install tahoma-gpt with tahoma is to use [Pypi](https://pypi.org/project/tahoma-gpt/)

- If you want to use tahoma-gpt in a virtual environement follow this [link](https://github.com/pzim-devdata/tahoma-gpt) or use [pipx](https://pypi.org/project/tahoma-gpt/)

- If you want to use tahoma with chatGPT from this repo, follow this steps :


1. install tahoma by following the instructions provided in the first steps

2. Downbload `tahoma-gpt.py` and `requirements_tahoma-gpt.txt`:

3. Install requirements:

`python3 -m pip install -r requirements_tahoma-gpt.txt` in order to install dependencies

4. Open `tahoma-gpt.py` with a text editor and add your ChatGPT API key and the model you want to use inside the document

5. Run the program in a terminal or command prompt by executing the following command: :

`python3 tahoma-gpt.py`


Make sure to carefully follow these steps to successfully integrate tahoma with ChatGPT.





-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

IF YOU WANT TO INSTALL THE PACKAGE USE PyPi (pip version) :

# Install the main package :
[PyPi Project Website](https://pypi.org/project/tahoma/#description)

Install tahoma :

- For Linux users :

```python
sudo python3 -m pip install -U tahoma
```

!!! It's very important to use the `sudo` command because in this way tahoma will be in PATH

- For Windows users :

```python
python3 -m pip install -U tahoma
```
Without the `sudo` command

# Configure :

(Do not use `sudo` command for Windows users)



It's very easy to configure, there are just two commands to execute once for all the first time

All is explained in tahoma --help and tahoma --info


1. Specify your Somfy-connect login's info and choose the Somfy server (`sudo` command is required) :


- `sudo tahoma --configure` or `sudo tahoma -c`


2. Configure the API and get the list of your personal Somfy's devices (`sudo` command is also required) :


- `sudo tahoma --getlist` or `sudo tahoma -g`


3. And now, you are ready to use tahoma :


# Usage : `tahoma [ACTION] [CATEGORY] [NAME]`


For instance : `tahoma open shutter kitchen` or `tahoma ouvrir volet cuisine`

You can also close a shutter or a sunscreen to a specific level. For example, to close to 25%, you can use the commands : `tahoma 25 shutter kitchen` or `tahoma 25 sunscreen kitchen`. Please note that this feature only works with IO protocols and not with RTS.

You can also run many commands during the same process without restarting tahoma ;

For instance : `tahoma arm alarm garden open shutter kitchen close shutter room6 confort heater dining off plug office 25 sunscreen kitchen`



# But first you need to retrieve your PERSONALS commands :


## Get a list of all possibles [ACTIONS] for each [CATEGORIES] : 


- `tahoma --list-actions` or `tahoma -la`

or

- `tahoma --list-actions-french` or `tahoma -laf`
 
 
 
## Get a list of availables [CATEGORIES] :


- `tahoma --list-categories` or `tahoma -lc`

or 

- `tahoma --list-categories-french` or `tahoma -lcf`



## Get the NAMES you have given to your personal devices in the Somfy's App :


- `tahoma --list-names` or `tahoma -ln`

or

- `tahoma --list-names-french` or `tahoma -lnf`



Enjoy !  For more info `tahoma -h` or `tahoma -i` 



# Create a PATH to tahoma :


On Linux, if you have installed tahoma without the `sudo` command you will need to create a PATH for starting tahoma with the `tahoma` command.

Indead, to be able to run tahoma directly in the terminal, without going to the source package, you should add the tahoma's folder to the PATH :

It can be permanently done by executing : `sudo gedit ~/.bashrc` and adding, at the end of the document, this line :

`export PATH=$PATH:/place/of/the/folder/tahoma`



If you want to temporarily test it before, you can just execute this command in the terminal : 

`export PATH=$PATH:/place/of/the/folder/tahoma` 

It will be restored on the next reboot.



By doing this, instead of taping `python3 '/place/of/the/folder/tahoma/tahoma.py open shutter kitchen'`,

 you will be able to directly tape in the terminal : `tahoma open shutter kitchen`.


Then execute tahoma just like this : `tahoma arm alarm garden open shutter kitchen close shutter room6 confort heater dining off plug office` and that's all !




-------------------------------------------------------------------------------------

For :


Somfy Connectivity Kit
Somfy Connexoon IO
Somfy Connexoon RTS
Somfy TaHoma
Somfy TaHoma Beecon
Somfy TaHoma Switch
Thermor Cozytouch
And more...

Supported devices :
Alarm
Shutter
Plug
Heater
Sensors
Scenes
and more if you ask me on github : 

[@pzim-devdata GitHub Pages](https://github.com/pzim-devdata/tahoma/issues)












<p align="center" width="100%">
    <img width="33%" src="https://avatars.githubusercontent.com/u/52496172?v=4"> 
</p>

------------------------------------------------------------------

- [Licence](https://github.com/pzim-devdata/DATA-developer/raw/master/LICENSE)
MIT License Copyright (c) 2023 pzim-devdata

------------------------------------------------------------------

Created by @pzim-devdata - feel free to contact me!
