#!/usr/bin/python3
#sudo python3 -m pip install pyoverkiz
#sudo python3 -m pip install tahoma-pzim -U
#tahoma.py by @pzim-devdata
#MIT Licence

import asyncio
import sys
import argparse
import os
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
    str_newrelic='New installation of the tahoma Github version'
except:
    from tahoma import __version__
    str_newrelic='New installation of the tahoma Pypi version'


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
        try:
            import configparser
            import newrelic.agent
            license_key="eu01xxa5bf9b857655fdc4fa8e6eba17FFFFNRAL"
            config_file_newrelic = os.path.dirname(os.path.abspath(__file__))+'/temp/newrelic.ini'
            def send_statistics(license_key=license_key,config_file_newrelic=config_file_newrelic):
                config = configparser.ConfigParser()
                config["newrelic"] = {
                    "license_key": license_key,
                    "app_name": "tahoma_pypi",
                    "monitor_mode" : "true",
                    "log_file" : "stdout",
                    "log_level" : "critical",
                    "high_security" : "false"
                }
                with open(config_file_newrelic, "w") as f:
                    config.write(f)
                f.close()
                newrelic.agent.initialize(config_file_newrelic)
                application = newrelic.agent.register_application(timeout=10)
                with newrelic.agent.BackgroundTask(application, name='bar', group='Task'):
                     newrelic.agent.record_log_event(str(str_newrelic))
                newrelic.agent.shutdown_agent(timeout=10)
            send_statistics()
        except: pass

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

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
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
                else :
                    print( "Device '"+device.label+"' NOT controlled by tahoma yet")
                get_state = await client.get_state( device.id )
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

    print( "\nIf you want to add a device you have found in this list but which is not controlled by tahoma yet, please provide info about this device from this file at \nhttps://github.com/pzim-devdata/tahoma/issues and I will update the plugin ;-). \nSonos products can't be had, use 'soco-cli' instead")
    print( "\nThe list of devices has been succesfully imported to the file : "+list_of_tahoma_devices+"\n" )

try:
    asyncio.run(main())
    exit(0)
except NameError as e:
    print(e)
    print("\nYou didn't specified any USERNAME or PASSWORD.\nExecute tahoma --config or provide a temporary USERNAME and PASSWORD by executing tahoma -u <USERNAME> -p <PASSWORD> command")
    exit(1)
