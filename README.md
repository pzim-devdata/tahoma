# tahoma
[UP TO DATE] This is a very easy API for controlling Somfy Tahoma's devices written in Python3, thanks to the pyoverkiz API.
You just need a three-word input to control a device.
It was created with Tahoma but can also works with Somfy Connectivity Kit, Connexoon, Cozytouch


![Somfy](https://www.voletsdusud.com/wp-content/uploads/2018/04/logo-tahoma.jpg)



[![GitHub license](https://img.shields.io/github/license/pzim-devdata/tahoma?style=plastic)](https://github.com/pzim-devdata/tahoma/blob/main/LICENSE)    ![](https://img.shields.io/badge/Works%20with-Python%203-red?style=plastic)    ![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/tahoma?style=plastic)    [](https://github.com/pzim-devdata/tahoma/issues)    ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/tahoma?style=plastic)    [![Visits Badge](https://badges.strrl.dev/visits/pzim-devdata/tahoma)](https://badges.strrl.dev)    ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/tahoma?style=plastic)    [![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/tahoma/v2.2.0.svg?style=plastic)](https://GitHub.com/pzim-devata/tahoma/commit/)    
<!---
THIS TAG DOESN'T WORK, DON'T TRUST IT : ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/tahoma/total?style=plastic) 
-->
[![Downloads](https://static.pepy.tech/personalized-badge/tahoma?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20downloads)](https://pepy.tech/project/tahoma)

THIS IS THE PORTABLE VERSION FOR DIRECT DOWNLOADING. IT'S NOT AN INSTALLED PACKAGE. TO RUN THE APP JUST EXECUTE, IN YOUR IMPORTED FOLDER, `python3 tahoma.py`
. IF YOU WANT TO INSTALL THE PACKAGE USING PyPI (pip version) go there : [How to install tahoma with pip ?](https://github.com/pzim-devdata/tahoma#install-the-main-package-) or go directly to the [PyPI Project Website](https://pypi.org/project/tahoma/#description) It's easier.

IF YOU LIKE THIS PROGRAM, PLEASE STAR IT TO IMPROVE TAHOMA'S VISIBILITY SO THAT OTHERS CAN ALSO BENEFIT FROM IT. :star:


# Download the zip file and extract it :

[Download :inbox_tray:](https://github.com/pzim-devdata/tahoma/releases/latest/download/tahoma.zip)


# Start the app :

Run in your imported folder : 

- `python3 -m pip install -r requirements.txt` in order to install dependencies
and
- `python3 tahoma.py` for being sure that tahoma starts

# Configure :

It's very easy to configure, there are just two commands to execute once for all the first time

All is explained in `python3 tahoma.py --help` and `python3 tahoma.py --info`


1. Specify your Somfy-connect login's info and choose the Somfy server :


- `python3 tahoma.py --configure` or `python3 tahoma.py -c`


2. Configure the API and get the list of your personal Somfy's devices :


- `python3 tahoma.py --getlist` or `python3 tahoma.py -g`


3. And now, you are ready to use tahoma :


# Usage : 
`python3 tahoma.py [ACTION] [CATEGORY] [NAME]`


For instance : `tahoma open shutter kitchen` or `tahoma ouvrir volet cuisine`

You can also close a shutter or a sunscreen to a specific level. For example, to close to 25%, you can use the commands : `tahoma 25 shutter kitchen` or `tahoma 25 sunscreen kitchen`. Please note that this feature only works with IO protocols and not with RTS.

As name you can use a unic word like `bath` or the full name with `[""]` like `["bath 1st floor"]`

You can also run many commands during the same process without restarting tahoma :

For instance : `tahoma arm alarm garden open shutter ["room 6"] confort heater dining off plug office 25 sunscreen kitchen launch scene morning`

There is also a wait functionality with `wait for` or `sleep for` or `attendre pendant` :

For instance : `tahoma open shutter kitchen wait for 20 close shutter kitchen`


Exemples :

- tahoma open shutter kitchen
- tahoma 25 sunscreen Velux3 (You can close a shutter or a sunscreen to a specifique level. Here it will close to 25% )
- tahoma get sensor ["Luminance sensor garden"] (You can use the full name of the device with `["<NAME>"]` )
- tahoma get sensor door (You will receive all the informations about all the sensors with the name `door` in the house in one time)
- tahoma get sensor ["Front door"] 
- tahoma on plug office
- tahoma open shutter ["room 6"]
- tahoma arm alarm garden
- tahoma confort heater dining
- tahoma get sensor ['heater dining room']
- tahoma launch scene morning
- tahoma arm alarm garden wait for 10 open shutter room6 sleep for 7 confort heater dining off plug office 25 sunscreen kitchen launch scene morning get sensor ['heater dining room']
- tahoma comfort heater dining wait for 3 get sensor ["Heater dining room"]

# But first you need to retrieve your PERSONALS commands :


## Get a list of all possibles [ACTIONS] for each [CATEGORIES] : 


- `python3 tahoma.py --list-actions` or `tahoma -la`

or

- `python3 tahoma.py --list-actions-french` or `tahoma -laf`
 
 
 
## Get a list of availables [CATEGORIES] :


- `python3 tahoma.py --list-categories` or `tahoma -lc`

or 

- `python3 tahoma.py --list-categories-french` or `tahoma -lcf`



## Get the [NAMES] you have given to your personal devices in the Somfy's App :


- `python3 tahoma.py --list-names` or `tahoma -ln`

or

- `python3 tahoma.py --list-names-french` or `tahoma -lnf`


Enjoy !  For more info `python3 tahoma.py -h` or `python3 tahoma.py -i` 


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


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

IF YOU WANT TO INSTALL THE PACKAGE USE PyPi (pip version) :

# Install the main package :
[PyPi Project Website](https://pypi.org/project/tahoma/#description)

Install tahoma :

```python
sudo python3 -m pip install -U tahoma
```

!!! It's very important to use the `sudo` command because in this way tahoma can store your logins in a safe place



# Configure :



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
