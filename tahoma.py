#!/usr/bin/python3
#python3 -m pip install pyoverkiz -U
#python3 -m pip install tahoma -U
#tahoma.py by @pzim-devdata
#MIT Licence
#Info about local API: https://github.com/Somfy-Developer/Somfy-TaHoma-Developer-Mode
#https://somfy-developer.github.io/Somfy-TaHoma-Developer-Mode/
#https://dev.duboc.pro/overkiz

"""
This is the main module
"""

import asyncio
import aiohttp
import sys
import argparse
import os
import re
from getpass import getpass
import time
import datetime
from pyoverkiz.const import SUPPORTED_SERVERS, OverkizServer
from pyoverkiz.client import OverkizClient, Command
from pyoverkiz.enums import OverkizCommand
from pyoverkiz.models import Command
from pyoverkiz.models import Scenario
from pyoverkiz.exceptions import NotAuthenticatedException
from aiohttp.client_exceptions import ClientConnectorError
import requests
import base64
from hashlib import sha256

try:
    import __version__
    if __version__:
        get_devices_url = "import get_devices_url"
        version = 'tahoma - portable Version '+ str(__version__.__version__)+' - by @pzim-devdata'
except ImportError:
    from tahoma import __version__
    if __version__:
        get_devices_url = "from tahoma import get_devices_url"
        version = 'tahoma - Pypi version '+ str(__version__.__version__)+' - by @pzim-devdata'

version_number=str(__version__.__version__)

url_releases = 'https://api.github.com/repos/pzim-devdata/tahoma/releases'

last_update = os.path.dirname(os.path.abspath(__file__))+'/temp/last_update.txt'
show_available_update = os.path.dirname(os.path.abspath(__file__))+'/temp/show_available_update.txt'


def check_last_release(show='y',show_forced='y'):
    try :
        f = open(show_available_update, 'r')
        show_available_update_str = f.read()
        f.close()
    except FileNotFoundError:
        show_available_update_str = 'y'
    if show_available_update_str == 'y' or show_forced == 'y':
        try:
            with open(last_update, "r") as f:
                last_update_str = datetime.datetime.strptime(f.read(), "%Y-%m-%d")
                f.close()
        except FileNotFoundError:
            last_update_str = datetime.datetime(2000, 1, 1)
        today = datetime.datetime.now().date()
        if last_update_str.date() < today or show_forced == 'y':
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(url_releases, headers=headers)
                releases = response.json()
                last_release = releases[0]['tag_name']
                info_release = releases[0]["body"]
                if str(last_release.lower()) == str(version_number).lower():
                    if show == 'y' :
                        print("    You are using the last version of Tahoma : " + str(last_release.lower()))
                else :
                    print(" Last version of Tahoma is : " + str(last_release.lower()) + " and you are using the version : " + str(version_number).lower())
                    print(" Here is an explanation of this update:")
                    print( info_release)
                    print( "")
                    print(" Pypi version : python3 -m pip install -U tahoma or pipx upgrade tahoma")
                    print(" Github version : https://github.com/pzim-devdata/tahoma/releases/latest/download/tahoma.zip")
                    print(" If you like tahoma, please give me a star on Github: https://github.com/pzim-devdata/tahoma. Thanks!")
            except : pass
        with open(last_update, "w") as f:
            f.write(today.strftime("%Y-%m-%d"))
            f.close()

check_last_release('n','n')

def countdown(duration):
    for i in range(duration-1, 0, -1):
        sys.stdout.write("\033[2K\r")  # Efface toute la ligne
        sys.stdout.write(str(i) + "\r")  
        sys.stdout.flush()
        time.sleep(1)
#    print("Sucess!")
#    sys.stdout.write("\rFin!\n")

def main():
    icon_app = os.path.dirname(os.path.abspath(__file__))+'/icons/connected_house.png'
    icon_chauffe_eau=os.path.dirname(os.path.abspath(__file__))+'/icons/water heater.png'

    passwd_file = os.path.dirname(os.path.abspath(__file__))+'/temp/identifier_file.txt'

    list_of_tahoma_devices = os.path.dirname(os.path.abspath(__file__))+'/temp/list_of_tahoma_devices.txt'
    list_of_tahoma_shutters = os.path.dirname(os.path.abspath(__file__))+'/temp/shutters.txt'
    list_of_tahoma_heaters = os.path.dirname(os.path.abspath(__file__))+'/temp/heaters.txt'
    list_of_tahoma_alarms = os.path.dirname(os.path.abspath(__file__))+'/temp/alarms.txt'
    list_of_tahoma_spotalarms = os.path.dirname(os.path.abspath(__file__))+'/temp/spotalarms.txt'
    list_of_tahoma_plugs = os.path.dirname(os.path.abspath(__file__))+'/temp/plugs.txt'
    list_of_tahoma_sunscreens = os.path.dirname(os.path.abspath(__file__))+'/temp/sunscreens.txt'
    list_of_tahoma_scenes = os.path.dirname(os.path.abspath(__file__))+'/temp/scenarios.txt'
    list_of_tahoma_sensors = os.path.dirname(os.path.abspath(__file__))+'/temp/sensors.txt'
    list_of_tahoma_states = os.path.dirname(os.path.abspath(__file__))+'/temp/states.txt'
    list_of_tahoma_lights = os.path.dirname(os.path.abspath(__file__))+'/temp/lights.txt'

    token_file = os.path.dirname(os.path.abspath(__file__))+'/temp/token.txt'
    gateway_id_file = os.path.dirname(os.path.abspath(__file__))+'/temp/gateway_id.txt'
    local_remote_file = os.path.dirname(os.path.abspath(__file__))+'/temp/local_remote.txt'

    notification_consent = os.path.dirname(os.path.abspath(__file__))+'/temp/consent_notification.txt'

    server_choosen =  os.path.dirname(os.path.abspath(__file__))+'/temp/server_choosen.txt'

    init_file = os.path.dirname(os.path.abspath(__file__))+'/__init__.py'

    logs_consent = os.path.dirname(os.path.abspath(__file__))+'/temp/consent_logs.txt'
    log_place = os.path.dirname(os.path.abspath(__file__))+'/temp/last_commands_send.log'
    #delete log_place if size > 10000 octets
    try:
        size_log = os.path.getsize(log_place)
        if size_log > 10000:
            os.remove(log_place)
            print(f"The old log file : {log_place} has been removed because of it size > 10000 octets\nA new file will be created.\n")
    except FileNotFoundError:
        pass

    list_categories = ['shutter','spotalarm','plug','light','alarm','heater','sunscreen','scene','sensor']
    list_categories_french = ['volet','spotalarme','prise','lumiere','alarme','chauffage','rideau','scenario','capteur']
    list_actions = ['[open,close,stop,my,NUMBER]','[on,off,toggle]','[on,off,toggle]','[on,off,toggle]','[arm,disarm,partial,arm_night,arm_away]','[comfort,comfort-1,comfort-2,eco,frostprotection,off,standby,manual,auto,prog,NUMBER]','[open,close,stop,my,NUMBER]','[on,activate,launch,execute]','[get,get_state,get_position,get_lumens,get_temperature]']
    list_actions_french = ['[ouvrir,fermer,stop,my,NOMBRE]','[allumer,eteindre,basculer]','[allumer,eteindre,basculer]','[allumer,eteindre,basculer]','[activer,desactiver,partiel,activer_nuit,activer_parti]','[confort,confort-1,confort-2,eco,horsgel,eteindre,veille,manuel,auto,prog,NOMBRE]','[ouvrir,fermer,stop,my,NOMBRE]','[lancer,activer,executer]','[obtenir,etat,position,luminosite,temperature]']

    try :
        f = open(token_file, 'r')
        token = f.read()
        f.close()
    except FileNotFoundError:
        token = ""

    try :
        f = open(gateway_id_file, 'r')
        gateway_id = f.read()
        f.close()
    except FileNotFoundError:
        gateway_id = ""

    try :
        f = open(local_remote_file, 'r')
        local_remote = f.read()
        f.close()
    except FileNotFoundError:
        local_remote = "remote"

    try :
        f = open(notification_consent, 'r')
        notification = f.read()
        f.close()
    except FileNotFoundError:
        notification = 'n'

    try:
        f = open(init_file, 'r')
        init = f.read()
        f.close()
        init_str=sha256(b"init").hexdigest()
    except:
        init_str="None"

    try :
        f = open(server_choosen, 'r')
        serverchoice = f.read()
        f.close()
    except FileNotFoundError:
        serverchoice = "somfy_europe"

    try :
        f = open(logs_consent, 'r')
        logs = f.read()
        f.close()
    except FileNotFoundError:
        logs = 'N'

    def info():
        print( "" )
        print( "      ***************************************************************      " )
        print( "      Tahoma version : "+version+"     " )
        print( "      ***************************************************************        " )
        print( "                   python3 -m pip install tahoma -U" )
        print( "                   https://pypi.org/project/tahoma/" )
        print( "                 https://github.com/pzim-devdata/tahoma" )
        print( "                          contact@pzim.fr" )
        print( "" )
        print( " USAGE : tahoma [ACTION] [CATEGORY] [NAME]" )
        print( " You must provide at least 3 arguments" )
        print( " For example :  tahoma open shutter kitchen")
        print( "" )
        print( " - List of possible ACTIONS : \n "+str(list_actions) )
        print( " - Liste des ACTIONS possibles : \n "+str(list_actions_french) )
        print( "" )
        print( " - List of possible CATEGORIES : \n "+str(list_categories) )
        print( " - Liste des CATEGORIES possibles : \n "+str(list_categories_french) )
        print( "" )
        print( ' - List of available NAMES : tahoma --list-names \n - Liste des NOMS possibles : tahoma --list-names-french \n   You must provide a part of the name you have assigned to the device in the Tahoma App. \n   The <NAME> must be a single and unique word, not taken by another device of the same category !\n   For example if you have two devices called <Alarm 1> and <Alarm 2> you will need to choose <2> as device <NAME> for <Alarm 2> and not <Alarm>).\n   You can also use the full NAME with <[""]>.\n   For example: tahoma arm alarm ["Alarm 2"]')
        print( "" )
        print( "\n You can close a shutter or a sunscreen to a specific level (IO protocols only)")
        print( " For example: tahoma 25 shutter kitchen. It will open the shutter to 75% or close it to 25%" )
        print( "" )
        print( " You can also provide, as many as you wish, orders on the same line." ) 
        print( " Tahoma will execute all orders one by one in the same process ;-)" )
        print( " For example: tahoma open shutter kitchen arm alarm garden on plug room wait train garestation " )
        print( "" )
        print( " There is a wait function: 'wait for <SECOND(S)>' or 'sleep for <SECONDE(S)>'")
        print( " Tahoma will wait the time in seconds you have specified")
        print( " For example: tahoma open shutter kitchen wait for 20 on plug room")
        print( "" )
        print( " You can also wait for a specific time with 'wait for <HOUR:MINUTE>' (24-hour format)")
        print( " For example: tahoma wait for 13:32 open shutten kitchen")
        print( "" )
        print( " The STOP action for shutters and sunscreens doesn't work with RTS protocols. " ) 
        print( " Instead you can cancel the immediate preceding command (without affecting a 'wait for <SECONDS>' command)." )
        print( " To do this you can use the command 'cancel last action' just after a command that opens or closes an RTS device." )
        print( " For example: 'tahoma open shutter kitchen wait for 2 cancel last action' : It will stop the kitchen shutter after 2 seconds" )
        print( "" )
        print( " ********************************************************************" )
        print( " FIRST you must configure login and password : 'tahoma -c' " )
        print( " It will be stored there : \n "+passwd_file )
        print( "" )
        print( " THEN you must download the list of all yours devices : 'tahoma -g' " )
        print( " It will be stored there : \n "+list_of_tahoma_devices )
        print( " ********************************************************************" )
        print( "")
        print( " ********************************************************************" )
        print( "                     To get help : tahoma -h " )
        print( "")
        print( "                   To show this sceen : tahoma -i" )
        print( "" )
        print( "      Il existe une aide en français : tahoma --help-french " )
        print( " ********************************************************************        " )
        print( "" )
        check_last_release()
        print( "" )
        print( "    Open your terminal in full screen mode to have a better view \n" )
    #    try :
    #        os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
    #        print( " \n          <--- Appuyez sur F11 to close fullscreen --->\n")
    #        print( " \n             <--- Press F11 to close fullscreen --->\n")
    #    except Exception :
    #       print( "       Open your terminal in full screen to have a better view ")
        exit()

    str_info = "You must provide at least three arguments\n\nFor example : tahoma  open shutter kitchen \n\nRun <b>tahoma --help</b> for help"

    ##########################ARGUMENTS

    for arg in sys.argv :
            if arg == '-v' or arg == '--version' :
                try :
                    print(version)
                    exit()
                except IndexError: 
                    info()
                    exit()

    for arg in sys.argv :
        if arg == '-g' or arg == '--getlist' :
            try :
                exec(get_devices_url)
                exit()
            except Exception as e: 
                print(e)
#                exec((open(os.path.dirname(os.path.abspath(__file__))+"/get_devices_url.py")).read())
                exit()

    for arg in sys.argv :
        if arg == '-l' or arg == '--list' :
            try:
                print((list_of_tahoma_devices))
                if os.path.isfile(list_of_tahoma_devices) :
                    f = open(list_of_tahoma_devices, 'r')
                    print(f.read())
                    f.close()
                    exit ()
                else : 
                    print("You didn't downloaded the list of Tahoma's devices yet.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                    exit()
            except NameError as e:
                print(e) 
                print("You didn't downloaded the list of Tahoma's devices yet.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()

    for arg in sys.argv :
        if arg == '-i' or arg == '--info' :
            info()
            exit()

    for arg in sys.argv :
        if arg == '-c' or arg == '--configure' or arg == '--config' :
            print("Do you want to show desktop notifications? (Only for Linux users) (Y/n)")
            notification = input()
            if notification.lower() == 'y'or notification.lower() == 'yes':
                print("You will get desktop notification")
                time.sleep(2)
                f = open(notification_consent, 'w')
                f.write('Yes')
                f.close()
            else :
                print("Consent file for notifications removed. You will not get any desktop notification")
                time.sleep(2)
                try :
                    os.remove(notification_consent)
                except : pass
            print("\nWould you like to create a log file to store the last executed commands? (Y/n)")
            notification = input()
            if notification.lower() == 'y'or notification.lower() == 'yes':
                f = open(logs_consent, 'w')
                f.write('Y')
                print("Logs file will be created there :\n"+log_place)
                time.sleep(2)
                f.close()
            else :
                print("No file will be created for keeping logs")
                time.sleep(2)
                try :
                    os.remove(logs_consent)
                except : pass
            print("\nPaste which server you want to use : somfy_europe , somfy_america, somfy_oceania or atlantic_cozytouch:")
            serverchoice = input()
            if serverchoice == "somfy_europe" or serverchoice == "somfy_america" or serverchoice == "somfy_oceania" or serverchoice == "atlantic_cozytouch" :
                print( "You have selected: "+serverchoice )
                time.sleep(3)
                f = open(server_choosen, 'w')
                f.write(serverchoice)
                f.close()
            else :
                print( "The server you provided in not in the list ! \nAre you certain about using this server: '"+serverchoice+"' ? (Y/n)" )
                notification = input()
                if notification.lower() == 'y'or notification.lower() == 'yes':
                    f = open(server_choosen, 'w')
                    f.write(serverchoice)
                    print( "You have selected: "+serverchoice )
                    time.sleep(3)
                    f.close()
                else:
                    print( "'somfy_europe' will be used instead" )
                    time.sleep(3)
                    serverchoice = "somfy_europe"
                    f = open(server_choosen, 'w')
                    f.write(serverchoice)
                    f.close() 
            print( "\nPlease provide USERNAME for the server you have selected: \nIt will be stored here : \n"+passwd_file+"\nIf you don't want to store it localy, you can leave it empty, but you will need to connect with the --username argument each time")
            print("Username:")
            USERNAME = input()
            time.sleep(3)
            print( "\nPlease provide somfy-connect's PASSWORD for the server you have selected \nIt will be stored here : \n"+passwd_file+"\nYou can leave it empty, but you will need to connect with the --password argument each time")
            PASSWORD = getpass()
            time.sleep(3)
            print( "\nDo you want to encrypt your login in "+passwd_file+"? \nIf not, the file will be erased:\n(Y/n)")
            CONSENT = input()
            if CONSENT.lower() == 'y'or CONSENT.lower() == 'yes':
                f = open(passwd_file, 'ab')
                f.write(base64.b64encode(str(USERNAME+":"+PASSWORD+init_str).encode('utf-8')))
                f.close()
                print( "Your logins are encrypted in "+passwd_file )
                time.sleep(3)
            else :
                try :
                    os.remove(passwd_file)
                    print( "The file "+passwd_file+" has been removed" )
                    print( "To connect to tahoma, please provide logins using these arguments: tahoma --username <mail address> --password <password>" )
                except : 
                    print("The file was already removed")
                time.sleep(3)
            print("\nDo you want to check every day if an update is available? (Y/n)")
            show_available_update_str = input()
            if show_available_update_str.lower() == 'y'or show_available_update_str.lower() == 'yes':
                print( "You will be notified when a new update of tahoma is available.")
                time.sleep(2)
                f = open(show_available_update, 'w')
                f.write('y')
                f.close()
            else :
                print( "You will not be notified when a new update of tahoma is available." )
                time.sleep(2)
                f = open(show_available_update, 'w')
                f.write('n')
                f.close() 
            print("\nDo you want to configure the local API of tahoma (only for tahoma and tahoma switch)? \n(Y/n)")
            response=input()
            if response.lower() == 'y'or response.lower() == 'yes':
                print("If you want to use the local API, you will need to activate the developer mode\nGo to http://www.somfy.com > My Account.\nClick on your box > See more > Activate developer mode.")
                time.sleep(3)
                print("\nDo you want to provide the PIN number of your tahoma's gateway?\nIt's useful if you have more than one tahoma's gateway\nOtherwise you can answer 'no' \n(Y/n)")
                response2 = input()
                if response2.lower() == 'y'or response2.lower() == 'yes':
                    print("\nEnter the PIN number of the gateway you want to use.\nYou can find the PIN number on the dashboard of your http://www.somfy.com account:")
                    gateway_id = input()
                    f = open(gateway_id_file, 'w')
                    f.write(gateway_id)
                    f.close()
                    print("Your gateway ID: "+gateway_id+" has been registered in the folder:\n"+gateway_id_file)
                else:
                   print("You didn’t provide any PIN number of the gateway. \nTahoma will automatically search for a new PIN number on the next laughing of tahoma")
                time.sleep(2)
                print("\nDo you want to provide your own token for using the local API of tahoma? \nIt's useful to provide an already used token if you use the local API with Homebridge or Home Assistant for example):\n(Y/n)")
                response3 = input()
                if response3.lower() == 'y'or response3.lower() == 'yes':
                    print("Please provide your token:")
                    token = input()
                    f = open(token_file, 'w')
                    f.write(token)
                    f.close()
                    print("Your token: "+str(token)+" has been registered in the folder:\n"+token_file)
                else:
                    print("You didn’t provide an already used token. \nTahoma will automatically search for a new token on the next launching")
            else:
                print("No modification made on the configuration of the local API")
            time.sleep(2)
            print("\nDo you want to use the local API of tahoma by default?(Y/n)")
            response4 = input()
            if response4.lower() == 'y'or response4.lower() == 'yes': 
                    f = open(local_remote_file, 'w')
                    f.write('local')
                    f.close()
                    print("You will use the local API by default for supported devices only and the cloud API for the other devices.")
            else:
                print("You will use the cloud API of tahoma by default.")
                f = open(local_remote_file, 'w')
                f.write('remote')
                f.close()
            time.sleep(2)
            exit()

    for arg in sys.argv :
        if arg == '-h' or arg == '--help' :
            print("tahoma -h, --help : "+version+"\n\nUsage:\n tahoma <ACTION> <CATEGORY> <NAME> \n\n You must provide at least three arguments\n For example : tahoma open shutter kitchen or tahoma ouvrir volet cuisine\n\n You can close a shutter or a sunscreen to a specific level (IO protocols only)\n For example : tahoma 25 shutter kitchen. It will open the shutter to 75% or close it to 25%\n\n You can also provide, as many as you wish, orders on the same line\n Tahoma will execute all orders one by one in the same process ;-)\n For example : tahoma open shutter kitchen arm alarm garden on plug room wait train garestation\n\nHelp options :\n -h,   --help                      Show this help\n -hf,  --help-french               Show this help in french\n -i,   --info                      Show more info\n\nPlugin options :\n -v,   --version                   Show the version of the plugin\n -c,   --configure                 To configure the plugin and store login and password in a text file which is located here : "+passwd_file+"\n -u,   --username                  If you don't want to store the login, you can provide the mail-address with this option\n -p,   --password                  If you don't want to store the password, you can provide it with this option\n --pin                             You can provide the pin code of your gateway for a local use of the API\n --token                           You can provide a specific token for a local use of the API\n --local                           By providing this argument, you will force tahoma to run locally\n --remote                          By providing this argument, you will force tahoma to run remotely\n --token                           You can provide a specific token for a local use of the API\n --server                          You can provide the name of the server you want to use to override the default server (somfy_europe, somfy_america, somfy_oceania or atlantic_cozytouch)\n -g,   --getlist                   Download the list of devices and store them here : "+list_of_tahoma_devices+"\n -l,   --list                      Show the complet list of devices installed\n -la,  --list-actions              Show the list of possible ACTIONS by CATEGORIES\n -lc,  --list-categories           Show all supported CATEGORIES of devices\n -lnf, --list-names                Show all installed devices by there NAMES\n\nOther commands:\n wait for <seconds>\n sleep for <seconds>               Tahoma will wait for <seconds> seconds to execute next action\n wait for <HOUR:MINUTE>            Tahoma will wait for a specific hour (24h-format)\n cancel last action                Tahoma will cancel the immediate preceding command (without affecting the 'wait for' command). This is useful for stopping an RTS device\n")
            check_last_release ()
            exit()

    for arg in sys.argv :
        if arg == '-hf' or arg == '--help-french' :
            print("tahoma -h --help : "+version+"\n\nUsage:\n tahoma <ACTION> <CATEGORIE> <NOM> \n\n Vous devez fournir au moins trois arguments\n Par exemple : tahoma ouvrir volet cuisine ou tahoma open shutter kitchen\n\n Vous pouvez fermer des rideaux ou des volets à un niveau precis (Seulement pour les équipements utilisant le protocole IO)\n Par exemple : tahoma 25 volet cuisine. Les volets vont s'ouvrir de 75% ou se fermer de 25%\n\n Vous pouvez aussi spécifier autant de commandes que vous le souhaitez sur la même ligne :\n Tahoma va executer chaque commande l'une aprés l'autre durant le même processus\n Par exemple : tahoma ouvrir volet cuisine confort chauffage salon\n\nOptions de l’aide :\n -h, --help                        Affiche les options de l’aide en anglais\n\nOptions de l’application :\n -v, --version                     Affiche la version de l’application\n -i, --info                        Afficher plus d'infos sur tahoma\n -c, --configure                   Renseigner l'identifiant et le mot de passe dans un fichier texte pour ne pas devoir les renseigner à chaque fois. Le fichier texte se situe dans : "+passwd_file+"\n -u, --username                    Renseigner le nom d'utilisateur\n -p, --password                    Renseigner le mot de passe de Somfy-connect\n --pin                             Vous pouvez indiquer le code pin de votre passerelle pour un usage local de l'API\n --token                           Vous pouvez indiquer un token spécifique pour un usage local de l'API\n --local                           En fournissant cet argument, vous forcerez Tahoma à s’exécuter en local\n --remote                          En fournissant cet argument, vous forcerez Tahoma à s’exécuter à distance\n --server                          En fournissant cet argument, vous forcerez Tahoma à utiliser un serveur spécifique (somfy_europe, somfy_america, somfy_oceania or atlantic_cozytouch)\n -g, --getlist                     Télécharge la liste des équipements et la stocke dans "+list_of_tahoma_devices+"\n -l, --list                        Affiche la liste téléchargée des équipements\n -laf, --list-actions-french       Affiche la liste des ACTIONS possibles en français par CATEGORIES\n -lcf, --list-categories-french    Affiche toutes les CATEGORIES d'équipements pris en charge en français\n -lnf, --list-names-french         Affiche les NOMS des équipements installés par categories en français\n\nAutres commandes :\n attendre pendant <SECONDES>       Tahoma attendra <SECONDES> secondes avant d'éxécuter la commande suivante\n attendre heure <HEURE:MINUTE>     Tahoma attendra l'heure exacte  <HEURE:MINUTE> en format 24h avant d’exécuter la commande suivante\n annuler precedente commande       Tahoma annulera la commande précédente immédiate (sans affecter la commande 'attendre pendant'). Ceci est utile pour arrêter un périphérique RTS.")
            check_last_release ()
            exit()

    for arg in sys.argv :
        if arg == '-lc' or arg == '--list-categories' :
            print( "tahoma can control this type of devices's categories :\n"+str(list_categories))
            exit()

    for arg in sys.argv :
        if arg == '-lcf' or arg == '--list-categories-french' :
            print( "tahoma peut controler ce type de categories d'équipements :\n"+str(list_categories_french))
            exit()

    for arg in sys.argv :
        if arg == '-ln' or arg == '--list-names' :
            print("\nExecute tahoma --getlist before this command for being sure to have a complete list of installed devices")
            for category in list_categories :
                try:
                    master_list = []
                    bad_name = []
                    f = open(eval("list_of_tahoma_"+category+"s"), 'r')
                    content = f.read()
                    f.close()
                    master_list = content.split("\n")
                    master_list.remove('')
                    for i in master_list :
                        bad_name.append(i.split(",")[0])
                    print("\nHere is the list of the installed devices for the "+category.upper()+" category :\n"+str(bad_name))
                except Exception as e:
                    print("\nCan't obtain any device from the "+category.upper()+" category\nDid you downloaded the list of Tahoma's devices ?\nIf not, execute tahoma --getlist \nFor more info execute tahoma -h")
            print( '\nYou must provide a part of the NAME as argument \n The name must be a single and unique word, not taken by another device of the same category !\n For example if you have two devices called <Alarm 1> and <Alarm 2> you will need to choose <2> as device [NAME] for <Alarm 2> and not <Alarm>).\n You can also use the full NAME with [""].\n For example ["Alarm 2"]\n See tahoma --list or tahoma --help for info.')
            exit()

    for arg in sys.argv :
        if arg == '-lnf' or arg == '--list-names-french' :
            print("\nPensez à exécuter la commande : tahoma --getlist pour vous assurer que la liste des équipements est complète")
            i=-1
            for i in range(-1,len(list_categories)-1) :
                i=i+1
                try:
                    master_list = []
                    bad_name = []
                    f = open(eval("list_of_tahoma_"+list_categories[i]+"s"), 'r')
                    content = f.read()
                    f.close()
                    master_list = content.split("\n")
                    master_list.remove('')
                    for j in master_list :
                        bad_name.append(j.split(",")[0])
                    print("\nVoici la liste des équipements installés pour la catégorie "+list_categories_french[i].upper()+" :\n"+str(bad_name))
                except Exception as e:
                    print(e)
                    print("\nImpossible d'obtenir la liste des équipements pour la catégorie "+list_categories_french[i].upper()+"\nAvez-vous téléchargé la liste des équipements installés ?\nSinon executez la commande : tahoma --getlist \nPour plus d'info : tahoma --help-french")
            print( "\nVous devez fournir une partie du NOM comme argument \nCe NOM ne doit pas être utilisé par un autre équipement de la même categorie !\nSi vous avez deux équipements appelés par ex. <Alarme 1> et <Alarme 2> vous devrez renseigner comme NOM seulement <2> pour <Alarme 2> et non <Alarme> Consultez l'aide en français : tahoma --help-french ou tahoma --info pour plus d'informations.")
            exit()

    for arg in sys.argv :
        if arg == '-la' or arg == '--list-actions' :
            print( "List of actions by categories :")
            for i in range(0,len(list_actions)) :
                print ( "For the category "+list_categories[i].upper()+" : "+list_actions[i] )
            exit()

    for arg in sys.argv :
        if arg == '-laf' or arg == '--list-actions-french' :
            print( "Liste des actions par categories :")
            for i in range(0,len(list_actions_french)) :
                print ( "Pour la categorie "+list_categories_french[i].upper()+" : "+list_actions_french[i] )
            exit()

    if len( sys.argv ) < 4 :
        try:
            if notification.lower() == 'y'or notification.lower() == 'yes':
                os.system("notify-send -i "+icon_app+" --expire-time=150000 Tahoma '"+str_info+"'")
        except:pass
        info()
        exit()
    try :
        f = open(passwd_file, 'rb')
        content = f.read()
        f.close()
        content_str = base64.b64decode(content).decode('utf-8')
        if len(content_str.split(':')[0]) > 0 :
            USERNAME = content_str.split(':')[0]
        if len(content_str.split(':')[1]) > 0 :
            PASSWORD = content_str.split(':')[1].replace(init_str, "")
    except: pass

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")

    parser.add_argument("--token")
    parser.add_argument("--pin")

    parser.add_argument("--local", action='store_true')
    parser.add_argument("--remote", action='store_true')

    parser.add_argument("--server")

    parser.add_argument("action")
    parser.add_argument("category")
    parser.add_argument("name")
    parser.add_argument("suite", nargs='*')

    args = parser.parse_args()
#    print(f'Input action(s) : {args.action} {args.category} {args.name} '+' '.join(args.suite) )

    if args.password:
        PASSWORD = (f'{args.password}')
        print("Your PASSWORD has been taken into account")
    if args.username:
        USERNAME = (f'{args.username}')
        print("Your USERNAME has been taken into account")

    if args.token:
        token = (f'{args.token}')
        print("Your token: "+token+" has been taken into account")
    if args.pin:
        gateway_id = (f'{args.pin}')
        print("Your gateway pin code: "+gateway_id+" has been taken into account")

    if args.local:
        local_remote = "local"
#        print("Will use tahoma with the 'local' config")
    if args.remote:
        local_remote = "remote"
        print("Will use tahoma with the 'remote' config")

    if args.server:
        serverchoice = (f'{args.server}')
        print("The server: "+serverchoice+" has been taken into account")

    def remove_accent(old):
        new = old.lower()
        new = re.sub(r'[àáâãäå]', 'a', new)
        new = re.sub(r'[èéêë]', 'e', new)
        new = re.sub(r'[ìíîï]', 'i', new)
        new = re.sub(r'[òóôõö]', 'o', new)
        new = re.sub(r'[ùúûü]', 'u', new)
        new = re.sub(r'[ç]', 'c', new)
        return new

    if (remove_accent(str(args.action)).lower() == 'cancel' or remove_accent(str(args.action)).lower() == 'annuler' or ('cancel' in [remove_accent(str(args.suite[i])).lower() for i in range(0, len(args.suite), 3)]) or ('annuler' in [remove_accent(str(args.suite[i])).lower() for i in range(0, len(args.suite), 3)]) )and local_remote == 'local':
        print("Be careful !!!\n\nCan't perform a CANCEL action when using the local API of tahoma: \nRun tahoma with the '--remote' argument.\n\nThe program will start with the 'remote' parameter...\n")
        local_remote = "remote"
        new_local_remote = "remote"

    ##########################PARAMETERING FUNCTION

    j=0
    for i in range(-1,int(len(args.suite)/3)) :
        if i == -1 :
            action = args.action
            category=args.category
            name=args.name
        else :
            action = args.suite[j]
            category = args.suite[j+1]
            name = args.suite[j+2]
            j=j+3

        url= []
        too_many_urls=[]
        bad_name=[]
        good_name=[]

        ##########################SHUTTERS
        
        if remove_accent(category) == 'shutter' or remove_accent(category) == 'volet':
            f = open(list_of_tahoma_shutters, 'r')
            content = f.read()
            f.close()
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's devices ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name.\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()
            success = 1
            if remove_accent(action).upper() == "OPEN" or remove_accent(action).upper() == "OUVRIR" :
                fonction = Command(OverkizCommand.OPEN, [0])
                success = 0
            elif remove_accent(action).upper() == 'CLOSE' or remove_accent(action).upper() == "FERMER" :
                fonction = Command(OverkizCommand.CLOSE, [0])
                success = 0
            elif remove_accent(action).upper() == 'STOP' :
                print("Please note that the 'stop' ACTION is only compatible with IO protocols and will not work with RTS devices. If you are using an RTS device, please use the command 'tahoma CANCEL LAST ACTION' instead.")
                fonction = Command(OverkizCommand.STOP, [0])
                success = 0
            elif remove_accent(action).upper() == 'MY' :
                fonction = Command(OverkizCommand.MY, [0])
                success = 0
            elif str(action).isnumeric() == True :
                if 0 <= int(action) <= 100 :
                    fonction = Command(OverkizCommand.SET_CLOSURE, [int(action)])
                    success = 0
                    print('Will close to '+str(action)+' %')
                    print("Be careful! This function is only available for IO protocols. It doesn't work with RTS devices...")
                else :
                    print("Your ACTION must be between 0 and 100. You have entered: "+str(action))
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [open close stop my NUMBER]")
            str1 = " "
            if success == 0:
#                print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
                message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)
                if logs == 'Y':
                    try:
                        with open(log_place, "a") as f:
                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                            f.close()
                    except: 
                        print('Could not access the log file. Permission denied')
                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                print(message)

        ##########################SUNSCREEN
        
        elif remove_accent(category) == 'sunscreen' or remove_accent(category) == 'rideau':
            f = open(list_of_tahoma_sunscreens, 'r')
            content = f.read()
            f.close()
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's devices ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()
            success = 1
            if remove_accent(action).upper() == "OPEN" or remove_accent(action).upper() == "OUVRIR" :
                fonction = Command(OverkizCommand.OPEN, [0])
                success = 0
            elif remove_accent(action).upper() == 'CLOSE' or remove_accent(action).upper() == "FERMER" :
                fonction = Command(OverkizCommand.CLOSE, [0])
                success = 0
            elif remove_accent(action).upper() == 'STOP' :
                print("Please note that the 'stop' function is only compatible with IO protocols and will not work with RTS devices. If you are using an RTS device, please use the command 'tahoma CANCEL LAST ACTION' instead.")
                fonction = Command(OverkizCommand.STOP, [0])
                success = 0
            elif remove_accent(action).upper() == 'MY' :
                fonction = Command(OverkizCommand.MY, [0])
                success = 0
            elif str(action).isnumeric() == True :
                if 0 <= int(action) <= 100 :
                    fonction = Command(OverkizCommand.SET_CLOSURE, [int(action)])
                    success = 0
                    print('Will close to '+str(action)+' %')
                    print("Be careful! This function is only available for IO protocols. It doesn't work with RTS devices...")
                else :
                    print("Your ACTION must be between 0 and 100. You have entered: "+str(action))
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [open close stop my]")
            str1 = " "
            if success == 0:
#                print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
                message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)
                if logs == 'Y':
                    try:
                        with open(log_place, "a") as f:
                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                            f.close()
                    except: 
                        print('Could not access the log file. Permission denied')
                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                print(message)

        ##########################SPOTALARMS PLUGS AND LIGHTS

        elif remove_accent(category) == 'spotalarm' or remove_accent(category) == 'plug' or remove_accent(category) == 'spotalarme' or remove_accent(category) == 'prise' or remove_accent(category) == 'light' or remove_accent(category) == 'lumiere':
            content = ''
            str1 = ''
            if remove_accent(category) == 'plug' or remove_accent(category) == 'prise':
                try :
                    f = open(list_of_tahoma_plugs, 'r')
                    content = f.read()
                    f.close()
                except FileNotFoundError: pass
            if remove_accent(category) == 'spotalarm' or remove_accent(category) == 'spotalarme':
                try :
                    f = open(list_of_tahoma_spotalarms, 'r')
                    content = f.read()
                    f.close()
                except FileNotFoundError: pass
            if remove_accent(category) == 'light' or remove_accent(category) == 'lumiere':
                try :
                    f = open(list_of_tahoma_lights, 'r')
                    content = f.read()
                    f.close()
                except FileNotFoundError: pass
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's devices ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()

            success = 1
            if remove_accent(action).upper() == "ON" or remove_accent(action).upper() == "ALLUMER" :
                fonction = Command(OverkizCommand.ON)
                success = 0
            elif remove_accent(action).upper() == 'OFF' or remove_accent(action).upper() == "ETEINDRE" :
                fonction = Command(OverkizCommand.OFF)
                success = 0
            elif remove_accent(action).upper() == 'TOGGLE' or remove_accent(action).upper() == "BASCULER" :
                f = open(list_of_tahoma_states, 'r')
                content = f.read()
                f.close()
                if str1.join(good_name).upper()+"," in content.upper():
                    async def state() -> None:
                        async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                            await client.login()
                            get_state = await client.get_state(str(url[0]))
#                            print(str(get_state).upper())
                            if "'OFF'" in str(get_state).upper():
                                fonction = Command(OverkizCommand.ON)
                                return fonction
                            else:
                                fonction = Command(OverkizCommand.OFF)
                                return fonction
                    overkiz_fonction = asyncio.run(state())
                    fonction = overkiz_fonction
                    success = 0
                else :
                    print("The device: "+str1.join(good_name)+" can't perform a toggle command. Perhaps because it's a RTS device.")
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [on off toggle]")
            if success == 0:
    #            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
                message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)
                if logs == 'Y':
                    try:
                        with open(log_place, "a") as f:
                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                            f.close()
                    except: 
                        print('Could not access the log file. Permission denied')
                        print("If you don’t want to see this message ag                        ain, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                print(message)

        ##########################ALARMS

        elif remove_accent(category) == 'alarm' or remove_accent(category) == 'alarme':
            f = open(list_of_tahoma_alarms, 'r')
            content = f.read()
            f.close()
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's devices ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()
            success = 1
            if remove_accent(action).upper() == "ARM" or remove_accent(action).upper() == "ACTIVER" or remove_accent(action).upper() == "ON":
                fonction = Command(OverkizCommand.ARM)
                success = 0
            elif remove_accent(action).upper() == 'DISARM' or remove_accent(action).upper() == "DESACTIVER" or remove_accent(action).upper() == "OFF" :
                fonction = Command(OverkizCommand.DISARM)
                success = 0
            elif remove_accent(action).upper() == 'PARTIAL' or remove_accent(action).upper() == "PARTIEL" :
                fonction = Command(OverkizCommand.PARTIAL)
                success = 0
            elif remove_accent(action).upper() == 'ARM_NIGHT' or remove_accent(action).upper() == "ACTIVER_NUIT" :
                fonction = Command(OverkizCommand.ARM_NIGHT)
                success = 0
            elif remove_accent(action).upper() == 'ARM_AWAY' or remove_accent(action).upper() == "ACTIVER_PARTI" :
                fonction = Command(OverkizCommand.ARM_AWAY)
                success = 0
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [arm disarm partial arm_night arm_away]")
            str1 = " "
            if success == 0:
    #            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
                message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)
                if logs == 'Y':
                    try:
                        with open(log_place, "a") as f:
                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                            f.close()
                    except: 
                        print('Could not access the log file. Permission denied')
                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                print(message)

        ##########################HEATERS

        elif remove_accent(category) == 'heater' or remove_accent(category) == 'chauffage':
            f = open(list_of_tahoma_heaters, 'r')
            content = f.read()
            f.close()
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's devices ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                        widget_heater = i.split(",")[2]
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
                         widget_heater = i.split(",")[2]
            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()
            success = 1
            if remove_accent(action).lower() == "comfort" or remove_accent(action).lower() == "confort" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort'])
                success = 0
            elif remove_accent(action).lower() == 'frostprotection' or remove_accent(action).lower() == "horsgel" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['frostprotection'])
                success = 0
            elif remove_accent(action).lower() == 'comfort-1' or remove_accent(action).lower() == "confort-1" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort-1'])
                success = 0
            elif remove_accent(action).lower() == 'comfort-2' or remove_accent(action).lower() == "confort-2" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort-2'])
                success = 0
            elif remove_accent(action).lower() == 'eco' :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['eco'])
                success = 0
            elif remove_accent(action).lower() == 'off' or remove_accent(action).lower() == "eteindre" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['off'])
                success = 0
            elif remove_accent(action).lower() == 'standby' or remove_accent(action).lower() == "veille" :
                if "adjustable" in widget_heater.lower() or "setpoint" in widget_heater.lower() :
#                if widget_heater == "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint" :
                    fonction = Command(OverkizCommand.SET_OPERATING_MODE, ['standby'])
                    success = 0
                else:
                    str1 = " "
                    message = "This ACTION: '"+action+"' is not compatible with your device.\nPlease provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]"
                    if logs == 'Y':
                        try:
                            with open(log_place, "a") as f:
                                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                f.close()
                        except: 
                            print('Could not access the log file. Permission denied')
                            print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                    print(message)
                    exit()
            elif remove_accent(action).lower() == 'manual' or remove_accent(action).lower() == "manuel" :
                if "adjustable" in widget_heater.lower() or "setpoint" in widget_heater.lower() :
#                if widget_heater == "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint" :
                    fonction = Command(OverkizCommand.SET_OPERATING_MODE, ['basic'])
                    success = 0
                else:
                    str1 = " "
                    message = "This ACTION: '"+action+"' is not compatible with your device: "+str1.join(good_name)+"\nPlease provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]"
                    if logs == 'Y':
                        try:
                            with open(log_place, "a") as f:
                                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                f.close()
                        except: 
                            print('Could not access the log file. Permission denied')
                            print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                    print(message)
                    exit()
            elif remove_accent(action).lower() == 'prog' :
                if "adjustable" in widget_heater.lower() or "setpoint" in widget_heater.lower() :
#                if widget_heater == "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint" :
                    fonction = Command(OverkizCommand.SET_OPERATING_MODE, ['internal'])
                    success = 0
                else:
                    str1 = " "
                    message = "This ACTION: '"+action+"' is not compatible with your device: "+str1.join(good_name)+"\nPlease provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]"
                    if logs == 'Y':
                        try:
                            with open(log_place, "a") as f:
                                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                f.close()
                        except: 
                            print('Could not access the log file. Permission denied')
                            print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                    print(message)
                    exit()
            elif remove_accent(action).lower() == 'auto' :
                if "adjustable" in widget_heater.lower() or "setpoint" in widget_heater.lower() :
#                if widget_heater == "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint" :
                    fonction = Command(OverkizCommand.SET_OPERATING_MODE, ['auto'])
                    success = 0
                else:
                    str1 = " "
                    message = "This ACTION: '"+action+"' is not compatible with your device: "+str1.join(good_name)+"\nPlease provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]"
                    if logs == 'Y':
                        try:
                            with open(log_place, "a") as f:
                                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                f.close()
                        except: 
                            print('Could not access the log file. Permission denied')
                            print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                    print(message)
                    exit()
            elif str(action).replace(".","").isnumeric():
                if "adjustable" in widget_heater.lower() or "setpoint" in widget_heater.lower() :
#                if widget_heater == "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint" :
                    fonction = Command(OverkizCommand.SET_TARGET_TEMPERATURE, [float(str(action))])
                    success = 0
                else:
                    str1 = " "
                    message = "This ACTION: '"+action+"' is not compatible with your device: "+str1.join(good_name)+"\nPlease provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]"
                    if logs == 'Y':
                        try:
                            with open(log_place, "a") as f:
                                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                f.close()
                        except: 
                            print('Could not access the log file. Permission denied')
                            print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                    print(message)
                    exit()
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as ACTION : [comfort comfort-1 comfort-2 eco off]")
                exit()
            str1 = " "
            if success == 0:
    #            print("Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
                message = "Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)
                if logs == 'Y':
                    try:
                        with open(log_place, "a") as f:
                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                            f.close()
                    except: 
                        print('Could not access the log file. Permission denied')
                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                print(message)

        ##########################SCENES

        elif remove_accent(category) == 'scene' or remove_accent(category) == 'scenario':
            f = open(list_of_tahoma_scenes, 'r')
            content = f.read()
            f.close()
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's scenes ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])

            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact. Did you mean : "+str(bad_name)+" ? Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()
            if len(url) > 1 :
                print("There is more than one match. The NAME you gave is not exact. Choose a UNIQUE part of word from this results as NAME argument or use [''] with the full name : "+str(too_many_urls)+"\nSee tahoma --list-names for help.")
                exit()

            
            #fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort'])
            #exec_id = await client.execute_scenario(device_url)

            str1 = " "
#            print("Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)
            if logs == 'Y':
                try:
                    with open(log_place, "a") as f:
                        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                        f.close()
                except: 
                    print('Could not access the log file. Permission denied')
                    print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
            print(message)

        ##########################SENSORS_STATES

        elif remove_accent(category) == 'sensor' or remove_accent(category) == 'capteur':
            command_state=[]
            f = open(list_of_tahoma_states, 'r')
            content = f.read()
            f.close()
            time.sleep(1)
            try:
                master_list = content.split("\n")
                master_list.remove('')
            except ValueError:
                print("\nDid you downloaded the list of Tahoma's sensors ?.\nExecute tahoma --getlist \nFor more info execute tahoma -h or tahoma --info")
                exit()
            for i in master_list :
                bad_name.append(i.split(",")[0])
                if len(name.split())>1 :
                    if remove_accent(i.split(",")[0]) == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                        command_state.append(i.split(",")[3])
                elif str(name).startswith("[") :
                    if '['+remove_accent(i.split(",")[0])+']' == remove_accent(str(name)) or remove_accent(str(name)).replace('[','').replace(']','') == remove_accent(i.split(",")[0]) :
                        url.append(i.split(",")[1])
                        too_many_urls.append(i.split(",")[0])
                        good_name.append(i.split(",")[0])
                        command_state.append(i.split(",")[3])
                else :
                    if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
                         url.append(i.split(",")[1])
                         too_many_urls.append(i.split(",")[0])
                         good_name.append(i.split(",")[0])
                         command_state.append(i.split(",")[3])

            if len(url)== 0 :
                print("There is no match. The NAME you gave is not exact or it's impossible to retrieve the state of '"+args.name+"'. \nPerhaps because it's RTS protocol and not IO. \n\nHere are supported devices : "+str(bad_name)+" \n\nChoose a UNIQUE part of word from this supported devices as NAME argument or if you want to indicate the exact NAME use square brackets AND quotation mark : ['NAME'] . \nFor exemple if you want to use the NAME <Heater Room 6> the syntax should be : ['Heater Room 6']. \n\nIf you don't find your device in this results try tahoma --getlist\nSee tahoma --list-names for help.")
                exit()

#            command_state=[]
#            time.sleep(1)
#            for i in master_list :
#                if remove_accent(i.split(",")[0]) in remove_accent(str(name)) or remove_accent(str(name)) in remove_accent(i.split(",")[0]) :
#                     command_state.append(i.split(",")[3])

        ##########################WAIT FUNCTION

        elif remove_accent(action) == 'wait' or remove_accent(action) == 'sleep' or remove_accent(action) == 'attendre':
            url.append(int(name.replace(":","")))

        ##########################CANCEL LAST ACTION FUNCTION

        elif remove_accent(action) == 'cancel' or remove_accent(action) == 'annuler':
            url.append('pass')

        ##########################

        else :
            print( "\nThe <CATEGORY> you have entered doesn't exist.\nChoose one of this category : "+str(list_categories)+"\nUse tahoma --help-categories or tahoma --list-categories for info")


    ##########################GENERATE NEW TOKEN AND GATEWAY.ID FOR 'LOCAL' CONFIG

        async def get_token_or_gateway_id() -> None:
            async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                await client.login()
                gateways = await client.get_gateways()
                gateway_id_list = []
                token_list = []
                try :
                    f = open(token_file, 'r')
                    token = f.read()
                    f.close()
                except FileNotFoundError:
                    token = ""
                try :
                    f = open(gateway_id_file, 'r')
                    gateway_id = f.read()
                    f.close()
                except FileNotFoundError:
                    gateway_id = ""
                if not gateway_id:
                    for gateway in gateways:
                        token2 = await client.generate_local_token(gateway.id)
                        await client.activate_local_token(gateway_id=gateway.id, token=token2, label="tahoma by @pzim-devdata")
                        if all(char.isdigit() or char == '-' for char in gateway.id) and gateway.id :
                                gateway_id_list.append(gateway.id)
                                #If many tahoma gateways, choosing the first one:
                                if len(gateway_id_list) > 1:
                                    print("You have more than one tahoma gateway, the process will be executed with the first one :")
                                    print(gateway_id_list[0]+"\n")
                                    time.sleep(5)
                                    print("Please provide the PIN number of the choosen tahoma gateway you want to use by executing `tahoma -c`")
                                    print("Choose one of this PIN number;")
                                    for pin in gateway_id_list:
                                        print("- "+pin)
                                        time.sleep(5)
                                gateway_id = gateway_id_list[0]
                        token_list.append(token2)
                        token = token_list[0]
                        f = open(token_file, 'w')
                        f.write(token)
                        f.close()
                        f = open(gateway_id_file, 'w')
                        f.write(gateway_id)
                        f.close()
                else:
                    f = open(gateway_id_file, 'r')
                    gateway_id = f.read()
                    f.close()
                    token2 = await client.generate_local_token(gateway_id)
                    await client.activate_local_token(gateway_id=gateway_id, token=token2, label="tahoma by @pzim-devdata")
                    token = token2
                    f = open(token_file, 'w')
                    f.write(token)
                    f.close()
                return token, gateway_id, gateway_id_list

    ##########################MAIN FUNCTION

        try:
            async def main() -> None:
                if local_remote == 'local':
                    great = 1
                    for value in [False,True]: # set verify_ssl to True then False if error occur. Verify_ssl to False if you don't use the .local hostname
                        if great == 1:
                            if remove_accent(category) == 'sunscreen' or remove_accent(category) == 'rideau' or remove_accent(category) == 'shutter' or remove_accent(category) == 'volet'or remove_accent(category) == 'heater' or remove_accent(category) == 'chauffage':
                                new_local_remote = 'local'
                                if args.local:
                                    print("Tahoma has been executed with the 'local' config for the category '"+category.lower()+"'")
                                try:
                                    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=value))
                                    great = 0
#                                    print("verify_ssl="+str(value))
                                    overkiz_function = 'OverkizClient(username="", password="", token="'+token+'", session=session, server=OverkizServer(name="Somfy TaHoma (local)",endpoint="https://gateway-'+gateway_id+'.local:8443/enduser-mobile-web/1/enduserAPI/",manufacturer="Somfy",configuration_url=None,))'
                                    break
                                except Exception as e:
                                    print("Error occure with verify_ssl="+str(value)+":\n"+e)
                            else:
                                new_local_remote = 'remote'
                                great =0
                                if remove_accent(action) != 'wait' and remove_accent(action) != 'attendre':
                                    if remove_accent(action) != 'cancel' and remove_accent(action) != 'annuler':
                                        print("Tahoma has been executed with the 'global' config because the '"+category.lower()+"' category is not yet supported for local use")
                                    else:
                                        print("\nCan't perform a CANCEL action when using a local API of tahoma: \nRun tahoma with the '--remote' argument.\n")
                                overkiz_function = 'OverkizClient(username="'+str(USERNAME)+'", password="'+str(PASSWORD)+'", server=SUPPORTED_SERVERS["'+str(serverchoice)+'"])'
                else:
                    new_local_remote = 'remote'
                    overkiz_function = 'OverkizClient(username="'+str(USERNAME)+'", password="'+str(PASSWORD)+'", server=SUPPORTED_SERVERS["'+str(serverchoice)+'"])'
                try :
                    j=0
                    for device_url in url :
                        if str(device_url).isnumeric() == True :
                            if ":" not in str(name):
                                message="Waiting for "+str(device_url)+" second(s)."
                                if logs == 'Y':
                                    try:
                                        with open(log_place, "a") as f:
                                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                            f.close()
                                    except: 
                                        print('Could not access the log file. Permission denied')
                                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                                print(message)
                                countdown(int(device_url))
    #                            time.sleep(int(device_url))
                            else:
                                message="At "+datetime.datetime.now().strftime('%H:%M')+", waiting for "+str(datetime.datetime.strptime(str(name), "%H:%M").strftime("%H:%M")+" (Local time, 24-hour format)")
                                if logs == 'Y':
                                    try:
                                        with open(log_place, "a") as f:
                                            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                            f.close()
                                    except: 
                                        print('Could not access the log file. Permission denied')
                                        print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                                print(message)
                                while True:
                                    hour = datetime.datetime.now().strftime("%H:%M")
                                    if hour == datetime.datetime.strptime(str(name), "%H:%M").strftime("%H:%M"):
                                        break
                                    time.sleep(1)
                        else :
                            if remove_accent(category) == 'scene' or remove_accent(category) == 'scenario':
                                try :
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
#                                    async with eval(overkiz_function) as client:
                                        await client.login()
                                        exec_id = await client.execute_scenario(device_url)
#                                        error = 0
#                                        return error
#                                except (NotAuthenticatedException,ClientConnectorError) as e:
#                                    print(e)
#                                    error = 1
#                                    return error
#                                except Exception as e:
#                                    if str(e) == "Missing authorization token" or str(e).startswith('Cannot connect to host'):
#                                        print(e)
#                                        error = 1
#                                        return error
#                                    else:
#                                        print(e)
#                                        error = 0
#                                        return error
                                except : pass
                            elif remove_accent(category) == 'sensor' or remove_accent(category) == 'capteur':
                                try:
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                                        await client.login()
                                        get_state = await client.get_state(device_url)
                                        state_function=str(command_state[j]).replace("['","").replace("']","")
                                        message=str(good_name[j])+':'+str(eval(state_function))
                                        if logs == 'Y':
                                            try:
                                                with open(log_place, "a") as f:
                                                    f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                                    f.close()
                                            except: 
                                                print('Could not access the log file. Permission denied')
                                                print("If you don’t want to see this message again, reconfigure Tahoma to NOT create a log file (tahoma --configure) \nor reinstall Tahoma in an accessible folder (without using the sudo command on Linux).")
                                        print(message)
                                except :pass
                            elif remove_accent(action).upper() == 'CANCEL' or remove_accent(action).upper() == 'ANNULER':
                                try:
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                                        await client.login()
                                        executions = await client.get_current_executions()
                                        for execution in executions:
                                            execution_id=str(execution.id)
                                        try:
                                            await client.cancel_command(str(execution_id))
                                            message="The last command: '"+execution.action_group['actions'][0]['commands'][0]['name']+"' has been successfully cancelled."
                                            if logs == 'Y':
                                                try:
                                                    with open(log_place, "a") as f:
                                                        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                                                        f.close()
                                                except: 
                                                    print('Could not access the log file. Permission denied')
                                                    print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
                                            print(message)
                                        except: pass 
                                except: pass
                            else :
                                try :
                                    if token and gateway_id and local_remote == 'local' or token and gateway_id and new_local_remote == 'local' or local_remote == 'remote' or new_local_remote == 'remote':
                                        async with eval(overkiz_function) as client:
                                            await client.login()
    #                                        print("Local API connection succesfull!")
    #                                        print(str(fonction))
    #                                        print(device_url)
                                            exec_id = await client.execute_command( device_url, fonction )
                                        error = 0
    #                                    print("execution")
                                        try:
                                            await session.close()
                                        except: pass
                                        return error
                                    else:
                                        error = 1
                                        try:
                                            await session.close()
                                        except: pass
                                        return error
                                except (NotAuthenticatedException,ClientConnectorError) as e:
                                    print(e)
                                    error = 1
                                    try:
                                        await session.close()
                                    except: pass 
                                    return error
                                except Exception as e:
                                    if str(e) == "Missing authorization token" or str(e).startswith('Cannot connect to host'):
                                        error = 1
                                        try:
                                            await session.close()
                                        except: pass 
                                        return error
                                    else:
                                        print(e)
                                        error = 0
                                        try:
                                            await session.close()
                                        except: pass 
                                        return error
                            j=j+1
                except Exception as e:
                    print(e) 
                    try:
                        if notification.lower() == 'y'or notification.lower() == 'yes':
                            os.system("notify-send -i "+icon_app+" -t 150000 Tahoma "+"'Program failed. Here is the error message :\n\n "+str(e)+"'")
                    except:pass
                    exit()
        except Exception as e:
            print( e )
            try :
                if notification.lower() == 'y'or notification.lower() == 'yes':
                    os.system("notify-send -i "+icon_app+" -t 150000 Tahoma "+"'Program failed. Here is the error message :\n\n "+str(e)+"'")
            except: pass

        execute = asyncio.run(main())
        if execute == 1:
            print("\nCouldn't connect, trying to get a new token or a new gateway_id...")
            get_token_gataway_id = asyncio.run(get_token_or_gateway_id())
            try:
                token = get_token_gataway_id[0]
                gateway_id = get_token_gataway_id[1]
                if token and gateway_id:
                    print("Succes, new token available and found the gateway_id")
#                    print("Tahoma will use the token : "+token)
                    print("If you also use the local API with Homebridge or Home Assistant, you will need to use this new token: "+token)
                    print("Your token will be store there: \n"+token_file)
                    print("Tahoma will use this PIN number of the gateway : "+gateway_id)
                    print("The PIN number of your gateway will be store there: \n"+gateway_id_file)
                    execute = asyncio.run(main())
                else:
                    print("\nThere is a problem with the 'local' config. \nTry to use the '--remote' argument, check your login and password or reconfigure tahoma: 'tahoma -c'")
                    time.sleep(5)
                    print("Using the 'remote' config...")
                    time.sleep(2)
                    local_remote = "remote"
                    execute = asyncio.run(main())
            except Exception as e:
                print(e)
                print("\nThere is a problem with the 'local' config. \nTry to use the '--remote' argument, check your login and password or reconfigure tahoma: 'tahoma -c'")
                time.sleep(5)
                print("Using the 'remote' config...")
                time.sleep(2)
                local_remote = "remote"
                execute = asyncio.run(main())

        try:
            if notification.lower() == 'y'or notification.lower() == 'yes':
                os.system("notify-send -i "+icon_app+" -t 150000 Tahoma 'Program succeded !'")
        except: pass



if __name__ == "__main__":
    # Catch all untrapped exceptions
    try:
        main()
        exit(0)
    except Exception as error:
        print(error)
        exit(1)
