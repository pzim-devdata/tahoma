# tahoma
[UP TO DATE] This is a very easy API for controlling Somfy Tahoma's devices written in Python3, thanks to the pyoverkiz API.
You just need a three-word input to control a device.
It was created with Tahoma but can also works with Somfy Connectivity Kit, Connexoon, Cozytouch


![Somfy](https://www.voletsdusud.com/wp-content/uploads/2018/04/logo-tahoma.jpg)





# Install the main package :


Install tahoma :

```python
sudo python3 -m pip install -U tahoma
```

!!! It's very important to use the `sudo` command because in this way tahoma can store your logins in a safe place



# Configure :



It's very easy to configure, there are just two commands to execute once for all the first time

All is explained in tahoma --help and tahoma --info


1. Specify your Somfy-connect login's info and choose the Somfy server (`sudo` command is required) :


- `sudo tahoma --config` or `sudo tahoma -c`


2. Configure the API and get the list of your personal Somfy's devices (`sudo` command is also required) :


- `sudo tahoma --getlist` or `sudo tahoma -g`


3. And now, you are ready to use tahoma :


# Usage : `tahoma [ACTION] [CATEGORY] [NAME]`


For instance : `tahoma open shutter kitchen` or `tahoma  ouvrir volet cuisine`

You can also run many commands during the same process without restarting tahoma ;

For instance : `tahoma arm alarm garden open shuter kitchen close shuter room6 confort heater dining off plug office`


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


If you have installed tahoma without the `sudo` command you will need to create a PATH for starting tahoma with the `tahoma` command.

Indead, to be able to run tahoma directly in the terminal, without going to the source package, you should add the tahoma's folder to the PATH :

On Linux, it can be permanently done by executing : `sudo gedit ~/.bashrc` and adding, at the end of the document, this line :

`export PATH=$PATH:/place/of/the/folder/tahoma`



If you want to temporarily test it before, you can just execute this command in the terminal : 

`export PATH=$PATH:/place/of/the/folder/tahoma` 

It will be restored on the next reboot.



By doing this, instead of taping `python3 '/place/of/the/folder/tahoma/tahoma.py open shuter kitchen'`,

 you will be able to directly tape in the terminal : `tahoma open shuter kitchen`.


Then execute tahoma just like this : `tahoma arm alarm garden open shuter kitchen close shuter room6 confort heater dining off plug office` and that's all !






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
