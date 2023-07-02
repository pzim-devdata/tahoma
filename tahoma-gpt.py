#!/usr/bin/python3
#MIT licence
#@pzim-devdata
#https://github.com/openai/openai-python
#https://github.com/pzim-devdata/tahoma#add-chatgpt-functionalities-
#python3 -m pip install --upgrade openai
#python3 -m pip install openai[embeddings]
#python3 -m pip install openai[wandb]
#python3 -m pip install openai[datalib] 


##############################################################################
###You can create a vitual environnement in Python if you want to test it first. All will be installed in the tahoma-gpt directory
#Create a directory with tahoma-gpt.py and requirements_tahoma-gpt.txt inside from there : https://github.com/pzim-devdata/tahoma
#Open a terminal
#cd in this directory
#Run : python3 -m venv env
#Run : source env/bin/activate
#
#Install tahoma and configure it (if it's not already done) :
##Run : python3 -m pip install -U tahoma
##Configure tahoma : tahoma -c
##Get the list of your devices : tahoma -g
#
#Run : python3 -m pip install -r requirements_tahoma-gpt.txt
#Modify this script to add OpenAI API key
#Run : python3 tahoma-gpt.py
#Play with tahoma and ChatGPT
#Run : deactivate
##############################################################################

import openai
import datetime
import os
import requests
import subprocess
import asyncio
import pyoverkiz
import time
try:
    from inputimeout import inputimeout, TimeoutOccurred
except:pass
import sys


openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
models=['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-16k']

model = models[4]

#arguments
args = sys.argv

def search(filename_to_find):
    # Répertoire d'exécution du script
    try:
        script_directory = os.path.dirname(os.path.realpath(__file__))
    except:
        script_directory = os.path.dirname(os.path.realpath(__name__))
    # Fonction récursive pour rechercher le fichier dans les répertoires
    def search_directory_for_file(directory, filename):
        for root, dirs, files in os.walk(directory):
            if filename in files:
                file_path = os.path.join(root, filename)
                return file_path
        return None  
    file_path = search_directory_for_file(script_directory, filename_to_find)
    if file_path:
        folder_path = os.path.dirname(file_path)
        #print("Le fichier", filename_to_find, "a été trouvé dans le dossier :", folder_path)
    else:
        print("Le fichier", filename_to_find, "n'a pas été trouvé dans les répertoires.")    
    return file_path

#folder_path=search('tahoma.py')

temp=search('temp')
try:
    names = subprocess.check_output(search('tahoma') + " -ln", shell=True)
    names = names.decode('utf-8')
    index_exclusion = names.find("You must provide a part of the NAME as argument")
    if index_exclusion != -1:
        names = names[:index_exclusion]
        names = "Here " + names.split("Here", 1)[-1].strip()
        start_index = names.index("Here is the list of the installed devices for the SUNSCREEN category")
        names1 = names[:start_index]
        names2 = names[start_index:]
except:
    names = subprocess.check_output("python3 '" + search('tahoma.py') + "' -ln", shell=True)
    names = names.decode('utf-8')
    index_exclusion = names.find("You must provide a part of the NAME as argument")
    if index_exclusion != -1:
        names = names[:index_exclusion]
        names = "Here " + names.split("Here", 1)[-1].strip()

try:
    actions = subprocess.check_output(search('tahoma') + " -la", shell=True)
    actions = actions.decode('utf-8')
except:
    actions = subprocess.check_output("python3 '" + search('tahoma.py') + "' -la", shell=True)
    actions = actions.decode('utf-8')

try:
    categories = subprocess.check_output(search('tahoma') + " -lc", shell=True)
    categories = categories.decode('utf-8')
except:
    categories = subprocess.check_output("python3 '" + search('tahoma.py') + "' -lc", shell=True)
    categories = categories.decode('utf-8')

def main(model):
    async def create_chat_completion(prompt):
#        chat_completion_resp = await openai.ChatCompletion.acreate(
        chat_completion_resp = await openai.ChatCompletion.acreate(
    #        model="gpt-3.5-turbo",
            model=model,
            messages=[
                {"role": "system", "content": """Here is the user manual for the Tahoma application, including the various commands it contains. Your task is to display the correct command to help me use this application or execute an instance of Tahoma using the syntax: 'command:' For example: 'command: tahoma ACTION CATEGORY ["EXACT NAME"]' based on what I ask you."""},
                {"role": "system", "content": "Here is part 1/2 of the list of equipment NAMES present in the house for each category. You will base your answers on these exact names. WARNING: DO NOT TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES: " + str(names1)},
                {"role": "system", "content": "Here is part 2/2 of the list of equipment NAMES present in the house for each category. You will base your answers on these exact names. WARNING: DO NOT TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES: " + str(names2)},
                {"role": "system", "content": "Here is the list of possible ACTIONS for the equipment present in the house for each category. You will base your answers on these actions. WARNING: DO NOT TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES: " + str(actions)},
                {"role": "system", "content": "Here is the list of possible CATEGORIES for the equipment present in the house. You will base your answers on these categories. WARNING: DO NOT TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES: " + str(categories)},
                {"role": "system", "content": "Tahoma allows you to control the equipment in the house from the Somfy brand."},
                {"role": "system", "content": "Description of Tahoma: Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch. Features: Control Somfy Tahoma devices with a simple API written in Python 3, Create scripts or shortcuts to control your house from a domestic server or your computer, With this API, you can integrate Somfy's products with other Matter-compatible devices, Works with Somfy Connectivity Kit, Connexoon, Cozytouch, and more, Support various Somfy's devices: alarm, shutter, plug, heater, sensors, scenes, and more, Compatible with Windows and Linux operating systems."},
                {"role": "system", "content": "The responses will be limited to the instructions I provide. If a request is not related to the Tahoma application or the instructions I give you, you will respond that your domain of expertise is limited to providing information about this application or controlling Somfy devices."},
                {"role": "system", "content": "There are just two commands to execute once to configure Tahoma: Specify your Somfy-connect login information and choose the Somfy server: python3 tahoma.py --configure or python3 tahoma.py -c Retrieve the list of your personal Somfy devices: python3 tahoma.py --getlist or python3 tahoma.py -g"},
                {"role": "system", "content": """When there are multiple commands to execute, you should launch only one instance of Tahoma with the commands listed one after another without opening a new instance of Tahoma. For example, to set the heating in the kitchen and the living room, you need to execute two commands in a single instance of Tahoma: tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]"""},
                {"role": "system", "content": """It is imperative to use brackets followed by quotes to define the ["EXACT NAME"] because sometimes there are multiple identical NAMES. For example, it is preferable to use the command tahoma open shutter ["EXACT NAME"] rather than tahoma open shutter PART_OF_A_NAME."""},
                {"role": "system", "content": """In the case of using sensors, you can omit the brackets and quotes if you want to retrieve the status of multiple sensors at the same time that have a common part of the NAME. For this, the sensors must have a common NAME among them. For example, if I have sensors that all contain the word 'blabla' in their EXACT NAME and I want to get the status of these sensors at the same time, I would not use the syntax: tahoma get sensor COMMON_PART. However, if I want the state of a specific sensor, I will necessarily use brackets and quotes. For example: tahoma get sensor ["EXACT NAME"]."""},
                {"role": "system", "content": """In the case of using sensors, you can also use the ACTION 'get_state' instead of 'get'. In that case, the syntax is: 'tahoma get_state sensor ["EXACT NAME"]' """},
                {"role": "system", "content": """For your information, the list of ["EXACT NAME"] is the result of the command 'tahoma -ln'."""},
                {"role": "system", "content": "For your information, the list of ACTIONS is the result of the command 'tahoma -la'."},
                {"role": "system", "content": "For your information, the list of CATEGORIES is the result of the command 'tahoma -lc'."},
                {"role": "system", "content": """If I ask you to execute a specific command, you will write the command to be executed preceded by the word 'command:'. For example: 'command: tahoma ACTION CATEGORY ["EXACT NAME"]'. The word 'command' in the syntax 'command:' should never be translated."""},
                {"role": "system", "content": "If I ask you to execute a command, your response should only contain the syntax 'command:' followed by the command to be executed and nothing else. You should not provide any other response than this specific syntax. We should not mix responses that require an explanation and responses that require the usage of the syntax: command: + the command to be executed."},
                {"role": "system", "content": """If I ask you to open the shutters in the kitchen, you will look for the CATEGORY that corresponds to the shutters (result of tahoma -lc), then you will look for the NAME of the kitchen shutters in the shutters CATEGORY (result of tahoma -ln), then you will look for the ACTION that corresponds to opening for the shutter CATEGORY (result of the command tahoma -la), and finally you will display the correct command with 'command: ' followed by tahoma ACTION CATEGORY ["EXACT NAME"]."""},
                {"role": "system", "content": "When writing a command, you should never translate the ACTIONS, CATEGORIES, or NAMES as they are unique references."},
                {"role": "system", "content": """Each command consists of three parameters (ACTION, CATEGORY, ["EXACT NAME"]). You should always check if the requested ACTION exists in the instructions and if the NAME is correct by consulting the result of the command tahoma -ln, which is also provided in the instructions. You should do the same to verify that the CATEGORY exists, which is the result of tahoma -lc, also present in your instructions."""},
                {"role": "system", "content": "If my request does not require executing a command, you will not display 'command:'."},
                {"role": "system", "content": """The syntax of a command is 'ACTION CATEGORY ["EXACT NAME"]'. The syntax of an instance of Tahoma is: 'tahoma' followed by the number of required commands."""},
                {"role": "system", "content": """To execute multiple commands in succession within the same instance of Tahoma, the syntax is as follows: tahoma ACTION CATEGORY NAME ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]... and you repeat this for the number of necessary commands."""},
                {"role": "system", "content": """There is no ["ALL"] NAME, so to execute an instance of Tahoma that performs an ACTION for all the NAMES of the same CATEGORY, you need to create an instance of Tahoma followed by the number of commands of the type ACTION CATEGORY ["EXACT NAME"] corresponding to the number of equipment in a CATEGORY."""},
                {"role": "system", "content": """There are two types of Somfy devices: devices equipped with IO technology (with feedback) and RTS devices without feedback. That's why you cannot ask an RTS device to close at 25% because it doesn't have the information about its state. You also cannot execute the 'stop' command with RTS devices. The only way to stop an RTS device is to cancel its previous command. For example, if I want to stop an RTS shutter 10 seconds after asking it to open, I would need to execute in the same instance of Tahoma: tahoma ACTION CATEGORY ["EXACT NAME"] sleep for 10 cancel last action. That's why it can be useful to ask if a shutter is RTS or IO in order to execute either the 'stop' ACTION or the 'cancel last action' command."""},
                {"role": "system", "content": """The only way to stop an RTS device is to cancel its previous command. For example, if I want to stop an RTS shutter 10 seconds after asking it to open, I would need to execute in the same instance of Tahoma: tahoma ACTION CATEGORY ["EXACT NAME"] sleep for 10 cancel last action. That's why it can be useful to ask if a shutter is RTS or IO in order to execute either the 'stop' ACTION or the 'cancel last action' command."""},
                {"role": "system", "content": """Here is an example of a single instance of Tahoma: tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]. This will execute the three actions in the specified order."""},
                {"role": "system", "content": """WARNING: NEVER TRANSLATE OR MODIFY THE NAME, ACTION NAMES, OR CATEGORY NAMES IN YOUR RESPONSES, AND PROVIDE THE FULL NAME, NOT JUST A PART OF THE NAME, USING THE SYNTAX ["NAME"]"""},
                {"role": "system", "content": """When it is stated that it is an EXAMPLE in the instructions, it means that these examples do not reflect the actual names of the equipment in the installation, so you should not use these EXAMPLES to write an instance of Tahoma or a command."""},
                {"role": "system", "content": """Regarding the shutter or sunscreen CATEGORY, the ACTION "MY" refers to a position saved in memory by the user. It is not the same ACTION as NUMBER, which allows entering a number from 0 to 100 to set any position on IO equipment. For example, the command "NUMBER shutter ["EXACT NAME"]" will close the shutter at NUMBER% in a Tahoma instance."""},
                {"role": "system", "content": """To close a shutter or curtain to a specific position, you should use the command "NUMBER" followed by the desired closing percentage. For example, to close a shutter at 50%, the command would be: tahoma 50 shutter ["EXACT NAME"]. It is important to note that this command only works for IO equipment."""},
                {"role": "system", "content": """To wait between two commands, you can use the "wait for SECONDS" command, which sets a delay in seconds before executing the next action. For example, if I want to open the shutters and close them after 10 seconds, I would use the following command in the Tahoma instance: tahoma open shutter ["EXACT NAME"] wait for 10 close shutter ["EXACT NAME"]. This is the command for waiting."""},
                {"role": "system", "content": """The "wait for" command has 3 arguments like any other command: "wait for SECONDS". It sets a delay in seconds between two actions executed in the same instance of Tahoma. For example, if I want to open the shutters and close them after 5 seconds, I would use the following command: 'tahoma open shutter ["EXACT NAME"] wait for 5 close shutter ["EXACT NAME"]'"""},
                {"role": "system", "content": """I can help you if you need clarification. Do not invent instances or commands."""},
                {"role": "system", "content": """It is important not to mix explanations of a command and commands to be executed ('command:'). The response should either be an explanation or a command."""},
                {"role": "system", "content": """A command is defined by using 3 parameters: ACTION, CATEGORY, ["EXACT NAME"]. An instance of Tahoma is defined as using one or more commands. For example, this is an instance of Tahoma containing three commands: 'tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]'"""},
                {"role": "system", "content": """Sensors are the only equipment that can use a UNIQUE_NAME that is not enclosed in brackets and quotes: [""]. This is useful if you want to obtain the status of different sensors that have an identical word in their EXACT_NAME in a single command. In this case, the syntax of the command is 'get sensor COMMON_NAME'. For example, if I have sensors named "blabla 1", "blabla 2", and "blabla 3", and I want to know their status in a single command, I would use this Tahoma instance: tahoma get sensor blabla."""},
                {"role": "system", "content": """Each command has 3 arguments. Never more or less. So an instance of Tahoma must contain multiples of 3 arguments (ACTION CATEGORY ["EXACT NAME"]) preceded by the word 'tahoma'. There is no command that is not composed of 3 arguments. For example, if an instance of Tahoma has 3 commands, there will be 9 arguments following the word 'tahoma': (3 commands * 3 arguments per command)"""},
                {"role": "system", "content": """Very important: If you do not know how to execute a command, do not hesitate to ask for help or confirmation before launching a Tahoma instance with the syntax 'command: ' to avoid executing incorrect actions. It can have serious consequences if the wrong command is executed with the 'command: ' syntax."""},
                {"role": "system", "content": """To obtain the state of a heater, you need to use the sensor CATEGORY using the syntax: 'tahoma get sensor heater ["EXACT HEATER NAME"]'. The 'get_state' CATEGORY does not exist."""},
                {"role": "system", "content": """Your name is tahoma-gpt and your role is to display the correct command based on what I'm going to ask you to help me use this Tahoma application."""},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion_resp
#
    async def chat_loop():
        if len(args) > 1 and sys.argv[1] != "":
            user_input = ' '.join(args[1:])
            response = await create_chat_completion(user_input)
            command = response['choices'][0]['message']['content']
            # Vérifie si la commande est "Command: echo 'Hello world'"
            if "command: tahoma" in command.lower():
                # Exécute la commande en utilisant subprocess
                print("\nExecuting command:", command.replace('command: ',''))
                try:
                    try:
                        output = subprocess.check_output(""+search('tahoma') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                        #print(response['choices'][0]['message']['content'])
                        print("Command result:", output.decode())
                        response = await create_chat_completion(str(output.decode()))
                        assistant_response = response['choices'][0]['message']['content']
                    except:
                        output = subprocess.check_output("python3 "+search('tahoma.py') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                        print("Incorrect command: tahoma", output.decode())
                        response = await create_chat_completion(str(output.decode()))
                        assistant_response = response['choices'][0]['message']['content']
                except Exception as e:
                    print(e)
                    response = await create_chat_completion(str(e))
                    assistant_response = response['choices'][0]['message']['content']
            else:
                # Affiche la réponse de ChatGPT
                assistant_response = response['choices'][0]['message']['content']
                print("\n\033[1mAssistant:\033[0m ", assistant_response)
            time.sleep(5)
            exit()
        else:
            pass
        print("")
        try:
            choix = inputimeout(prompt="Would you like to load an advanced configuration of Tahoma-GPT for practice? (Y/n) ", timeout=4).lower()
#            choix = choix.lower()
            if choix in ["y", "yes", "o", "oui"]:
                try:
                    print("Loading advanced configuration...")
                    print("")
                    print("Please wait, Tahoma-gpt is loading and analyzing your configuration...")
                    print("Tahoma-gpt may crash the first time you start it. It's normal, Just restart tahoma-gpt in this case.")
                    print("")
                    user_input = "\nI have provided you with new instructions. Have you taken these new instructions into account?"
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("1/6 : ok")
                except :
                    print("1/6 : non ok")
                try:
                    user_input = """\nCan you incorporate this information as succinctly as possible to make better use of it? WARNING: NEVER TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES. Here is the first list (1/2) of EXACT NAMES: """ + str(names1) + """. This information will help you formulate Tahoma commands with the syntax tahoma ACTION CATEGORY ["EXACT NAME"]."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("2/6 : ok")
                except:
                    print("2/6 : non ok")
                try:
                    user_input = """\nCan you incorporate this information as succinctly as possible to make better use of it? WARNING: NEVER TRANSLATE OR MODIFY THESE NAMES IN YOUR RESPONSES. Here is the second list (2/2) of EXACT NAMES: """ + str(names2) + """. This information will help you formulate Tahoma commands with the syntax tahoma ACTION CATEGORY ["EXACT NAME"]."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("3/6 : ok")
                except:
                    print("3/6 : non ok")
                try:
                    user_input = """\nCan you incorporate this information as succinctly as possible to make better use of it? WARNING: NEVER TRANSLATE OR MODIFY THE NAME, ACTION NAMES, AND CATEGORY NAMES IN YOUR RESPONSES, AND PROVIDE THE ENTIRE NAME, NOT JUST A PART OF THE NAME, IN THE SYNTAX ["EXACT NAME"]. Here is the list of actual ACTIONS: """ + str(actions) + """. This information will help you formulate Tahoma commands with the syntax tahoma ACTION CATEGORY ["EXACT NAME"]."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("4/6 : ok")
                except:
                    print("4/6 : non ok")
                try:
                    user_input = """\nCan you, according to your instructions, from the two lists of names (1/2) and (2/2), present me with the complete list of names by categories, and then the complete list of actions by categories? WARNING: NEVER TRANSLATE OR MODIFY THE EXACT NAMES, ACTION NAMES, AND CATEGORY NAMES IN YOUR RESPONSES, AND PROVIDE THE "EXACT NAME" IN ITS ENTIRETY, NOT JUST A PART OF THE NAME, IN THE SYNTAX ["EXACT NAME"]. You will respond to me without an introduction phrase and without a polite concluding phrase, but by presenting it as a general instruction presentation."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("5/6 : ok")
                    print("\n\033[1mLIST OF DEVICES\033[0m \n", assistant_response)
                except:
                    print("5/6 : non ok")
                try:
                    user_input = """\nCan you, according to your instructions, explain as succinctly as possible the syntax to use, making sure to specify that for the NAME you need brackets, quotes, and the EXACT NAME between the two quotes: ["EXACT NAME"]? Can you also tell me very briefly why, for RTS equipment, regarding the stop ACTION, we need to use the 'cancel last action' command? Can you also tell me how to close a shutter or curtain at a specific position? Can you explain why sometimes, just for the CATEGORY sensors, it's better not to use ["EXACT NAME"] but a PART_NAME ? WARNING: NEVER TRANSLATE OR MODIFY THE ["EXACT NAME"], ACTION NAMES, AND CATEGORY NAMES IN YOUR RESPONSES, AND PROVIDE THE EXACT NAMES, NOT JUST A PART OF THE NAME, IN THE SYNTAX ["EXACT NAME"]. Use examples with the exats names of my devices configuration using brackets and quotation marks. You will respond to me without an introduction phrase and without a polite concluding phrase, but by presenting it as a general instruction presentation."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("6/6 : ok")
                    print("\n\033[1mGENERAL INSTRUCTIONS\033[0m \n", assistant_response)
                except:
                    print("6/6 : non ok")
                try:
                    user_input = "\nCan you, according to your instructions, quickly explain the use of the 'wait for' command and the need to formulate commands within the same Tahoma instance? Please provide concise and understandable answers. Respond without any introductory or concluding polite phrases, but present it as a general instruction presentation. Use examples with the REAL names of my devices configuration using brackets and quotation marks. Also, let me know that YOU CAN execute commands if I ask you to but don't explain how you do this."
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("")
                    print(assistant_response)
                except:
                    print("")
            else:
                print("Loading default configuration...")
#        except TimeoutOccurred:
#            print("Timeout atteint. Chargement de la configuration par défaut.")
        except: pass
        assistant_response = "\nWelcome to your Tahoma usage assistance service. I am tahoma-gpt. \nThe intelligence model used is: " + model + ".\nI can help you to create commands for Tahoma and also execute them if you ask me to.\nYou can exit at any time by typing 'exit'."
        print("\n\033[1mAssistant:\033[0m ", assistant_response)
        while True:
            # Demande à l'utilisateur d'entrer une phrase d'instruction
            user_input = input("\n\033[1mInstruction:\033[0m ")
            # Si l'utilisateur entre "exit", le script se termine
            if user_input.lower() == "exit":
                print("Au revoir !")
                break
            # Appelle la fonction create_chat_completion() avec la phrase d'instruction de l'utilisateur
            response = await create_chat_completion(user_input)
            # Vérifie si une commande système a été renvoyée
            if response['choices'][0]['message']['role'] == 'assistant':
                command = response['choices'][0]['message']['content']
                # Vérifie si la commande est "Command: echo 'Hello world'"
                if "command: tahoma" in command.lower():
                    # Exécute la commande en utilisant subprocess
                    print("\nExecuting command:", command.replace('command: ',''))
                    try:
                        try:
                            output = subprocess.check_output(""+search('tahoma') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                            #print(response['choices'][0]['message']['content'])
                            print("Command result:", output.decode())
                            response = await create_chat_completion(str(output.decode()))
                            assistant_response = response['choices'][0]['message']['content']
                        except:
                            output = subprocess.check_output("python3 "+search('tahoma.py') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                            print("Incorrect command: tahoma", output.decode())
                            response = await create_chat_completion(str(output.decode()))
                            assistant_response = response['choices'][0]['message']['content']
                    except Exception as e:
                        print(e)
                        response = await create_chat_completion(str(e))
                        assistant_response = response['choices'][0]['message']['content']
                else:
                    # Affiche la réponse de ChatGPT
                    assistant_response = response['choices'][0]['message']['content']
                    print("\n\033[1mAssistant:\033[0m ", assistant_response)
# Exécute la boucle de chat de manière asynchrone
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chat_loop())

main(model)

