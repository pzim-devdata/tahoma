#!/usr/bin/python3
#https://github.com/openai/openai-python

#cd ~/Bureau/OpenAI
#python3 -m venv env
#source env/bin/activate
#python3 -m pip install --upgrade openai
#python3 -m pip install openai[embeddings]
#python3 -m pip install openai[wandb]
#python3 -m pip install openai[datalib] 
#deactivate

import openai
import datetime
import os
import requests
import subprocess
import asyncio
import pyoverkiz

openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxx"
models=['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-16k']


model = models[4]

def search(filename_to_find):
    # Fonction récursive pour rechercher le fichier dans les répertoires
    def search_directory_for_file(directory, filename):
        for root, dirs, files in os.walk(directory):
            if filename in files or (filename in dirs and root.endswith('tahoma')):
                file_path = os.path.join(root, filename)
                folder_path = os.path.dirname(file_path)
                return folder_path
        return None
    if os.name == 'posix':  # Linux, macOS
        root_directories = ['/']
        separator = '/'
    elif os.name == 'nt':  # Windows
        root_directories = [f'{d}:' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        separator = '\\'
    else:
        print("Système d'exploitation non pris en charge.")
        return
    found = False
    for root_directory in root_directories:
        result = search_directory_for_file(root_directory, filename_to_find)
        if result:
            folder_path = os.path.join(result, filename_to_find)
            #print("Le fichier ou répertoire", filename_to_find, "a été trouvé dans le dossier :", folder_path)
            found = True
            break
    if not found:
        print("Le fichier ou répertoire", filename_to_find, "n'a pas été trouvé dans les répertoires.")
    return folder_path

#folder_path=search('tahoma.py')

temp=search('temp')
try:
    names = subprocess.check_output(search('tahoma') + " -ln", shell=True)
except:
    names = subprocess.check_output("python3 " + search('tahoma.py') + " -ln", shell=True)

try:
    actions = subprocess.check_output(search('tahoma') + " -la", shell=True)
except:
    actions = subprocess.check_output("python3 " + search('tahoma.py') + " -la", shell=True)

try:
    categories = subprocess.check_output(search('tahoma') + " -lc", shell=True)
except:
    categories = subprocess.check_output("python3 " + search('tahoma.pc') + " -ln", shell=True)

def main(model):
    async def create_chat_completion(prompt):
#        chat_completion_resp = await openai.ChatCompletion.acreate(
        chat_completion_resp = await openai.ChatCompletion.acreate(
    #        model="gpt-3.5-turbo",
            model=model,
            messages=[
                {"role": "system", "content": "Voici le mode d'emploi de l'application tahoma avec les différentes commandes qu'elle contient. Ton travail consiste à afficher la bonne commande en fonction de ce que je vais te demander pour m'aider à utiliser cette application"},
                {"role": "system", "content": "Domaine d'application: tahoma permet de controler les équipements de la maison de la marque Somfy"},
                {"role": "system", "content": "Descriptif de tahoma: Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch. Features: Control Somfy Tahoma devices with a simple API written in Python 3, Create scripts or shortcuts to control your house from a domestic server or your computer, With this API, you can integrate Somfy's products with other Matter-compatible devices, Works with Somfy Connectivity Kit, Connexoon, Cozytouch, and more, Support various Somfy's devices: alarm, shutter, plug, heater, sensors, scenes, and more, Compatible with Windows and Linux operating systems"},
                {"role": "system", "content": "Tes réponses se cantonneront aux instructions que je vais te fournir. Si une demande ne concerne pas cette application tahoma ou les instructions que je te fourni, tu répondras que ton domaine d'exercice est limité à la fourniture d'informations au sujet de cette application ou à contrôler les équipements Somfy"},
                {"role": "system", "content": "Retrieve your PERSONAL commands :USAGE EXAMPLE: python3 tahoma.py [ACTION] [CATEGORY] [NAME] For EXAMPLE : tahoma open shutter kitchen or tahoma ouvrir volet cuisine To retrieve your personal commands, you can use the following options:List all possible [ACTIONS] for each [CATEGORIES]: python3 tahoma.py -la or python3 tahoma.py --list-actions or tahoma -la or python3 tahoma.py --list-actions-french or tahoma -laf List available [CATEGORIES]:python3 tahoma.py --list-categories or tahoma -lc or python3 tahoma.py --list-categories-french or tahoma -lcf Retrieve the [NAMES] you have assigned to your personal devices in the Somfy's App: python3 tahoma.py --list-names or tahoma -ln or python3 tahoma.py --list-names-french or tahoma -lnf"},
                {"role": "system", "content": "There are just two commands to execute once to configure Tahoma:Specify your Somfy-connect login information and choose the Somfy server: : python3 tahoma.py --configure or python3 tahoma.py -c Retrieve the list of your personal Somfy devices: : python3 tahoma.py --getlist or python3 tahoma.py -g"},
                {"role": "system", "content": "Use Cases:Usage: python3 tahoma.py [ACTION] [CATEGORY] [NAME] For EXAMPLE : tahoma open shutter kitchen or tahoma ouvrir volet cuisine You can specify the closing level for shutters or sunscreens with a numeric value as ACTION.For instance, to close a shutter or a sunsceen to 25% :tahoma 25 shutter kitchen tahoma 25 sunscreen kitchen.Please note that this feature only works with IO protocols and not with RTS. You can use either a unique word : bath or the full name of a device in square brackets [''] : ['bath 1st floor']) as the NAME parameter.For EXAMPLE :tahoma open shutter garden tahoma arm alarm ['garden door'] Multiple commands can be executed in the same process without restarting Tahoma.For EXAMPLE :tahoma arm alarm garden open shutter ['room 6'] confort heater dining off plug office 25 sunscreen kitchen launch scene morning There is also a wait functionality with wait for or sleep for or attendre pendant :For EXAMPLE :tahoma open shutter kitchen wait for 20 close shutter kitchen Since it is impossible to stop an RTS device, there is the possibility to cancel the immediate preceding command (without affecting a 'wait for ' command). To do this you can use the command 'cancel last action' or 'annuler precedente commande' just after a command that opens or closes an RTS device.For EXAMPLE :tahoma open shutter kitchen wait for 2 cancel last action : It will stop the kitchen shutter after 2 seconds tahoma open shutter kitchen open shutter room6 cancel last action : It will only stop the room6 shutter"},
                {"role": "system", "content": 'Lorsqu il y a deux ou plus de commandes à executer, il ne faut lancer qu une seule instance de tahoma avec les commandes qui se suivent à la suite sans ouvrir une nouvelle instance de tahoma. Par exemple pour mettre le chauffage dans la cuisine et le salon, il faudra executer cette commande : tahoma comfort heater ["Cuisine"] comfort heater ["Salon"]'},
                {"role": "system", "content": 'Il est préférable d utiliser les brakets suivis de guillemets pour définir le NAME car des fois il y a plusieurs NAMES identiques. Par exemple il préférable d utiliser la commande tahoma open shutter ["Cuisine"] plutôt que tahoma open shutter cuisine'},
                {"role": "system", "content": """Dans le cas d usage des sensors, il est possible de ne pas utiliser les brakets suivi de guillemets si par exemple on veut récupérer l état de plusieurs capteurs en même temps avec une seule commande. Pour cela il faut que les capteur aient un NOM en commun entre eux. Par exemple si j ai des capteurs qui contiennent tous le NOM porte et que je veux avoir l état des capteurs de porte en même temps, je ne vais pas utiliser de brakets suivi de guillemets : tahoma get sensor porte. Par contre si je veux l état d un capteur spécifique je vais forcement utiliser les brakets et les guillemets. Par exemple : tahoma get sensor ["Porte d'entrée"]"""},
                {"role": "system", "content": "Examples :Here are some EXAMPLE commands : tahoma open shutter kitchen, tahoma 25 shutter Velux3 (Closes the shutter to 25%), tahoma get sensor ['Luminance sensor garden'] (You can use the full name of the device with ['<NAME>'] ), tahoma get sensor door (Provides information about all sensors named 'door' in the house), tahoma get sensor ['Front door'], tahoma on plug office, tahoma open shutter ['room 6'], tahoma arm alarm garden, tahoma comfort heater dining, tahoma get sensor ['heater dining room'], tahoma launch scene morning, tahoma arm alarm garden wait for 10 open shutter room6 sleep for 7 confort heater dining off plug office 25 sunscreen kitchen launch scene morning get sensor ['heater dining room'], tahoma comfort heater dining wait for 3 get sensor ['Heater dining room'], tahoma open shutter kitchen open shutter room6 wait for 2 cancel last action` (It will stop the room6 shutter after 2 seconds)"},
                {"role": "system", "content": "Pour information, la liste des NAME est le résultat de la commande tahoma -ln" },
                {"role": "system", "content": "Pour information, la liste des ACTIONS est le résultat de la commande tahoma -la"},
                {"role": "system", "content": "Pour information, la liste des CATEGORIES est le résultat de la commande tahoma -lc" },
                {"role": "system", "content": "Si je te demande d’exécuter une commande spécifique tu rédigeras la commande à executer precedée du mot `command: `Par exemple si je te demande d'ouvrir les volets de la cuisine, tu chercheras le NAME de cuisine (résultat de tahoma -ln) et tu m'afficheras mot pour mot: `command: tahoma open shutter cuisine`. Il ne faut jamais traduire la syntaxe `command: `."},
                {"role": "system", "content": "Si je te demande d'executer une commande, il est imperatif que ta réponse ne contienne que la syntaxe command: puis la commande à executer et rien d'autre. Tu ne formuleras pas d'autre réponse que cette syntaxe bien précise. On ne mélange pas les réponses qui necessitent une explication et les réponses qui necessitent l'usage de la syntaxe : command: + la ommande à executer"}, 
                {"role": "system", "content": "Par exemple, si je te demande d'ouvrir les volets de la cuisine, tu devras dans un premier temps récupérer le NOM de l'équipement qui contient le mot cuisine qui se trouve dans le résultat de la commande tahoma -ln que je t'ai fourni dans les instructions et afficher en guise de reponse : 'command: tahoma open shutter cuisine'"},
                {"role": "system", "content": 'Par exemple,si je te demande d ouvrir les volets de la cuisine, tu chercheras tu chercheras la CATEGORY qui correspond aux volets (résultat de tahoma -lc) puis tu chercheras le NAME des volets de la cuisine dans la CATEGORY des volets (résultat de tahoma -ln) puis tu chercheras l ACTION qui correspond à ouvrir pour la CATEGORY volet (résultat de la commande tahoma -la) et enfin tu m afficheras la commande suivante : command: tahoma open shutter ["Volet Cuisine"]'},
                {"role": "system", "content": "Lors de la rédaction d'une commande il ne faut jamais traduire les ACTION, les CATEGORY ou les NOM car ce sont des références uniques"},
                {"role": "system", "content": "Chaque commande contient trois paramètres (ACTION, CATEGORY, NAME). Il faut toujours vérifier si l'ACTION demandée existe dans le résultat de 'tahoma -la' présent dans les instructions et si le NOM est correct en consultant le résultat de la commande tahoma -ln présent aussi dans les instructions. Tu feras de même pour contrôler que la CATEGORY existe bien"},
                {"role": "system", "content": "Si ma demande n'exige pas d’exécuter une commande tu n'afficheras pas command:"},
                {"role": "system", "content": "Tu utiliseras le vouvoiement"},
                {"role": "system", "content": "la syntaxe d'une commande est `ACTION CATEGORY NAME`. La syntaxe d'une instance de tahoma est : `tahoma` suivi du nombre de commandes necessaires"},
                {"role": "system", "content": "Pour exécuter plusieurs commandes à la suite dans la même instance de tahoma, la syntaxe est la suivante : tahoma ACTION CATGORY NAME ACTION CATEGORY NAME ACTION CATEGORY NAME ACTION CATEGORY NAME... et tu répètes cela pour le nombre de commandes nécessaires."},
                {"role": "system", "content": """Il n'y a pas de NOM ["ALL"], donc pour exécuter une instance de tahoma qui donne une ACTION pour tous les NOMS de la même CATEGORY il faut créer une instance de tahoma suivi du nombre de commandes du type ACTION CATGORY NAME correspondant au nombre d'équipement d'une CATEGORY"""},
                {"role": "system", "content": """tahoma permet de controler des equipement présent dans un domicile. Donc pour eteindre le chauffage dans toute la maison, il faut creer une instance de tahoma et eteindre les chauffages de toutes les pieces"""},
                {"role": "system", "content": """Il existe deux types d'équipements Somfy. Les équipements équipés de la technologie IO (avec retour d'information) et les équipement RTS sans retour d'information. C'est pourquoi on ne peux pas demander à un équipement RTS de se fermer à 25% car il n'a pas l'information de son état. On ne peux pas non plus exécuter la commande stop avec les équipements RTS. Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par exemple si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : tahoma open shutter NOM sleep for 10 cancel last action. C'est pourquoi il peut-etre judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION stop, soit la commande cancel last action"""},
                {"role": "system", "content": "Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par exemple si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : tahoma open shutter NOM sleep for 10 cancel last action. C'est pourquoi il peut être judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION stop, soit la commande cancel last action"},
                {"role": "system", "content": """Voici un exemple d'une seule instance de tahoma :`tahoma open shutter ["Cuisine"] open shutter ["Salon"] on plug ["Bureau"]`. Cela exécutera les trois actions dans l'ordre spécifié."""},
                {"role": "system", "content": "Voici la liste des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces noms que tu feras tes réponses. Il n'est pas possible de modifier ces noms ou de les traduire dans tes réponses :"+str(names) },
                {"role": "system", "content": "Voici la liste des ACTION possibles pour les équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces actions que tu feras tes réponses. Il n'est pas possible de modifier ces actions ou de les traduire dans tes réponses :"+str(actions) },
                {"role": "system", "content": "Voici la liste des CATEGORY possibles pour les équipements présents dans la maison. C'est sur la base de ces catégories que tu feras tes réponses. Il n'est pas possible de modifier ces catégories ou de les traduire dans tes réponses :"+str(categories) },
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion_resp
#
    async def chat_loop():
        # Obtenir la phrase de bienvenue de ChatGPT
        user_input = "\nJe viens de te fournir de nouvelles instructions. As-tu bien pris en compte ces nouvelles instructions ?"
        assistant_response = "\nBienvenue dans votre service tahoma. Le model d'IA utilisé est : "+ model +"\nVous pouvez quitter à tout moment en tapant 'exit'."
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
                    print("\nExécution de la commande :", command.replace('command: ',''))
                    try:
                        try:
                            output = subprocess.check_output(""+search('tahoma') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                            #print(response['choices'][0]['message']['content'])
                            print("Résultat de la commande :", output.decode())
                        except:
                            output = subprocess.check_output("python3 "+search('tahoma.py') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                            print("Résultat de la commande :", output.decode())
                    except Exception as e:
                        print(e)
                else:
                    # Affiche la réponse de ChatGPT
                    assistant_response = response['choices'][0]['message']['content']
                    print("\n\033[1mAssistant:\033[0m ", assistant_response)
# Exécute la boucle de chat de manière asynchrone
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chat_loop())

main(model)

