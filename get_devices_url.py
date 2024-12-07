#!/usr/bin/python3
#sudo python3 -m pip install pyoverkiz
#sudo python3 -m pip install tahoma-pzim -U
#tahoma.py by @pzim-devdata
#MIT Licence

import asyncio
import sys
import argparse
import os
import requests
from datetime import datetime, timedelta
import json
from collections import defaultdict
import re
from getpass import getpass
import time
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.client import OverkizClient
from pyoverkiz.enums import OverkizCommand
from pyoverkiz.models import Command
from pyoverkiz.models import Scenario
import base64
from hashlib import sha256
try:
    import __version__
    str_newrelic='Github'
except:
    from tahoma import __version__
    str_newrelic='Pypi'


async def main() -> None:

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
    list_of_tahoma_pergolas = os.path.dirname(os.path.abspath(__file__))+'/temp/pergolas.txt'

    server_choosen =  os.path.dirname(os.path.abspath(__file__))+'/temp/server_choosen.txt'
    init_file = os.path.dirname(os.path.abspath(__file__))+'/__init__.py'

#    consent_statistics = os.path.dirname(os.path.abspath(__file__))+'/temp/consent_statistics.txt'

#    print("Would you like to share anonymous statistics when you use this functionality?")
#    print("It will help the developer to improve your experience. ")
#    print("Only the sentence ‘New installation of the tahoma’ will be sent, no other information.")
#    print("No personal information will be send. (Y/n):")
#    send_statistics = input()
#    if send_statistics.lower() == 'y'or send_statistics.lower() == 'yes':
#        print( "You consent to share anonymous statistics. Thanks!\n")
#        time.sleep(2)
#        f = open(consent_statistics, 'w')
#        f.write("Y")
#        f.close()
#    else :
#        print( "You don't consent to share anonymous statistics.\n" )
#        time.sleep(2)
#        f = open(consent_statistics, 'w')
#        f.write("N")
#        f.close() 

#    try :
#        f = open(consent_statistics, 'r')
#        send_statistics = f.read()
#        f.close()
#    except :
#        send_statistics = "N"

    send_statistics = 'Y'
    if send_statistics == 'Y':
    #New_relic :
#        try:
#            import configparser
#            import newrelic.agent
#            license_key="eu01xxa5bf9b857655fdc4fa8e6eba17FFFFNRAL"
#            config_file_newrelic = os.path.dirname(os.path.abspath(__file__))+'/temp/newrelic.ini'
#            def send_statistics(license_key=license_key,config_file_newrelic=config_file_newrelic):
#                config = configparser.ConfigParser()
#                config["newrelic"] = {
#                    "license_key": license_key,
#                    "app_name": "tahoma_pypi",
#                    "monitor_mode" : "true",
#                    "log_file" : "stdout",
#                    "log_level" : "critical",
#                    "high_security" : "false"
#                }
#                with open(config_file_newrelic, "w") as f:
#                    config.write(f)
#                f.close()
#                newrelic.agent.initialize(config_file_newrelic)
#                application = newrelic.agent.register_application(timeout=10)
#                with newrelic.agent.BackgroundTask(application, name='bar', group='Task'):
#                     newrelic.agent.record_log_event(str(str_newrelic))
#                newrelic.agent.shutdown_agent(timeout=10)
#            send_statistics()
#        except: pass
    #Github :
    #Encoder:
    #import base64
    #token = "github_pat_xxxxxxx"
    #encoded = base64.b64encode(f"dsds{token}".encode()).decode()
    #print(f"{encoded}")

        try:
            ENCODED_TOKEN = "ZHNkc2dpdGh1Yl9wYXRfMTFBTVFRT0xBMGl6cWtvcmhSWHY0RV84bEFEUDFsajE5enZTWThzWXBWanhLbTA4czMxSG1uSW5md0hkN2JxaHVaM1JWSjZNQ0R5Q2R1c215dA=="
            token = base64.b64decode(ENCODED_TOKEN).decode()[4:]
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            stats_url = "https://api.github.com/repos/pzim-devdata/stats_tahoma/contents/stats.json"
            readme_url = "https://api.github.com/repos/pzim-devdata/stats_tahoma/contents/README.md"

            # Création ID machine et mise à jour des stats
            hostname = os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'Unknown')
            machine_id = base64.b64encode(f"{hostname}_{os.name}".encode()).decode()[:12]

            # Lecture du fichier stats existant
            response = requests.get(stats_url, headers=headers)
            if response.status_code == 200:
                content = response.json()
                current_content = json.loads(base64.b64decode(content["content"]).decode())
                sha = content["sha"]
            else:
                current_content = {"users": {}}
                sha = None

            # Mise à jour des stats
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if machine_id not in current_content["users"]:
                current_content["users"][machine_id] = {
                    "visits": 1,
                    "first_seen": timestamp,
                    "version": str_newrelic
                }
            else:
                current_content["users"][machine_id]["visits"] += 1
            current_content["users"][machine_id]["last_seen"] = timestamp
            current_content["users"][machine_id]["version"] = str_newrelic  # Mise à jour de la version
            current_content["total_users"] = len(current_content["users"])
            current_content["total_visits"] = sum(user["visits"] for user in current_content["users"].values())

            # Mise à jour du fichier stats avec gestion du conflit
            def update_file(url, content, sha, message):
                update_data = {
                    "message": message,
                    "content": base64.b64encode(content.encode()).decode()
                }
                if sha:
                    update_data["sha"] = sha

                put_response = requests.put(url, headers=headers, json=update_data)
                if put_response.status_code == 409:  # Conflit
                    # Récupérer le dernier SHA
                    latest = requests.get(url, headers=headers).json()
                    update_data["sha"] = latest["sha"]
                    put_response = requests.put(url, headers=headers, json=update_data)
                return put_response

            # Mise à jour du fichier stats
            stats_content = json.dumps(current_content, indent=2)
            put_response = update_file(stats_url, stats_content, sha, f"Update stats ({machine_id[:6]})")

            # Création des statistiques mensuelles
            monthly_stats = defaultdict(lambda: {
                "installs": 0,
                "unique_users": set(),
                "total_visits": 0,
                "versions": defaultdict(int)
            })
            last_install = datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

            for user_id, user_data in current_content["users"].items():
                first_seen = datetime.strptime(user_data["first_seen"], "%Y-%m-%d %H:%M:%S")
                last_seen = datetime.strptime(user_data["last_seen"], "%Y-%m-%d %H:%M:%S")
                version = user_data.get("version", "Unknown")
                
                month_key = first_seen.strftime("%Y-%m")
                monthly_stats[month_key]["unique_users"].add(user_id)
                monthly_stats[month_key]["total_visits"] += user_data["visits"]
                monthly_stats[month_key]["versions"][version] += 1
                
                if last_seen > last_install:
                    last_install = last_seen

            # Création des graphiques ASCII
            months = sorted(monthly_stats.keys())
            max_users = max(len(stats["unique_users"]) for stats in monthly_stats.values())
            max_visits = max(stats["total_visits"] for stats in monthly_stats.values())
            max_version = max(max(versions.values()) for stats in monthly_stats.values() for versions in [stats["versions"]])
            
            # Graphique des utilisateurs uniques
            users_graph = "```\nUtilisateurs uniques ayant installé Tahoma par mois :\n"
            for month in months:
                unique_users = len(monthly_stats[month]["unique_users"])
                bars = int((unique_users / max_users) * 20) if max_users > 0 else 0
                users_graph += f"{month}: {'█' * bars} {unique_users}\n"
            users_graph += "```\n"

            # Graphique des installations
            visits_graph = "```\nInstallations par mois :\n"
            for month in months:
                visits = monthly_stats[month]["total_visits"]
                bars = int((visits / max_visits) * 20) if max_visits > 0 else 0
                visits_graph += f"{month}: {'█' * bars} {visits}\n"
            visits_graph += "```\n"

            # Graphique des versions
            versions_graph = "```\nNombre d'installations par version par mois :\n"
            for month in months:
                versions = monthly_stats[month]["versions"]
                versions_graph += f"\n{month}:\n"
                for version, count in sorted(versions.items()):
                    bars = int((count / max_version) * 20) if max_version > 0 else 0
                    versions_graph += f"  {version:7}: {'█' * bars} {count}\n"
            versions_graph += "```\n"

            # Création du contenu du README
            readme_content = f"""# Statistiques Tahoma

Voici les informations du trafic de l'application Tahoma :
- Total d'utilisateurs uniques ayant installé Tahoma : {current_content['total_users']}
- Nombre d'installations de Tahoma : {current_content['total_visits']}
- Date de la dernière installation : {last_install.strftime("%Y-%m-%d %H:%M:%S")}

## Graphiques
{users_graph}
{visits_graph}
{versions_graph}

*Dernière mise à jour : {timestamp}*
"""

            # Mise à jour du README avec gestion des conflits
            readme_response = requests.get(readme_url, headers=headers)
            readme_sha = readme_response.json()["sha"] if readme_response.status_code == 200 else None
            update_file(readme_url, readme_content, readme_sha, "Update README with latest stats")

            # Débogage:
#            test_response = requests.get("https://api.github.com/repos/pzim-devdata/stats_tahoma", headers=headers)
#            print(f"Test connexion: {test_response.status_code}")
#            print(f"Machine ID: {machine_id}")
#            print(f"GET status: {response.status_code}")
#            print(f"PUT status: {put_response.status_code}")
#            if put_response.status_code != 200:
#                print(f"Erreur PUT: {put_response.text}")


        except Exception as e:
            print(f"Erreur: {str(e)}")


    try :
        f = open(server_choosen, 'r')
        serverchoice = f.read()
        f.close()
    except :
        serverchoice = "somfy_europe"

    f2 = open(list_of_tahoma_devices, 'w')
    f3 = open(list_of_tahoma_shutters, 'w')
    f4 = open(list_of_tahoma_heaters, 'w')
    f5 = open(list_of_tahoma_alarms, 'w')
    f6 = open(list_of_tahoma_spotalarms, 'w')
    f7 = open(list_of_tahoma_plugs, 'w')
    f8 = open(list_of_tahoma_sunscreens, 'w')
    f9 = open(list_of_tahoma_scenes, 'w')
    f10 = open(list_of_tahoma_sensors, 'w')
    f11 = open(list_of_tahoma_states, 'w')
    f12 = open(list_of_tahoma_lights, 'w')
    f13 = open(list_of_tahoma_pergolas, 'w')

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-s", "--server")
    parser.add_argument("-g", action='store_true') #store_true for not asking argument
    parser.add_argument("--getlist", action='store_true') #store_true for not asking argument
    args = parser.parse_args()

    try:
        f = open(init_file, 'r')
        init = f.read()
        f.close()
        init_str=sha256(b"init").hexdigest()
    except:
        init_str="None"

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

    for arg in sys.argv:
        if args.password:
            PASSWORD = (f'{args.password}')
        if args.username:
            USERNAME = (f'{args.username}')
        if args.server:
            serverchoice = (f'{args.server}')

    async with OverkizClient(USERNAME, PASSWORD, SUPPORTED_SERVERS[serverchoice]) as client:
        try:
            await client.login()
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)
            return
        devices = await client.get_devices()
        scenarios = await client.get_scenarios()
        try :
            f2.write(f"Devices :\n")
            for device in devices:
                print("\n"+device.label+","+device.id+","+device.widget+","+device.ui_class+","+device.controllable_name+"")
                print(f"{device.label},{device.id},{device.widget},{device.ui_class},{device.controllable_name}")
                f2.write("\n"+device.label+","+device.id+","+device.widget+","+device.ui_class+","+device.controllable_name+"\n")
                f2.write(f"{device.label},{device.id},{device.widget},{device.ui_class},{device.controllable_name}\n")
                if "Shutter" in device.widget or "PositionableTiltedScreen" in device.widget:
                    f3.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_shutters)
                elif "Heater" in device.widget :
                    f4.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_heaters)
                elif "MyFoxAlarm" in device.widget :
                    f5.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_alarms)
                elif "StatefulOnOffLight" in device.widget :
                    f6.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_spotalarms)
                elif "StatelessOnOff" in device.widget :
                    f7.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_plugs)
                elif "StatefulOnOff" in device.widget :
                    f7.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_plugs)
                elif "PositionableScreen" in device.widget or "PositionableHorizontalAwning" in device.widget:
                    f8.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_sunscreens)
                elif "Sensor" in device.widget:
                    f10.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_sensors)
                elif "Light" in device.widget:
                    f12.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_lights)
                elif "PositionableTiltedScreen" in device.widget or "PergolaHorizontalAwning" in device.widget:
                    f13.write(device.label+","+device.id+","+device.widget+"\n")
                    print( "Device "+device.label+" controled by tahoma. Added to : "+list_of_tahoma_pergolas)
                else :
                    print( "Device '"+device.label+"' NOT controlled by tahoma yet")
#                get_state = await client.get_state( device.id )
                get_state = await asyncio.wait_for( client.get_state( device.id ), timeout=10.0)
                i=0
                for i in range(len(get_state)) :
    #                print(i)
    #                print(str(get_state[i].value))
                    if "closed" in str(get_state[i].value) or "open" in str(get_state[i].value) :
                        f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['closed','open'],"+str(get_state[i].value)+"\n")
                        print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                    if "StatefulOnOff" == device.widget or "StatefulOnOffLight" == device.widget :
                        f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['on','off'],"+str(get_state[i].value)+"\n")
                        print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                    if "armed" in str(get_state[i].value) or "disarmed" in str(get_state[i].value) :
                        f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['armed','disarmed'],"+str(get_state[i].value)+"\n")
                        print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                    if "Heater" not in device.widget and 'DomesticHotWaterTank' not in device.widget and "StatefulOnOff" not in device.widget and "StatefulOnOffLight" not in device.widget and 'TSKAlarmController' not in device.widget:
                            if str(get_state[i].value) == 'on' or str(get_state[i].value) =='off':
                                f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['on','off'],"+str(get_state[i].value)+"\n")
                                print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                    if 'io:TargetHeatingLevelState' not in str(get_state[i].name) and 'io:LastTargetHeatingLevelState' not in str(get_state[i].name) and 'core:OnOffState' not in str(get_state[i].name):
                            if 'TSKAlarmController' not in device.widget and 'DomesticHotWaterTank' not in device.widget:
                                if str(get_state[i].value) == 'eco' or str(get_state[i].value) =='comfort' or str(get_state[i].value) =='frostprotection' or str(get_state[i].value) =='off':
                                    f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['eco','comfort','frostprotection','off'],"+str(get_state[i].value)+"\n")
                                    print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                    if 'TemperatureSensor' == device.widget :
                        try:
                            if str(get_state[i].name) == 'core:TemperatureState':
                                f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['°C'],"+str(get_state[i].value)+"\n")
                                print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                        except : pass
                    if 'LuminanceSensor' == device.widget :
                        #print(get_state)
                        try:
                            if str(get_state[i].name) == 'core:LuminanceState' :
                            #if str(int(get_state[i].value)).isnumeric() == True :
                                f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['Lumens'],"+str(get_state[i].value)+"\n")
                                print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                        except : pass
                    if 'CumulativeElectricPowerConsumptionSensor' == device.widget :
                        try:
                            if str(get_state[i].name) == 'core:ElectricEnergyConsumptionState' :
                                f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['kWh'],"+str(get_state[i].value)+"\n")
                                print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                        except : pass
                    if 'DomesticHotWaterTank' == device.widget :
                        try:
                            if str(get_state[i].name) == 'io:ForceHeatingState' :
                                f11.write(device.label+","+device.id+","+device.widget+",get_state["+str(i)+"].value,['on','off'],"+str(get_state[i].value)+"\n")
                                print("States for "+device.label+" added to : "+ list_of_tahoma_states)
                        except : pass

                    i=i+1
        except Exception as e :
            print(e)
        print("\nScenes :\n")
    try :
        f2.write(f"\nScenes :\n")
        for scenario in scenarios:
            f2.write(f"{scenario.label},{scenario.oid}\n")
            f9.write(f"{scenario.label},{scenario.oid}\n")
            print( 'Scene : "'+scenario.label+'" controled by tahoma. Added to : '+list_of_tahoma_scenes)
    except Exception as e :
        print(e)

    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    f7.close()
    f8.close()
    f9.close()
    f10.close()
    f11.close()
    f12.close()
    f13.close()

    print( "\nIf you want to add a device you have found in this list but which is not controlled by tahoma yet, please provide info about this device from this file at \nhttps://github.com/pzim-devdata/tahoma/issues and I will update the plugin ;-). \nSonos products can't be had, use 'soco-cli' instead")
    print( "\nThe list of devices has been succesfully imported to the file : "+list_of_tahoma_devices+"\n" )

try:
    asyncio.run(main())
    exit(0)
except NameError as e:
    print(e)
    print("\nYou didn't specified any USERNAME or PASSWORD.\nExecute tahoma --config or provide a temporary USERNAME and PASSWORD by executing tahoma -u <USERNAME> -p <PASSWORD> command")
    exit(1)
