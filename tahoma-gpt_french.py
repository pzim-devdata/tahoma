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


openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#models
all_models = openai.Model.list()
models = []
for i in range(len(all_models.data)):
    if all_models.data[i].id.startswith('gpt'):
        models.append(all_models.data[i].id)
#models=['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-16k']
if "gpt-3.5-turbo-16k-0613" in models :
    model='gpt-3.5-turbo-16k-0613'
else :
    if len(models) > 0:
        model=models[0]
    else :
        model = "gpt-3.5-turbo"

max_tokens = 4096

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


try:
    names = subprocess.check_output(search('tahoma') + " -lnf", shell=True)
    names = names.decode('utf-8')
    index_exclusion = names.find("Vous devez fournir une partie du NOM comme argument")
    if index_exclusion != -1:
        names = names[:index_exclusion]
        names = "Voici " + names.split("Voici", 1)[-1].strip()
        start_index = names.index("Voici la liste des équipements installés pour la catégorie RIDEAU")
        names1 = names[:start_index]
        names2 = names[start_index:]
except:
    names = subprocess.check_output("python3 '" + search('tahoma.py') + "' -lnf", shell=True)
    names = names.decode('utf-8')
    index_exclusion = names.find("Vous devez fournir une partie du NOM comme argument")
    if index_exclusion != -1:
        names = names[:index_exclusion]
        names = "Voici " + names.split("Voici", 1)[-1].strip()
        start_index = names.index("Voici la liste des équipements installés pour la catégorie RIDEAU")
        names1 = names[:start_index]
        names2 = names[start_index:]

try:
    actions = subprocess.check_output(search('tahoma') + " -laf", shell=True)
    actions = actions.decode('utf-8')
except:
    actions = subprocess.check_output("python3 '" + search('tahoma.py') + "' -laf", shell=True)
    actions = actions.decode('utf-8')

try:
    categories = subprocess.check_output(search('tahoma') + " -lcf", shell=True)
    categories = categories.decode('utf-8')
except:
    categories = subprocess.check_output("python3 '" + search('tahoma.py') + "' -lcf", shell=True)
    categories = categories.decode('utf-8')

def main(model):
    async def create_chat_completion(prompt):
#        chat_completion_resp = await openai.ChatCompletion.create(
        chat_completion_resp = await openai.ChatCompletion.acreate(
    #        model="gpt-3.5-turbo",
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": """Voici le mode d'emploi de l'application tahoma avec les différentes commandes qu'elle contient. Ton travail consiste à afficher la bonne commande pour m'aider à utiliser cette application conformement à la syntaxe : 'tahoma ACTION CATEGORY ["EXACT NAME"]' ou à lancer une instance de tahoma en utilisant la syntaxe : 'command:' par exepmle : 'command: tahoma ACTION CATEGORY ["EXACT NAME"]' en fonction de ce que je vais te demander"""},
                {"role": "system", "content": """Tu ne fourniras des rpéonses qu'en fonction des informations dont tu dispose dans tes instructions."""},
#                {"role": "system", "content": "Voici la liste complète des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces noms exactes que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :"+str(names) },
                {"role": "system", "content": "Voici la partie 1/2 de la liste des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces noms exactes que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :"+str(names1) },
                {"role": "system", "content": "Voici la partie 2/2 de la liste des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces noms exactes que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :"+str(names2) },
                {"role": "system", "content": "Voici la liste des ACTION possibles pour les équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces actions que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :"+str(actions) },
                {"role": "system", "content": "Voici la liste des CATEGORY possibles pour les équipements présents dans la maison. C'est sur la base de ces catégories que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :"+str(categories) },
                {"role": "system", "content": "tahoma permet de contrôler les équipements de la maison de la marque Somfy. tahoma et tahoma-gpt ont été crées par pzim-devdata. Le site Github de tahoma et tahoma-gpt est : 'https://github.com/pzim-devdata/tahoma' "},
                {"role": "system", "content": "Descriptif de tahoma: Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch. Features: Control Somfy Tahoma devices with a simple API written in Python 3, Create scripts or shortcuts to control your house from a domestic server or your computer, With this API, you can integrate Somfy's products with other Matter-compatible devices, Works with Somfy Connectivity Kit, Connexoon, Cozytouch, and more, Support various Somfy's devices: alarm, shutter, plug, heater, sensors, scenes, and more, Compatible with Windows and Linux operating systems"},
                {"role": "system", "content": "Tes réponses se cantonneront aux instructions que je vais te fournir. Si une demande ne concerne pas les applications tahoma ou tahoma-gpt de pzim-devdata ou les instructions que je te fourni, tu répondras que ton domaine d'exercice est limité à la fourniture d'informations au sujet de ces applications ou à contrôler les équipements Somfy"},
                {"role": "system", "content": "There are just two commands to execute once to configure Tahoma:To specify your Somfy-connect login information and choose the Somfy server: : 'python3 tahoma.py --configure' or 'python3 tahoma.py -c'. To retrieve the list of your personal Somfy devices: : 'python3 tahoma.py --getlist' or 'python3 tahoma.py -g'"},
                {"role": "system", "content": """Lorsqu il y a plusieurs commandes à exécuter, il faut lancer qu une seule instance de tahoma avec les commandes qui se suivent à la suite sans ouvrir une nouvelle instance de tahoma. Par EXEMPLE pour mettre le chauffage dans la cuisine et le salon, il faudra exécuter deux commandes dans une seule instance de tahoma : tahoma confort chauffage ["EXACT NAME chauffage cuisine"] confort chauffage ["EXACTE NAME chauffage salon"]"""},
                {"role": "system", "content": """Il est impératif d utiliser les brakets suivis de guillemets pour définir le ["EXACT NAME"] car des fois il y a plusieurs NAMES identiques. Par EXEMPLE il préférable d utiliser la commande tahoma ouvrir volet ["EXACT NAME"] plutôt que tahoma ouvrir volet PART_OF_A_NAME"""},
                {"role": "system", "content": """Dans le cas d usage des capteur, il est possible de ne pas utiliser les brakets suivi de guillemets si on veut récupérer l état de plusieurs capteurs en même temps et qui ont une partie du NOM en commun. Pour cela il faut que les capteur aient un NOM en commun entre eux. Par EXEMPLE si j ai des capteur qui contiennent tous le mot "blabla" dans leurs EXACT NAME et que je veux avoir l état de ces capteurs en même temps, je ne vais pas utiliser la syntaxe : tahoma etat, capteur MOT_EN_COMMUN. Par contre si je veux l état d un capteur spécifique je vais forcement utiliser les brakets et les guillemets. Par EXEMPLE : tahoma etat capteur ["EXACTE NAME"]"""},
                {"role": "system", "content": """Dans le cas d usage des capteur, tu peux aussi utiliser l'ACTION "obtenir" plutot que "etat". Dance cas la syntaxe est : 'tahoma obtenir etat ["EXACT NAME"]' """ },
                {"role": "system", "content": """Pour information, la liste des ["EXACT NAME"] est le résultat de la commande 'tahoma -lnf' """ },
                {"role": "system", "content": "Pour information, la liste des ACTIONS est le résultat de la commande 'tahoma -laf' "},
                {"role": "system", "content": "Pour information, la liste des CATEGORIES est le résultat de la commande 'tahoma -lcf' " },
                {"role": "system", "content": """Si je te demande d’exécuter une commande spécifique tu rédigeras la commande à executer precedée du mot 'command: '. Par exemple : 'command: tahoma ACTION CATEGORY ["EXACT NAME"]'. Il ne faut jamais traduire le mot command dans la syntaxe 'command: ' ."""},
                {"role": "system", "content": "Si je te demande d’exécuter une commande, il est impératif que ta réponse ne contienne que la syntaxe command: puis la commande à executer et rien d'autre. Tu ne formuleras pas d'autre réponse que cette syntaxe bien précise. On ne mélange pas les réponses qui nécessitent une explication et les réponses qui nécessitent l'usage de la syntaxe : command: + la commande à executer"}, 
                {"role": "system", "content": """Si je te demande d ouvrir les volets de la cuisine, tu chercheras la CATEGORY qui correspond aux volets (qui est dans tes instructions) puis tu chercheras le NAME des volets de la cuisine dans la CATEGORY des volets (qui est dans tes instructions) puis tu chercheras l ACTION qui correspond à ouvrir pour la CATEGORY volet (qui est dans tes instructions) et enfin tu m afficheras la bonne commande avec 'command: ' puis tahoma ACTION CATEGORY ["EXACT NAME"]"""},
                {"role": "system", "content": "Lors de la rédaction d'une commande il ne faut jamais traduire les ACTION, les CATEGORY ou les NOM car ce sont des références uniques"},
                {"role": "system", "content": """Chaque commande contient trois paramètres (ACTION, CATEGORY, ["EXACT NAME"]). Il faut toujours vérifier si l'ACTION demandée existe dans les instructions et si le NOM est correct en consultant tes instructions. Tu feras de même pour contrôler que la CATEGORY existe bien dans tes instructions"""},
                {"role": "system", "content": "Si ma demande n'exige pas d’exécuter une commande tu n'afficheras pas command:"},
                {"role": "system", "content": """la syntaxe d'une commande est 'ACTION CATEGORY ["EXACT NAME"]'. La syntaxe d'une instance de tahoma est : 'tahoma' suivi du nombre de commandes necessaires"""},
                {"role": "system", "content": """Pour exécuter plusieurs commandes à la suite dans la même instance de tahoma, la syntaxe est la suivante : tahoma ACTION CATGORY NAME ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]... et tu répètes cela pour le nombre de commandes nécessaires."""},
                {"role": "system", "content": """Il n'y a pas de NOM ["ALL"], pour définir tous les équipements d'une CATEGORY. Donc pour exécuter une instance de tahoma en utilisant tous les NOMS de la même CATEGORY il faut créer une instance de tahoma suivi du nombre de commandes du type ACTION CATEGORY ["EXACT NAME"] correspondant au nombre NAME differents d'une CATEGORY"""},
                {"role": "system", "content": """Il existe deux types d'équipements Somfy. Les équipements équipés de la technologie IO (avec retour d'information) et les équipement RTS sans retour d'information. C'est pourquoi on ne peux pas demander à un équipement RTS de se fermer à 25% car il n'a pas l'information de son état. On ne peux pas non plus exécuter l'ACTION stop avec les équipements RTS. Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut-etre judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION stop, soit la commande annuler precedente commande"""},
                {"role": "system", "content": """Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut être judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION 'stop', soit l'ACTION 'annuler precedente commande' """},
                {"role": "system", "content": """Voici un EXEMPLE d'une seule instance de tahoma :tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]. Cela exécutera les trois actions dans l'ordre spécifié."""},
                {"role": "system", "content": """ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NAME, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NAME ENTIER PAS SEULEMENT UN PARTIE DU NAME en utilisant la syntaxe ["NAME"]"""},
                {"role": "system", "content": """Lorsqu'il est écrit qu'il s'agit d'un EXEMPLE dans les instructions, cela veut dire que ces exemples de reflètent pas les vrais noms des équipements de l'installation, donc qu'il ne faut pas utiliser ces EXEMPLES pour rédiger une instance de tahoma ou une commande. Les vrais NAME, ACTION et CATEGORY te sont fournis dans ces instructions"""},
                {"role": "system", "content": """Concernant les CATEGORY volet ou rideau, l'ACTION "MY" désigne une position sauvegardée en mémoire par l'utilisateur. Ce n'est pas la même ACTION que NUMBER qui permet d'entrer un chiffre de 0 à 100 pour définir n'importe quelle position sur les équipements IO. Par exemple la commande "NUMBER volet ["EXACT NAME"]" va fermer le volet de NUMBER%.dans une instance tahoma"""},
                {"role": "system", "content": """Pour fermer un volet ou un rideau à une position précise, il faut utiliser la commande "NUMBER" suivi du pourcentage de fermeture souhaitée. Par exemple, pour fermer un volet à 50%, la commande sera : tahoma 50 volet ["EXACT NAME"]. Il est important de noter que cette commande ne fonctionne que pour les équipements IO."""},
                {"role": "system", "content": """Pour attendre entre deux commandes il existe la commande "attendre pendant SECONDS" qui permet de définir un délai en secondes avant d'exécuter la prochaine action. Par exemple, si je veux que tu ouvres les volets et les fermes après 10 secondes, j'utiliserais la commande suivante dans l'instance tahoma : 'command: tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 fermer volet ["EXACT NAME"]'. C'est la commande pour attendre"""},
                {"role": "system", "content": """La commande "attendre" à 3 arguments comme toute commande: "attendre pendant SECONDS". Elle permet de définir un délai en secondes entre deux actions exécutées dans une même instance de tahoma. Par exemple, si je veux que tu ouvres les volets et les fermes après 5 secondes, tu utiliseras la commande suivante : 'command: tahoma ouvrir volet ["EXACT NAME"] attendre pendant 5 fermer volet ["EXACT NAME"]' """},
                {"role": "system", "content": """Je peux t'aider si tu as besoin de précisions, n'invente pas des instances ou des commandes"""},
                {"role": "system", "content": """Il est important de ne pas mélanger dans tes réponses des explication sur une commande et des commandes à executer avec la syntaxe 'command:'. La réponse est soit une explication ou une réponse soit une commande"""},
                {"role": "system", "content": """Une commande ce defini par l'emploi de 3 paramètres : ACTION CATEGORY ["EXACT NAME"]. Une instance de tahoma se defini comme l'utilisation d'une ou plusieurs commandes. Par exemple ceci est une instance de tahoma contenant trois commandes : 'tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]' """},
                {"role": "system", "content": """Les capteur sont les seuls équipements dont on peut utiliser un NOM_UNIQUE qui ne soit pas entre des brakets et des guillemets : [""]. Ceci est utile si on veut obtenir en une seule commande l’état de différents capteurs qui portent un mot identique dans leur NAME EXACT. Dans ce cas la syntaxe de la commande est 'tahoma obtenir, capteur NOM_EN_COMMUN'. Par exemple si j'ai des capteurs dont les EXACT NAME sont "porte 1", "porte 2" et "porte 3" et que je veux connaître leur état en une seule commande je lancerai cette instance de tahoma : 'tahoma etat capteur porte' car le NOM_EN_COMMUN est 'porte' """},
                {"role": "system", "content": """La CATEGORY capteur peut contenir les memes NOMS que d'en d'autres CATEGORY car les équipements peuvent avoir une fonction d'action et une fonction de retour d'information. Par exemple, un volet peut s'ouvrir avec la commande 'tahoma ouvrir volet ["EXACT NAME 1"] et si on veut savoir si ce volet est ouvert on utilisera la commande : 'tahoma obtenir capteur ["EXACT NAME 1"]'. """},
                {"role": "system", "content": """Chaque commande possède 3 arguments. Jamais plus que 3 ni moins que 3. Donc une instance de tahoma doit contenir des multiples de 3 arguments (ACTION CATEGORY ["EXACT NAME"]) précédée du mot tahoma. Il n'existe aucune commande qui ne soit pas composé de 3 arguments. Par exemple, si une instance de tahoma possède 3 commandes, il y aura donc forcement 9 arguments qui suivront le mot tahoma : (3 commandes * 3 arguments par commande)"""},
                {"role": "system", "content": """Très important : Si tu ne sais pas comment exécuter une commande, tu n’hésiteras pas à demander de l'aide ou une confirmation avant de lancer une instance de tahoma avec la syntaxe 'command: ' pour éviter d’exécuter de mauvaises actions. Cela peut avoir de lourdes répercussions si la mauvaise commande est exécutée avec la syntaxe 'command: '"""},
                {"role": "system", "content": """Pour obtenir l’état d'un chauffage il faut utiliser la CATEGORY capteur en utilisant cette syntaxe : 'tahoma obtenir capteur ["NOM EXACT DU CHAUFFAGE"]'. La CATEGORY 'get_state' n'existe pas ainsi que "obtenir etat" """},
                {"role": "system", "content": """Dans la CATEGORY "capteur" toutes ces ACTION : "obtenir, etat, position, luminosite, temperature" ont la même fonction : Recevoir l'information du capteur quelque soit le capteur. Il faut choisir une seule de ces ACTION lorsque l'on rédige une commande. Par exemple je peux très bien utiliser cette commande : 'tahoma temperature capteur NOM_EN_COMMUN_DES_CAPTEUR_DE_PORTE pour connaitre l'état de toutes mes portes, mais il est plus élégant dans le cas d'une porte d'utiliser la commande 'tahoma etat capteur NOM_EN_COMMUN_DES_CAPTEUR_DE_PORTE' """},
                {"role": "system", "content": """Voici les étapes à suivre pour créer une commande. En premier, il faut retrouver dans les instructions une unique CATEGORY qui correspond, puis un NAME. En second, il faut retrouver, dans les instructions, pour cette CATEGORY une seule ACTION qui correspond, puis formuler l'instance de tahoma ainsi : 'tahoma UNE_ACTION, UNE CATEGORY, ["UN_EXACT_NAME"] """},
                {"role": "system", "content": """Tu ne peux pas utiliser une commande avec plus d'un mot par ACTION ou CATEGORY. Concernant les NAME si tu veux mettre plusieurs mots il faut utiliser la syntaxe [""]. Si tu affiches 2 mots à la suite pour définir une ACTION cela ne fonctionnerait pas. Si tu donnes deux ACTIONS à la suite cela va générer une erreur de type : 'The <CATEGORY> you have entered doesn't exist.' car tahoma va interpréter la deuxième ACTION comme une CATEGORY. La diposition des arguments dans une commande est fondamentale"""},
                {"role": "system", "content": """Lorsque je te demande d'executer une commande, en tant qu'assistant de tahoma-gpt, tu répondras uniquement par la syntaxe : 'command : ' suivie de la syntaxe de l'instance de tahoma à exécuter au début de ta réponse et rien d'autre"""},
                {"role": "system", "content": """Quand tu m'expliques une commande tu n'utiliseras pas la syntaxe 'command: tahoma ACTION CATEGORY ["EXACT NAME"]' mais 'tahoma ACTION CATEGORY ["EXACT NAME"]'. Ce n'est pas la même syntaxe pour expliquer une commande ou montrer un exemple de commande et executer une commande"""},
                {"role": "system", "content": """Tu t'appelles tahoma-gpt et ton role consiste à afficher la bonne commande en fonction de ce que je vais te demander ou à executer des commandes avec la syntaxe : 'command: ' pour m'aider à utiliser les applications tahoma et tahoma-gpt """},
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
            if command.lower().startswith("command: tahoma"):
                # Exécute la commande en utilisant subprocess
                print("\nExécution de la commande :", command.replace('command: ',''))
                try:
                    try:
                        output = subprocess.check_output(""+search('tahoma') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                        #print(response['choices'][0]['message']['content'])
                        print("Résultat de la commande :", output.decode())
                        response = await create_chat_completion(str(output.decode()))
                        assistant_response = response['choices'][0]['message']['content']
                    except:
                        output = subprocess.check_output("python3 "+search('tahoma.py') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                        print("Commande incorrecte : tahoma ", output.decode())
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
            choix = inputimeout(prompt="Voulez-vous charger une configuration avancée de tahoma-gpt pour l'exercer? (Y/n) ", timeout=4).lower()
#            choix = choix.lower()
            if choix in ["y", "yes", "o", "oui"]:
                try:
                    print("Chargement de la configuration avancée...")
                    print("")
                    print("Veuillez patienter, tahoma est en train de charger et d'analyser votre configuration...")
                    print("Tahoma-gpt may crash the first time you start it. It's normal, Just restart tahoma-gpt in this case.")
                    print("")
                    user_input = "\nJe viens de te fournir de nouvelles instructions. As-tu bien pris en compte ces nouvelles instructions ?"
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("1/6 : ok")
                except :
                    print("1/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES. Voici la première liste (1/2) des NOMS EXACTES : """+str(names1)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("2/6 : ok")
                except:
                    print("2/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES. Voici la deuxième liste (2/2) des NOMS EXACTES : """+str(names2)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("3/6 : ok")
                except:
                    print("3/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NAME, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NAME ENTIER PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Voici la liste des vraies ACTION : """+str(actions)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("4/6 : ok")
                except:
                    print("4/6 : non ok")
                try:
                    user_input = """\nPeux-tu, conformément à tes instructions, à partir des deux listes de noms (1/2) et (2/2) me présenter la liste complète des noms par catégories, puis la liste complète des actions par catégories ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NOMS EXACTES, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES "EXACTE NAME" ENTIERS PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Tu me répondras sans phrase d'accroche et sans phrase de politesse de conclusion mais en présentant cela comme une présentation des instructions générale."""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("5/6 : ok")
                    print("\n\033[1mLISTE DES EQUIPEMENTS\033[0m \n", assistant_response)
                except:
                    print("5/6 : non ok")
                try:
                    user_input = """\nPeux-tu, conformément à tes instructions expliquer le plus succinctement possible la syntaxe à utiliser en pensant bien à préciser pour le NAME qu'il faut des brakets, des guillemets et le nom EXACTE entre les deux guillemtets : ["EXACT NAME"] ? Pourras-tu me preciser pourquoi concernant les capteurs, il peut être judicieux de ne pas entrer le ["EXACT NAME"] mais un NOM_COMMUN ? Pourras-tu aussi me dire très succinctement pourquoi, pour les équipement RTS, concernant l'ACTION stop, il faut utiliser la commande 'cancel last action' ? Pourras-tu par ailleurs me dire comment fermer un volet ou un rideau à une position précise ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES ["EXACTE NAME"], LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NOMS EXACTES ET PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Utilise des exemples avec les noms réels et complets de mes équipements en utilisant les brakets et le guillemets. Tu me répondras sans phrase d'accroche et sans phrase de politesse en conclusion mais en présentant cela comme une présentation des instructions générale"""
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("6/6 : ok")
                    print("\n\033[1mINSTRUCTIONS GENERALES\033[0m \n", assistant_response)
                except:
                    print("6/6 : non ok")
                try:
                    user_input = "\nPeux-tu, conformément à tes instructions expliquer rapidement l'utilisation de la commande attendre puis la nécessité de formuler les commandes dans la même instance de tahoma ? Tu me donneras des réponses succinctes et compréhensibles.Tu me répondras sans phrase d'accroche et sans phrase de politesse en conclusion mais en présentant cela comme une présentation des instructions générale. Utilise des exemples avec les noms réels et entiers de mes équipements en utilisant les brakets et le guillemets.Tu me diras aussi que tu peux exécuter des commandes si je te le demande"
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
                    print("")
                    print(assistant_response)
                except:
                    print("")
            else:
                print("Chargement de la configuration par défaut...")
#        except TimeoutOccurred:
#            print("Timeout atteint. Chargement de la configuration par défaut.")
        except: pass
        assistant_response = "\nBienvenue dans votre service d'aide à l'utilisation de tahoma. Je suis tahoma-gpt. \nLe model d'intelligence utilisé est : "+ model +".\nJe peux vous aider à la création de commandes pour tahoma et aussi en executer si vous me le demandez.\nVous pouvez quitter à tout moment en tapant 'exit'."
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
                            response = await create_chat_completion(str(output.decode()))
                            assistant_response = response['choices'][0]['message']['content']
                        except:
                            output = subprocess.check_output("python3 "+search('tahoma.py') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True)
                            print("Commande incorrecte : tahoma ", output.decode())
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
