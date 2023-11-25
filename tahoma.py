#!/usr/bin/python3
#sudo python3 -m pip install pyoverkiz -U
#sudo python3 -m pip install tahoma -U
#tahoma.py by @pzim-devdata
#MIT Licence

"""
This is the main module
"""

import asyncio
import sys
import argparse
import os
import re
from getpass import getpass
import time
import datetime
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.client import OverkizClient
from pyoverkiz.enums import OverkizCommand
from pyoverkiz.models import Command
from pyoverkiz.models import Scenario
import __version__
import requests
import base64
from hashlib import sha256

version_number=str(__version__.__version__)
get_devices_url="import get_devices_url"

url_releases = 'https://api.github.com/repos/pzim-devdata/tahoma/releases'

def check_last_release (show='y'):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url_releases, headers=headers)
        releases = response.json()
        last_release = releases[0]['tag_name']
        info_release = releases[0]["body"]
        if str(last_release.lower()) == str(version_number).lower():
            if show == 'y' :
                print(" You are using the last version of Tahoma : " + str(last_release.lower()))
        else :
            print(" Last version of Tahoma is : " + str(last_release.lower()) + " and you are using the version : " + str(version_number).lower())
            print(" Here is an explanation of this update:")
            print( info_release)
            print( "")
            print(" Pypi version : python3 -m pip install -U tahoma or pipx upgrade tahoma")
            print(" Github version : https://github.com/pzim-devdata/tahoma/releases/latest/download/tahoma.zip")
    except : pass

check_last_release ('n')

def countdown(duration):
    for i in range(duration-1, 0, -1):
        sys.stdout.write("\033[2K\r")  # Efface toute la ligne
        sys.stdout.write(str(i) + "\r")  
        sys.stdout.flush()
        time.sleep(1)
#    print("Sucess!")
#    sys.stdout.write("\rFin!\n")

def main():
    version ='tahoma - portable Version '+ str(version_number)+' - by @pzim-devdata'

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

    notification_consent = os.path.dirname(os.path.abspath(__file__))+'/temp/consent_notification.txt'

    server_choosen =  os.path.dirname(os.path.abspath(__file__))+'/temp/server_choosen.txt'

    init_file = os.path.dirname(os.path.abspath(__file__))+'/__init__.py'

    logs_consent = os.path.dirname(os.path.abspath(__file__))+'/temp/consent_logs.txt'
    log_place = os.path.dirname(os.path.abspath(__file__))+'/temp/last_commands_send.log'
    #delete log_place if size > 1000 octets
    try:
        size_log = os.path.getsize(log_place)
        if size_log > 1000:
            os.remove(log_place)
            print(f"The old log file : {log_place} has been removed because of it size > 1000 octets\nA new file will be created.\n")
    except FileNotFoundError:
        pass

    list_categories = ['shutter','spotalarm','plug','light','alarm','heater','sunscreen','scene','sensor']
    list_categories_french = ['volet','spotalarme','prise','lumiere','alarme','chauffage','rideau','scenario','capteur']
    list_actions = ['[open,close,stop,my,NUMBER]','[on,off]','[on,off]','[on,off]','[arm,disarm,partial,arm_night,arm_away]','[comfort,comfort-1,comfort-2,eco,frostprotection,off]','[open,close,stop,my,NUMBER]','[on,activate,launch,execute]','[get,get_state,get_position,get_lumens,get_temperature]']
    list_actions_french = ['[ouvrir,fermer,stop,my,NOMBRE]','[allumer,eteindre]','[allumer,eteindre]','[allumer,eteindre]','[activer,desactiver,partiel,activer_nuit,activer_parti]','[confort,confort-1,confort-2,eco,horsgel,eteindre]','[ouvrir,fermer,stop,my,NOMBRE]','[lancer,activer,executer]','[obtenir,etat,position,luminosite,temperature]']

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
        print( "              sudo python3 -m pip install tahoma -U" )
        print( "                   https://pypi.org/project/tahoma/" )
        print( "                 https://github.com/pzim-devdata/tahoma" )
        print( "                          contact@pzim.fr" )
        print( "" )
        print( " USAGE : tahoma [ACTION] [CATEGORY] [NAME]" )
        print( "")
        print( " - List of possible ACTIONS : \n "+str(list_actions) )
        print( " - Liste des ACTIONS possibles : \n "+str(list_actions_french) )
        print( "" )
        print( " - List of possible CATEGORIES : \n "+str(list_categories) )
        print( " - Liste des CATEGORIES possibles : \n "+str(list_categories_french) )
        print( "" )
        print( ' - List of available NAMES : tahoma --list-names \n - Liste des NOMS possibles : tahoma --list-names-french \n You must provide a part of the name you have assigned to the device in the Tahoma App. \n It must be a single and unique word, not taken by another device of the same category !\n For instance if you have two devices called <Alarm 1> and <Alarm 2> you will need to choose <2> as device [NAME] for <Alarm 2> and not <Alarm>).\n You can also use the full NAME with [""].\n For instance ["Alarm 2"]\n See tahoma --list or tahoma --help for info.')
        print( "" )
        print( " You must provide at least 3 arguments" )
        print( " For instance :  tahoma open shutter kitchen")
        print( "\n You can close a shutter or a sunscreen to a specific level (IO protocols only)")
        print( " For instance : tahoma 25 shutter kitchen. It will open the shutter to 75% or close it to 25%" )
        print( "" )
        print( " You can also provide, as many as you wish, orders on the same line." ) 
        print( " Tahoma will execute all orders one by one in the same process ;-)" )
        print( " For instance : tahoma open shutter kitchen arm alarm garden on plug room wait train garestation " )
        print( "" )
        print( " You can add a wait function with 'wait for' or 'sleep for'")
        print( " Tahoma will wait the time in seconds you have specified")
        print( " For instance : tahoma open shutter kitchen wait for 20 on plug room")
        print( "" )
        print( " The STOP action for shutters and sunscreens doesn't work with RTS protocols. " ) 
        print( " Instead you can cancel the immediate preceding command (without affecting a 'wait for <SECONDS>' command)." )
        print( " To do this you can use the command 'cancel last action' just after a command that opens or closes an RTS device." )
        print( " For instance : 'tahoma open shutter kitchen wait for 2 cancel last action' : It will stop the kitchen shutter after 2 seconds" )
        print( "" )
        print( " FIRST you must configure login and password : sudo tahoma -c " )
        print( " It will be stored there : \n "+passwd_file )
        print( "" )
        print( " THEN you must download the list of all yours devices : sudo tahoma -g " )
        print( " It will be stored there : \n "+list_of_tahoma_devices )
        print( "" )
        print( "                     To get help : tahoma -h " )
        print( "")
        print( "                   To show this sceen : tahoma -i" )
        print( "" )
        print( "      Il existe une aide en français : tahoma --help-french " )
        print( " ********************************************************************        " )
        print( "" )
        check_last_release ()
        print( "" )
        print( "    Open your terminal in full screen mode to have a better view \n" )
    #    try :
    #        os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
    #        print( " \n          <--- Appuyez sur F11 to close fullscreen --->\n")
    #        print( " \n             <--- Press F11 to close fullscreen --->\n")
    #    except Exception :
    #       print( "       Open your terminal in full screen to have a better view ")
        exit()

    str_info = "You must provide at least three arguments\n\nFor instance : tahoma  open shutter kitchen \n\nRun <b>tahoma --help</b> for help"

    ##########################ARGUMENTS

    for arg in sys.argv :
            try :
                if arg == '-v' or arg == '--version' :
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
            print("Do you want to show desktop notifications ? (Only for Linux users) (Y/n)")
            notification = input()
            if notification.lower() == 'y'or notification.lower() == 'yes':
                f = open(notification_consent, 'w')
                f.write('Yes')
                f.close()
            else :
                print("Consent file for notifications removed. You will not get any desktop notification")
                try :
                    os.remove(notification_consent)
                except : pass
            print("\nDo you want to create a log file ? (Y/n)")
            notification = input()
            if notification.lower() == 'y'or notification.lower() == 'yes':
                f = open(logs_consent, 'w')
                f.write('Y')
                print("Logs file will be created there :\n"+log_place)
                f.close()
            else :
                print("No file will be created for keeping logs")
                try :
                    os.remove(logs_consent)
                except : pass
            print("Paste which server you want to use : somfy_europe , somfy_america or somfy_oceania :")
            serverchoice = input()
            if serverchoice == "somfy_europe" or serverchoice == "somfy_america" or serverchoice == "somfy_oceania" :
                print( "You have selected "+serverchoice )
                f = open(server_choosen, 'w')
                f.write(serverchoice)
                f.close()
            else :
                print( "The server you provided in incorrect ! 'somfy_europe' will be used instead\n" )
                serverchoice = "somfy_europe"
                f = open(server_choosen, 'w')
                f.write(serverchoice)
                f.close() 
            print( "Please provide somfy-connect's username for tahoma-pzim (mail address) : \nIt will be stored here : \n"+passwd_file+"\nIf you don't want to store it localy, you can leave it empty, but you will need to connect with the --username argument each time")
            print("Username:")
            USERNAME = input()
            print( "\nPlease provide somfy-connect's password for tahoma-pzim : \nIt will be stored here : \n"+passwd_file+"\nYou can leave it empty, but you will need to connect with the --password argument each time")
            PASSWORD = getpass()
            print( "Do you want to store them in "+passwd_file+" ? \nIf Not, the file will be erased\n(Y/n)")
            CONSENT = input()
            if CONSENT.lower() == 'y'or CONSENT.lower() == 'yes':
                os.remove(passwd_file)
                f = open(passwd_file, 'ab')
                f.write(base64.b64encode(str(USERNAME+":"+PASSWORD+init_str).encode('utf-8')))
                f.close()
                print( "stored in "+passwd_file )
            else :
                try :
                    os.remove(passwd_file)
                    print( "The file "+passwd_file+" has been removed" )
                    print( "To connect to tahoma provide the logins info in this way : tahoma --username <mail address> --password <password>" )
                    print( passwd_file+" is removed" )
                except : 
                    print("The file was already removed")
            exit()

    for arg in sys.argv :
        if arg == '-h' or arg == '--help' :
            print("tahoma -h, --help : "+version+"\n\nUsage:\n tahoma ACTION CATEGORY NAME \n\n You must provide at least three arguments\n For instance : tahoma open shutter kitchen or tahoma ouvrir volet cuisine\n\n You can close a shutter or a sunscreen to a specific level (IO protocols only)\n For instance : tahoma 25 shutter kitchen. It will open the shutter to 75% or close it to 25%\n\n You can also provide, as many as you wish, orders on the same line\n Tahoma will execute all orders one by one in the same process ;-)\n For instance : tahoma open shutter kitchen arm alarm garden on plug room wait train garestation\n\nHelp options :\n -h,   --help                      Show this help\n -hf,  --help-french               Show this help in french\n -i,   --info                      Show more info\n\nPlugin options :\n -v,   --version                   Show the version of the plugin\n -c,   --configure                 To configure the plugin and store login and password in a text file which is located here : "+passwd_file+"\n -u,   --username                  If you don't want to store the login, you can provide the mail-address with this option\n -p,   --password                  If you don't want to store the password, you can provide it with this option\n -g,   --getlist                   Download the list of devices and store them here : "+list_of_tahoma_devices+"\n -l,   --list                      Show the complet list of devices installed\n -la,  --list-actions              Show the list of possible ACTIONS by CATEGORIES\n -lc,  --list-categories           Show all supported CATEGORIES of devices\n -lnf, --list-names                Show all installed devices by there NAMES\n\nCommand options :\n wait for <seconds>\n sleep for <seconds>               Tahoma will wait for <seconds> seconds to execute next action\n cancel last action                Tahoma will cancel the immediate preceding command (without affecting the 'wait for' command). This is useful for stopping an RTS device\n")
            check_last_release ()
            exit()

    for arg in sys.argv :
        if arg == '-hf' or arg == '--help-french' :
            print("tahoma -h --help : "+version+"\n\nUsage:\n tahoma ACTION CATEGORIE NOM \n\n Vous devez fournir au moins trois arguments\n Par exemple : tahoma ouvrir volet cuisine ou tahoma open shutter kitchen\n\n Vous pouvez fermer des rideaux ou des volets à un niveau precis (Seulement pour les équipements utilisant le protocole IO)\n Par exemple : tahoma 25 volet cuisine. Les volets vont s'ouvrir de 75% ou se fermer de 25%\n\n Vous pouvez aussi spécifier autant de commandes que vous le souhaitez sur la même ligne :\n Tahoma va executer chaque commande l'une aprés l'autre durant le même processus\n Par exemple : tahoma ouvrir volet cuisine confort chauffage salon\n\nOptions de l’aide :\n -h, --help                        Affiche les options de l’aide en anglais\n\nOptions de l’application :\n -v, --version                     Affiche la version de l’application\n -i, --info                        Afficher plus d'infos sur tahoma\n -c, --configure                   Renseigner l'identifiant et le mot de passe dans un fichier texte pour ne pas devoir les renseigner à chaque fois. Le fichier texte se situe dans : "+passwd_file+"\n -u, --username                    Renseigner le nom d'utilisateur\n -p, --password                    Renseigner le mot de passe de Somfy-connect\n -g, --getlist                     Télécharge la liste des équipements et la stocke dans "+list_of_tahoma_devices+"\n -l, --list                        Affiche la liste téléchargée des équipements\n -laf, --list-actions-french       Affiche la liste des ACTIONS possibles en français par CATEGORIES\n -lcf, --list-categories-french    Affiche toutes les CATEGORIES d'équipements pris en charge en français\n -lnf, --list-names-french         Affiche les NOMS des équipements installés par categories en français\n\nOptions de commande :\n attendre pendant <secondes>       Tahoma attendra <secondes> secondes avant d'éxécuter la commande suivante\n annuler precedente commande       Tahoma annulera la commande précédente immédiate (sans affecter la commande 'attendre pendant'). Ceci est utile pour arrêter un périphérique RTS.")
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
            print( '\nYou must provide a part of the NAME as argument \nt must be a single and unique word, not taken by another device of the same category !\n For instance if you have two devices called <Alarm 1> and <Alarm 2> you will need to choose <2> as device [NAME] for <Alarm 2> and not <Alarm>).\n You can also use the full NAME with [""].\n For instance ["Alarm 2"]\n See tahoma --list or tahoma --help for info.')
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

    parser.add_argument("action")
    parser.add_argument("category")
    parser.add_argument("name")
    parser.add_argument("suite", nargs='*')

    args = parser.parse_args()
#    print(f'Input action(s) : {args.action} {args.category} {args.name} '+' '.join(args.suite) )

    if args.password:
        PASSWORD = (f'{args.password}')
    if args.username:
        USERNAME = (f'{args.username}')

    def remove_accent(old):
        new = old.lower()
        new = re.sub(r'[àáâãäå]', 'a', new)
        new = re.sub(r'[èéêë]', 'e', new)
        new = re.sub(r'[ìíîï]', 'i', new)
        new = re.sub(r'[òóôõö]', 'o', new)
        new = re.sub(r'[ùúûü]', 'u', new)
        new = re.sub(r'[ç]', 'c', new)
        return new

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

            if remove_accent(action).upper() == "OPEN" or remove_accent(action).upper() == "OUVRIR" :
                fonction = Command(OverkizCommand.OPEN)
            elif remove_accent(action).upper() == 'CLOSE' or remove_accent(action).upper() == "FERMER" :
                fonction = Command(OverkizCommand.CLOSE)
            elif remove_accent(action).upper() == 'STOP' :
                print("Please note that the 'stop' ACTION is only compatible with IO protocols and will not work with RTS devices. If you are using an RTS device, please use the command 'tahoma CANCEL LAST ACTION' instead.")
                fonction = Command(OverkizCommand.STOP)
            elif remove_accent(action).upper() == 'MY' :
                fonction = Command(OverkizCommand.MY)
            elif str(action).isnumeric() == True :
                fonction = Command(OverkizCommand.SET_CLOSURE, [int(action)])
                print('Will close to '+str(action)+' %')
                print("Be careful! This function is only available for IO protocols. It doesn't work with RTS devices...")
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [open close stop my]")
            str1 = " "
#            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
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

            if remove_accent(action).upper() == "OPEN" or remove_accent(action).upper() == "OUVRIR" :
                fonction = Command(OverkizCommand.OPEN)
            elif remove_accent(action).upper() == 'CLOSE' or remove_accent(action).upper() == "FERMER" :
                fonction = Command(OverkizCommand.CLOSE)
            elif remove_accent(action).upper() == 'STOP' :
                print("Please note that the 'stop' function is only compatible with IO protocols and will not work with RTS devices. If you are using an RTS device, please use the command 'tahoma CANCEL LAST ACTION' instead.")
                fonction = Command(OverkizCommand.STOP)
            elif remove_accent(action).upper() == 'MY' :
                fonction = Command(OverkizCommand.MY)
            elif str(action).isnumeric() == True :
                fonction = Command(OverkizCommand.SET_CLOSURE, [int(action)])
                print('Will close to '+str(action)+' %')
                print("Be careful! This function is only available for IO protocols. It doesn't work with RTS devices...")
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [open close stop my]")
            str1 = " "
#            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
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
            content2 = ''
            content3 = ''
            content4 = ''
            try :
                f = open(list_of_tahoma_plugs, 'r')
                content2 = f.read()
                f.close()
            except FileNotFoundError: pass
            try :
                f = open(list_of_tahoma_spotalarms, 'r')
                content3 = f.read()
                f.close()
            except FileNotFoundError: pass
            try :
                f = open(list_of_tahoma_lights, 'r')
                content4 = f.read()
                f.close()
            except FileNotFoundError: pass
            content=content2+content3+content4
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

            if remove_accent(action).upper() == "ON" or remove_accent(action).upper() == "ALLUMER" :
                fonction = Command(OverkizCommand.ON)
            elif remove_accent(action).upper() == 'OFF' or remove_accent(action).upper() == "ETEINDRE" :
                fonction = Command(OverkizCommand.OFF)
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [on off]")
            str1 = " "
#            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
            if logs == 'Y':
                try:
                    with open(log_place, "a") as f:
                        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{message}\n")
                        f.close()
                except: 
                    print('Could not access the log file. Permission denied')
                    print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
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

            if remove_accent(action).upper() == "ARM" or remove_accent(action).upper() == "ACTIVER" or remove_accent(action).upper() == "ON":
                fonction = Command(OverkizCommand.ARM)
            elif remove_accent(action).upper() == 'DISARM' or remove_accent(action).upper() == "DESACTIVER" or remove_accent(action).upper() == "OFF" :
                fonction = Command(OverkizCommand.DISARM)
            elif remove_accent(action).upper() == 'PARTIAL' or remove_accent(action).upper() == "PARTIEL" :
                fonction = Command(OverkizCommand.PARTIAL)
            elif remove_accent(action).upper() == 'ARM_NIGHT' or remove_accent(action).upper() == "ACTIVER_NUIT" :
                fonction = Command(OverkizCommand.ARM_NIGHT)
            elif remove_accent(action).upper() == 'ARM_AWAY' or remove_accent(action).upper() == "ACTIVER_PARTI" :
                fonction = Command(OverkizCommand.ARM_AWAY)
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [arm disarm partial arm_night arm_away]")
            str1 = " "
#            print("Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).upper()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
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

            if remove_accent(action).lower() == "comfort" or remove_accent(action).lower() == "confort" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort'])
            elif remove_accent(action).lower() == 'frostprotection' or remove_accent(action).lower() == "horsgel" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['frostprotection'])
            elif remove_accent(action).lower() == 'comfort-1' or remove_accent(action).lower() == "confort-1" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort-1'])
            elif remove_accent(action).lower() == 'comfort-2' or remove_accent(action).lower() == "confort-2" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['comfort-2'])
            elif remove_accent(action).lower() == 'eco' :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['eco'])
            elif remove_accent(action).lower() == 'off' or remove_accent(action).lower() == "eteindre" :
                fonction = Command(OverkizCommand.SET_HEATING_LEVEL,['off'])
            else :
                print( "\n'"+action+"'"+" is not a valide action.\n")
                print("Please provide one of this argument as action : [comfort comfort-1 comfort-2 eco off]")
                exit()
            str1 = " "
#            print("Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)+ " \nwith url : "+str1.join(url))
            message = "Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
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
            message = "Output action : "+remove_accent(action).lower()+" "+remove_accent(category)+" "+str1.join(good_name)+"\n"+"Success!"
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
            url.append(int(name))

        ##########################CANCEL LAST ACTION FUNCTION

        elif remove_accent(action) == 'cancel' or remove_accent(action) == 'annuler':
            url.append('pass')

        ##########################

        else :
            print( "\nThe <CATEGORY> you have entered doesn't exist.\nChoose one of this category : "+str(list_categories)+"\nUse tahoma --help-categories or tahoma --list-categories for info")


    ##########################MAIN FUNCTION

        try:
            async def main() -> None:
                try :
                    j=0
                    for device_url in url :
                        if str(device_url).isnumeric() == True :
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
                        else :
                            if remove_accent(category) == 'scene' or remove_accent(category) == 'scenario':
                                try :
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                                        await client.login()
                                        exec_id = await client.execute_scenario(device_url)
                                except : pass
                            elif remove_accent(category) == 'sensor' or remove_accent(category) == 'capteur':
                                try:
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
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
                                                print("If you don’t want to see this message again, reconfigure Tahoma to not create a log file (tahoma --configure) \nor install Tahoma in an accessible folder.")
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
                                except : pass
                            else :
                                try :
                                    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
                                        await client.login()
                                        exec_id = await client.execute_command( device_url, fonction )
                                except : pass
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

        asyncio.run(main())

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
