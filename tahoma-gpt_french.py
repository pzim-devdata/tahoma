#!/usr/bin/python3
#MIT licence
#@pzim-devdata
#https://github.com/openai/openai-python
#https://github.com/pzim-devdata/tahoma#add-chatgpt-functionalities-
#python3 -m pip install --upgrade openai
#Non utiles :
##python3 -m pip install openai[embeddings]
##python3 -m pip install openai[wandb]
##python3 -m pip install openai[datalib] 


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
from hashlib import sha256

version="0.0.1"
langage="french"

version='tahoma_gpt : version '+version+"_"+langage

openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#engine or model ?
engine_or_model = 'model'

#get models and engines
try:
    all_models = openai.Model.list()
    models = []
    engines = []
    for i in range(len(all_models.data)):
        if all_models.data[i].id.startswith('gpt'):
            models.append(all_models.data[i].id)
        else :
            engines.append(all_models.data[i].id)
    #models=['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-16k']
except openai.error.AuthenticationError:
        print("Veuillez entrer une clé API OpenAI valide dans le script")
        exit()

#choose a model
model="gpt-3.5-turbo-16k-0613"

if model in models :
    pass
else :
    if len(models) > 0:
        model=models[0]
    else :
        model = "gpt-3.5-turbo"

#choose an engine
if "babbage" in engines :
    engine='babbage'
else :
    engine=models[0]

##parametres
max_tokens = int(9000) #longueur max d'un seul échange user assistant
max_tokens_allowed = int(0.95*max_tokens)#(max_token gpt-3.5-turbo : 4096 ,gpt-3.5-turbo-16k-0613 :16385 tokens)
temperature=0.4 #0.7 par defaut entre 0 et 1 0:rationnel 1:inventif
presence_penalty=2.0 #0 par defaut. par exemple, 2.0 incitera le modèle à respecter davantage les instructions sans créativité : de 0 à l'infini
frequency_penalty=0 #0 par defaut. diversité lexicale de 0 à infini. Peu de diversité : 0 .>2 beaucoup de diversité
top_p= 0.5 #1.0 par defaut. de 0 à 1 variété des réponses probables. 0 : choisi la reponse la plus probable

#arguments
args = sys.argv

def search(filename_to_find):
    # Répertoire d'exécution du script
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
    except:
        script_directory = os.path.dirname(os.path.abspath(__name__))
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

#Générer une reference domicile pour l'assistant
try:
    domicile_ref=sha256(b"names1+names2+actions+categories").hexdigest()
except:
    domicile_ref="None"


#instructions=[
#    {"role": "system", "content": """Voici le mode d'emploi de l'application tahoma avec les différentes commandes qu'elle contient. Tu as deux roles : - Rôle de "help assistant" pour m'aider à utiliser l'application tahoma conformément à la syntaxe : 'tahoma ACTION CATEGORY ["EXACT NAME"]'. - Rôle de "command execution"  pour éxecuter une instance de tahoma en utilisant dans la function 'command' la syntaxe : 'command: tahoma ACTION CATEGORY ["EXACT NAME"]' en fonction de ce que je vais te demander."""}, # 'command:' par exemple : 'command:
#    {"role": "system", "content": """Tu ne fourniras des réponses qu'en fonction des informations dont tu disposes dans tes instructions locales."""}, 
##    {"role": "user", "content": "Voici la liste complète des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base locale de ces noms exacts que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :<names>\n"+str(names)+"\n</names>"},
#    {"role": "system", "content": "Voici la partie 1/2 de la liste des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base locale de ces noms exacts que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :<names1>\n"+str(names)+"\n</names1>"},
#    {"role": "system", "content": "Voici la partie 2/2 de la liste des NAME des équipements présents dans la maison pour chaque catégorie. C'est sur la base locale de ces noms exacts que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :<names2>\n"+str(names2)+"\n</names2>"},
#    {"role": "system", "content": "Voici la liste des ACTION possibles pour les équipements présents dans la maison pour chaque catégorie. C'est sur la base de ces actions que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :<actions>\n"+str(actions)+"\n</actions>"},
#    {"role": "system", "content": "Voici la liste des CATEGORY possibles pour les équipements présents dans la maison. C'est sur la base locale de ces catégories que tu feras tes réponses. ATTENTION, NE SURTOUT PAS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES :<categories>\n"+str(categories)+"\n</categories>"},
#    {"role": "user", "content": "tahoma permet de contrôler les équipements de la maison de la marque Somfy. tahoma et tahoma-gpt ont été créés par pzim-devdata. Le site Github de tahoma et tahoma-gpt est : 'https://github.com/pzim-devdata/tahoma'"},
#    {"role": "user", "content": "Descriptif de tahoma: Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch. Features: Control Somfy Tahoma devices with a simple API written in Python 3, Create scripts or shortcuts to control your house from a domestic server or your computer, With this API, you can integrate Somfy's products with other Matter-compatible devices, Works with Somfy Connectivity Kit, Connexoon, Cozytouch, and more, Support various Somfy's devices: alarm, shutter, plug, heater, sensors, scenes, and more, Compatible with Windows and Linux operating systems"},
#    {"role": "user", "content": "Tes réponses se cantonneront aux instructions que je vais te fournir. Si une demande ne concerne pas les applications tahoma ou tahoma-gpt de pzim-devdata ou les instructions que je te fournis, tu répondras que ton domaine d'exercice est limité à la fourniture d'informations au sujet de ces applications ou à contrôler les équipements Somfy"},
#    {"role": "user", "content": "There are just two commands to execute once to configure Tahoma:To specify your Somfy-connect login information and choose the Somfy server: : 'python3 tahoma.py --configure' or 'python3 tahoma.py -c'. To retrieve the list of your personal Somfy devices: : 'python3 tahoma.py --getlist' or 'python3 tahoma.py -g'"},
#    {"role": "system", "content": """Lorsqu'il y a plusieurs commandes à exécuter, il faut lancer qu'une seule instance de tahoma avec les commandes qui se suivent à la suite sans ouvrir une nouvelle instance de tahoma. Par EXEMPLE pour mettre le chauffage dans la cuisine et le salon, il faudra exécuter deux commandes dans une seule instance de tahoma : tahoma confort chauffage ["EXACT NAME chauffage cuisine"] confort chauffage ["EXACTE NAME chauffage salon"]"""},
#    {"role": "system", "content": """Il est impératif d'utiliser les brackets suivis de guillemets pour définir le ["EXACT NAME"] car parfois il y a plusieurs NAMES identiques. Par EXEMPLE il est préférable d'utiliser la commande tahoma ouvrir volet ["EXACT NAME"] plutôt que tahoma ouvrir volet PART_OF_A_NAME"""},
#    {"role": "system", "content": """Dans le cas d'utilisation des capteurs, il est possible de ne pas utiliser les brackets suivis de guillemets si on veut récupérer l'état de plusieurs capteurs en même temps et qui ont une partie du NOM en commun. Pour cela, il faut que les capteurs aient un NOM en commun entre eux. Par EXEMPLE, si j'ai des capteurs qui contiennent tous le mot "blabla" dans leurs EXACT NAME et que je veux avoir l'état de ces capteurs en même temps, je vais utiliser la syntaxe : tahoma etat, capteur MOT_EN_COMMUN. Par contre, si je veux l'état d'un capteur spécifique, je vais forcément utiliser les brackets et les guillemets. Par EXEMPLE : tahoma etat capteur ["EXACT NAME"]"""},
#    {"role": "system", "content": """Dans le cas d'utilisation des capteurs, il existe plusieurs types de capteurs, mais tous peuvent utiliser n'importe quelle ACTION. Toutes les ACTIONS de la CATEGORY des capteur ont la même fonction; celle de récupérer l'état d'un équipement. Je te suggère d'utiliser l'ACTION 'etat' pour tous les types de capteurs """},
#    {"role": "user", "content": """Pour information, la liste des ["EXACT NAME"] est le résultat de la commande 'tahoma -lnf' """},
#    {"role": "user", "content": "Pour information, la liste des ACTIONS est le résultat de la commande 'tahoma -laf' "},
#    {"role": "user", "content": "Pour information, la liste des CATEGORIES est le résultat de la commande 'tahoma -lcf' " },
#    {"role": "user", "content": """Si je te demande d’exécuter une commande spécifique tu rédigeras la commande à executer dans la function 'command'. Tu afficheras 'command: tahoma ACTION CATEGORY ["EXACT NAME"]'. Il ne faut jamais traduire le mot 'command: '  lorsque tu exécutes la function 'command' ."""},
#    {"role": "user", "content": "Si je te demande d’exécuter une commande, il est impératif que ta réponse ne contienne que la syntaxe de la function 'command' et rien d'autre. Tu ne formuleras pas d'autre réponse que cette syntaxe bien précise. On ne mélange pas les réponses qui nécessitent une explication et les réponses qui nécessitent l'usage de la function 'command' avec la commande à exécuter"},
#    {"role": "system", "content": """Si je te demande d ouvrir les volets de la cuisine, tu chercheras l'ACTION qui correspond à ouvrir pour la CATEGORY volet (qui est dans tes instructions locales) puis la CATEGORY qui correspond aux volets (qui est dans tes instructions locales) puis tu chercheras le NAME des volets de la cuisine dans la CATEGORY des volets (qui est dans tes instructions locales) et enfin tu executeras la function 'command' avec la syntaxe qui correspond"""}, #avec 'command: ' puis
#    {"role": "system", "content": "Lors de la rédaction d'une commande il ne faut jamais traduire les ACTION réels, les CATEGORY réelles ou les NOM réels car ce sont des références uniques"},
#    {"role": "user", "content": """Chaque commande contient trois paramètres (ACTION, CATEGORY, ["EXACT NAME"]). Il faut toujours vérifier si la CATEGORY, l'ACTION et le NOM sont corrects en consultant tes instructions"""},
#    {"role": "system", "content": "Si ma demande n'exige pas d’exécuter une commande tu n'utiliseras pas la function 'command' mais la function 'explication'"},
#    {"role": "user", "content": """la syntaxe d'une commande est 'ACTION CATEGORY ["EXACT NAME"]'. La syntaxe d'une instance de tahoma est : 'tahoma' suivi du nombre de commandes necessaires"""},
#    {"role": "system", "content": """Pour exécuter plusieurs commandes à la suite dans la même instance de tahoma, la syntaxe est la suivante : tahoma ACTION CATGORY NAME ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]... et tu répètes cela pour le nombre de commandes nécessaires."""},
#    {"role": "user", "content": """Il n'y a pas de NOM ["ALL"], pour définir tous les équipements d'une CATEGORY. Donc pour exécuter une instance de tahoma en utilisant tous les NOMS de la même CATEGORY il faut créer une instance de tahoma suivi du nombre de commandes du type ACTION CATEGORY ["EXACT NAME"] correspondant au nombre de NAME differents d'une CATEGORY"""},
#    {"role": "system", "content": """Il existe deux types d'équipements Somfy. Les équipements équipés de la technologie IO (avec retour d'information) et les équipement RTS sans retour d'information. C'est pourquoi on ne peux pas demander à un équipement RTS de se fermer à 25% car il n'a pas l'information de son état. On ne peux pas non plus exécuter l'ACTION stop avec les équipements RTS. Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut-etre judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION stop de la CATEGORY volet, soit la commande annuler precedente commande"""},
#    {"role": "user", "content": """Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut être judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION 'stop', soit l'ACTION 'annuler precedente commande' """},
#    {"role": "user", "content": """Voici un EXEMPLE d'une seule instance de tahoma :tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"]. Cela exécutera les trois actions dans l'ordre spécifié."""},
#    {"role": "user", "content": """ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NAME, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NAME ENTIER PAS SEULEMENT UN PARTIE DU NAME en utilisant la syntaxe ["NAME"]"""},
#    {"role": "user", "content": """Lorsqu'il est écrit qu'il s'agit d'un EXEMPLE dans les instructions, cela veut dire que ces exemples de reflètent pas les vrais noms des équipements de l'installation, donc qu'il ne faut pas utiliser ces EXEMPLES pour rédiger une instance de tahoma ou une commande. Les vrais NAME, ACTION et CATEGORY te sont fournis dans ces instructions"""},
#    {"role": "system", "content": """Concernant les CATEGORY volet ou rideau, l'ACTION "MY" désigne une position sauvegardée en mémoire par l'utilisateur. Ce n'est pas la même ACTION que NUMBER qui permet d'entrer un chiffre de 0 à 100 pour définir n'importe quelle position sur les équipements IO. Par exemple la commande "NUMBER volet ["EXACT NAME"]" va fermer le volet de NUMBER%.dans une instance tahoma"""},
#    {"role": "user", "content": """Pour fermer un volet ou un rideau à une position précise, il faut utiliser la commande "NUMBER" suivi du pourcentage de fermeture souhaitée. Par exemple, pour fermer un volet à 50%, la commande sera : tahoma 50 volet ["EXACT NAME"]. Il est important de noter que cette commande ne fonctionne que pour les équipements IO."""},
#    {"role": "system", "content": """Pour attendre entre deux commandes il existe la commande "attendre pendant SECONDS" qui permet de définir un délai en secondes avant d'exécuter la prochaine action. Par exemple, si je veux que tu ouvres les volets et les fermes après 10 secondes, j'utiliserais la commande suivante dans l'instance tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 fermer volet ["EXACT NAME"]'. C'est la commande pour attendre"""}, #command: 
#    {"role": "user", "content": """La commande "attendre" à 3 arguments comme toute commande: "attendre pendant SECONDS". Elle permet de définir un délai en secondes entre deux actions exécutées dans une même instance de tahoma. Par exemple, si je veux que tu ouvres les volets et les fermes après 5 secondes, tu utiliseras la commande suivante dans la function 'command' : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 5 fermer volet ["EXACT NAME"]' """}, #command: 
#    {"role": "user", "content": """Je peux t'aider si tu as besoin de précisions, N’hésites pas à me demander des précisions si tu ne trouves pas les noms dans tes instructions locales.Ne récupère pas des instances ou des commandes ailleurs que dans tes instructions locales.Si tu ne trouves pas les bons noms tu formuleras une réponse disant qu'il faut préciser ma demande car tu n'as pas assez d'information dans les instructions locales"""},
##    {"role": "user", "content": """Il est important de ne pas mélanger dans tes réponses des explication sur une commande et des commandes à executer avec la syntaxe 'command:'. La réponse est soit une explication ou une réponse soit une commande"""},
#    {"role": "system", "content": """Une commande ce defini par l'emploi de 3 paramètres : ACTION CATEGORY ["EXACT NAME"]. Une instance de tahoma se defini comme l'utilisation d'une ou plusieurs commandes. Par exemple ceci est une instance de tahoma contenant trois commandes : 'tahoma ACTION CATEGORY ["EXACT NAME"] ACTION CATEGORY ["EXACT NAME"] ACTION capteur NOM_UNIQUE_EN_COMMUN """},
#    {"role": "user", "content": """Les capteur sont les seuls équipements dont on peut utiliser un NOM_UNIQUE qui ne soit pas entre des brakets et des guillemets : [""]. Ceci est utile si on veut obtenir en une seule commande l’état de différents capteurs qui portent un mot identique dans leur NAME EXACT. Dans ce cas la syntaxe de la commande est 'tahoma etat, capteur NOM_EN_COMMUN'. Par exemple si j'ai des capteurs dont les EXACT NAME sont "porte 1", "porte 2" et "porte 3" et que je veux connaître leur état en une seule commande je lancerai cette instance de tahoma : 'tahoma etat capteur porte' car le NOM_EN_COMMUN est 'porte' """},
#    {"role": "user", "content": """La CATEGORY capteur peut contenir les mêmes NOMS que d'en d'autres CATEGORY car les équipements peuvent avoir une fonction d'action et une fonction de retour d'information. Par exemple, un volet peut s'ouvrir avec la commande 'tahoma ouvrir volet ["EXACT NAME 1"] et si on veut savoir si ce volet est ouvert on utilisera la commande : 'tahoma etat capteur ["EXACT NAME 1"]'. """},
#    {"role": "system", "content": """Chaque commande possède 3 arguments. Jamais plus que 3 ni moins que 3. Donc une instance de tahoma doit contenir des multiples de 3 arguments (ACTION CATEGORY ["EXACT NAME"]) précédée du mot tahoma. Il n'existe aucune commande qui ne soit pas composé de 3 arguments. Par exemple, si une instance de tahoma possède 3 commandes, il y aura donc forcement 9 arguments qui suivront le mot tahoma : (3 commandes * 3 arguments par commande)"""},
##    {"role": "user", "content": """Très important : Si tu ne sais pas comment exécuter une commande, tu n’hésiteras pas à demander de l'aide ou une confirmation avant de lancer une instance de tahoma avec la syntaxe 'command: ' pour éviter d’exécuter de mauvaises actions. Cela peut avoir de lourdes répercussions si la mauvaise commande est exécutée avec la syntaxe 'command: '"""},
#    {"role": "user", "content": """Pour obtenir l’état d'un chauffage il faut utiliser la CATEGORY capteur en utilisant cette syntaxe : 'tahoma etat capteur ["NOM EXACT DU CHAUFFAGE"]' """},
#    {"role": "user", "content": """Dans la CATEGORY "capteur" toutes ces ACTION : "obtenir, etat, position, luminosite, temperature" ont la même fonction : recevoir l'information du capteur quelque soit le type capteur. Il faut choisir une seule de ces ACTION lorsque l'on rédige une commande. Par exemple je peux très bien utiliser cette commande : 'tahoma temperature capteur NOM_EN_COMMUN_DES_CAPTEUR_DE_PORTE pour connaitre l'état de toutes mes portes, mais il est plus élégant dans le cas d'une porte d'utiliser la commande 'tahoma etat capteur NOM_EN_COMMUN_DES_CAPTEUR_DE_PORTE' """},
#    {"role": "user", "content": """ L'instance "tahoma etat capteur ["porte"] n'est pas correct.Pour connaître l’état des capteurs portant un nom en commun on n'utilise pas les brakets et les guillemets"""},
#    {"role": "user", "content": """Voici les étapes à suivre pour créer une commande. En premier, il faut retrouver dans les instructions l'unique  ACTION qui correspond à la CATEGORY, puis la CATEGORY qui correspond, puis un NAME  appartenant à la CATEGORY, puis formuler l'instance de tahoma ainsi : 'tahoma UNE_ACTION, UNE CATEGORY, ["UN_EXACT_NAME"] """},
#    {"role": "system", "content": """Tu ne peux pas utiliser une commande avec plus d'un mot par ACTION ou CATEGORY. Concernant les NAME si tu veux mettre plusieurs mots il faut utiliser la syntaxe ["EXACT NAME"]. Si tu affiches 2 mots à la suite pour définir une ACTION cela ne fonctionnera pas. Si tu donnes deux ACTIONS à la suite cela va générer une erreur de type : 'The <CATEGORY> you have entered doesn't exist.' car tahoma va interpréter la deuxième ACTION comme une CATEGORY. La disposition des arguments dans une commande est fondamentale """},
#    {"role": "system", "content": """Si tu affiches 2 mots à la suite pour définir une CATEGORY cela ne fonctionnera pas. Si tu donnes deux CATEGORY à la suite cela va générer une erreur de type : "There is no match. The NAME you gave is not exact or it's impossible to retrieve the state of '[exact name]'". car tahoma va interpréter la deuxième CATEGORY comme un NAME. La disposition des arguments dans une commande est fondamentale"""},
##    {"role": "user", "content": """Lorsque je te demande d'exécuter une commande, en tant qu'assistant de tahoma-gpt, tu répondras uniquement par la syntaxe : 'command: ' suivie de la syntaxe de l'instance de tahoma à exécuter au début de ta réponse et rien d'autre"""},
##    {"role": "user", "content": """Quand tu m'expliques une commande tu n'utiliseras pas la syntaxe 'command: tahoma ACTION CATEGORY ["EXACT NAME"]' mais 'tahoma ACTION CATEGORY ["EXACT NAME"]'. Ce n'est pas la même syntaxe pour expliquer une commande ou montrer un exemple de commande et exécuter une commande"""},
#    {"role": "user", "content": """Tu t'appelles tahoma-gpt et ton rôle consiste à afficher la bonne commande en fonction de ce que je vais te demander ou à exécuter des commandes en début de réponse pour m'aider à utiliser l'application tahoma avec tahoma-gpt."""},
#    {"role": "user", "content": "Pour définir le contexte :La version de cette application qui s'appelle tahoma-gpt est : "+version+". La référence du domicile est : "+domicile_ref}, #avec la syntaxe : 'command: '
##    {"role": "user", "content": """Si je te demande d'exécuter une commande, tu utiliseras le rôle de function et non d'assistant et tu afficheras l'instance de tahoma correspondante dans le contenu de la réponse. Cela se fera dans la section 'response' de ta réponse."""},
#    #                {"role": "user", "content": prompt}
#]

instructions=[
{"role": "system", "content": "Tu t'appelles tahoma-gpt et ton rôle consiste à afficher la bonne réponse en utilisant l'une des trois functions présentes dans tes instructions suivant le type de demande formulée"},
{"role": "system", "content": "Pour définir le contexte de cette conversation :La version de cette application qui s'appelle tahoma-gpt est : "+version+". La référence du domicile est : "+domicile_ref},
{"role": "system", "content": "Tu ne fourniras des réponses qu'en fonction des informations dans tes instructions." },
{"role": "system", "content": "Partie 1/2 de la liste des équipements présents dans la maison pour chaque catégorie : <names1>\n" + str(names1) + "\n</names1>" },
{"role": "system", "content": "Partie 2/2 de la liste des équipements présents dans la maison pour chaque catégorie : <names2>\n" + str(names2) + "\n</names2>" },
{"role": "system", "content": "Liste des ACTIONS possibles pour les équipements présents dans la maison : <actions>\n" + str(actions) + "\n</actions>" },
{"role": "system", "content": "Liste des CATEGORIES possibles pour les équipements présents dans la maison : <categories>\n" + str(categories) + "\n</categories>" },
{"role": "user", "content": "Tahoma permet de contrôler les équipements de la maison de la marque Somfy. Tahoma et Tahoma-GPT ont été créés par pzim-devdata. Le site GitHub de Tahoma et Tahoma-GPT est : 'https://github.com/pzim-devdata/tahoma'" },
{"role": "user", "content": "Descriptif de Tahoma : Tahoma is a simple API for controlling Somfy Tahoma devices using Python 3, thanks to the pyoverkiz API. With just a three-word input, you can control your devices. It was initially created for Tahoma but also works with Somfy Connectivity Kit, Connexoon, and Cozytouch." },
{"role": "user", "content": "Tes réponses se cantonneront aux instructions que je vais te fournir. Si une demande ne concerne pas les applications Tahoma ou Tahoma-GPT de pzim-devdata ou les instructions que je te fournis, tu répondras que ton domaine d'exercice est limité à la fourniture d'informations au sujet de ces applications ou à contrôler les équipements Somfy." },
{"role": "user", "content": "Il y a seulement deux commandes à exécuter pour configurer Tahoma : spécifier les informations de connexion Somfy et choisir le serveur Somfy avec 'python3 tahoma.py --configure' ou 'python3 tahoma.py -c', et récupérer la liste de vos équipements Somfy avec 'python3 tahoma.py --getlist' ou 'python3 tahoma.py -g'." },
{"role": "system", "content": "Lorsqu'il y a plusieurs commandes à exécuter, il faut les regrouper dans une seule instance de Tahoma. Par exemple, pour mettre le chauffage dans la cuisine et le salon, tu exécuteras deux commandes dans une seule instance de Tahoma : 'tahoma confort chauffage [\"NOM EXACT chauffage cuisine\"] confort chauffage [\"NOM EXACT chauffage salon\"]'." },
{"role": "system", "content": """Il existe deux types d'équipements Somfy. Les équipements équipés de la technologie IO (avec retour d'information) et les équipement RTS sans retour d'information. C'est pourquoi on ne peux pas demander à un équipement RTS de se fermer à 25% car il n'a pas l'information de son état. On ne peux pas non plus exécuter l'ACTION stop avec les équipements RTS. Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet ["EXACT NAME"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut-etre judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION stop de la CATEGORY volet, soit la commande annuler precedente commande"""},
{"role": "user", "content": "Le seul moyen d’arrêter un équipement RTS est d'annuler sa commande précédente dans la même instance de tahoma qui demande soit une ouverture soit une fermeture. Par EXEMPLE si je veux arrêter un volet RTS 10 secondes après lui avoir demandé de s'ouvrir, il faut exécuter dans la même instance de tahoma : 'tahoma ouvrir volet [\"EXACT NAME\"] attendre pendant 10 annuler precedente commande'. C'est pourquoi il peut être judicieux de demander si un volet est RTS ou IO afin d’exécuter, soit l'ACTION 'stop', soit l'ACTION 'annuler precedente commande'. La commande 'annuler précédente commande' annule la commande précédente immédiate de l'instance de tahoma sauf la commande 'attendre pendant SECOND' "},
{"role": "user", "content": "La commande 'annuler precedente commande' doit toujours être précédée d'une autre commande qu'elle annule. Cette commande annule la commande immédiatement précédente sauf la commande 'attendre pendant SECOND' dans la même instance de tahoma. Par EXEMPLE : 'tahoma fermer volet [\"EXACT NAME\"] attendre pendant 10 annuler precedente commande'. Dans cet EXEMPLE, cette instance de tahoma va fermer le volet, attendre 10 secondes et annuler la commande precedente qui est  'fermer volet [\"EXACT NAME\"]' sans annuler la commande 'attendre 10 secondes'"},
{"role": "user", "content": "Tu ne peux pas savoir si un volet est RTS ou IO, il faut le demander si tu as besoin de le savoir avant de fournir la bonne commande, car cette information n'est pas dans tes instructions locales"},
{"role": "system", "content": "Utilise les guillemets pour définir le ['NOM EXACT'] afin de distinguer les noms identiques. Par exemple, utilise la commande 'tahoma ouvrir volet [\"NOM EXACT\"]' au lieu de 'tahoma ouvrir volet PART_OF_A_NAME'." },
{"role": "system", "content": "Seulement pour la catégorie capteur, si tu veux récupérer l'état de plusieurs capteurs ayant une partie du NOM en commun, tu n'as pas besoin d'utiliser les guillemets. Par exemple, 'tahoma etat capteur MOT_EN_COMMUN' permet de récupérer l'état de plusieurs capteurs en même temps. Si tu veux l'état d'un capteur spécifique, tu utiliseras les guillemets et brackets : 'tahoma etat capteur [\"NOM EXACT\"]'." },
{"role": "system", "content": "Pour attendre entre deux commandes il existe la commande 'attendre pendant SECONDS' qui permet de définir un délai en secondes avant d'exécuter la prochaine action. Comme toutes commandes elle possède trois arguments. Par exemple, si je veux que tu ouvres les volets et les fermes après 10 secondes, j'utiliserais les commandes suivantes dans la même instance de tahoma : 'tahoma ouvrir volet [\"NOM EXACT\"] attendre pendant 10 fermer volet [\"NOM EXACT\"]'. C'est la commande pour attendre"},
{"role": "system", "content": "Pour les capteurs, utilise l'ACTION 'etat' pour tous les types de capteurs." },
{"role": "system", "content": "Concernant les CATEGORY volet ou rideau, l'ACTION 'MY' désigne une position sauvegardée en mémoire par l'utilisateur. Ce n'est pas la même ACTION que NUMBER qui permet d'entrer un chiffre de 0 à 100 pour définir n'importe quelle position sur les équipements IO. Par exemple la commande 'tahoma NUMBER volet [\"EXACT NAME\"]' va fermer le volet de NUMBER%.dans une instance tahoma"},
{"role": "system", "content": "la syntaxe de l'intance tahoma utilisant l'ACTION NUMBER est la suivante : 'tahoma NUMBER CATEGORY [\"EXACT NAME\"]"},
{"role": "system", "content": "Tu ne peux pas utiliser une commande avec plus d'un mot par ACTION ou CATEGORY. Concernant les NAME si tu veux mettre plusieurs mots il faut utiliser la syntaxe [\"EXACT NAME\"]. Si tu affiches 2 mots à la suite pour définir une ACTION cela ne fonctionnera pas. Si tu donnes deux ACTIONS à la suite cela va générer une erreur de type : '''The <CATEGORY> you have entered doesn't exist.''' car tahoma va interpréter la deuxième ACTION comme une CATEGORY. La disposition des arguments dans une commande est fondamentale "},
{"role": "system", "content": "Si tu affiches 2 mots à la suite pour définir une CATEGORY cela ne fonctionnera pas. Si tu donnes deux CATEGORY à la suite cela va générer une erreur de type : '''There is no match. The NAME you gave is not exact or it's impossible to retrieve the state of '[exact name]' '''. car tahoma va interpréter la deuxième CATEGORY comme un NAME. La disposition des arguments dans une commande est fondamentale"}, 
{"role": "user", "content": "La liste des NOMS EXACTS est le résultat de la commande 'tahoma -lnf'." },
{"role": "user", "content": "La liste des ACTIONS est le résultat de la commande 'tahoma -laf'." },
{"role": "user", "content": "La liste des CATEGORIES est le résultat de la commande 'tahoma -lcf'." },
{"role": "user", "content": "Si je te demande d'exécuter une commande spécifique, tu rédigeras la commande à exécuter dans la fonction 'command'. Tu afficheras 'command: ' suivi de la syntaxe 'tahoma ACTION CATEGORY [\"NOM EXACT\"]'. Ne traduis jamais le mot 'command: ' lors de l'exécution de la fonction 'command'." },
{"role": "user", "content": "Si je te demande d'exécuter une commande, ta réponse doit contenir uniquement la syntaxe de la commande à exécuter, sans explications supplémentaires. Ne mélange pas les réponses nécessitant une explication avec les réponses nécessitant l'utilisation de la fonction 'command' pour la commande à exécuter." },
{"role": "system", "content": "Lorsque je te demande d'ouvrir les volets de la cuisine, tu chercheras l'ACTION correspondante à 'ouvrir' dans la CATEGORY 'volet' (selon tes instructions). Ensuite, tu chercheras le NOM des volets de la cuisine dans la CATEGORY 'volet' (selon tes instructions). Enfin, tu exécuteras la function 'inexistant_localement' s'il n'y a pas de correspondance entre ma demande et les équipements présents dans tes instructions locales ou la fonction 'command' avec la syntaxe appropriée : 'command: tahoma ouvrir volet [\"NOM EXACT\"]' " },
{"role": "system", "content": "Il est important de ne jamais traduire les ACTIONS réelles, les CATEGORIES réelles ou les NOMS réels, car ce sont des références pour le fonctionnement de l'application Tahoma." },
{"role": "system", "content": "Si tu rencontres des difficultés pour trouver l'ACTION, la CATEGORY ou le NOM exact dans tes instructions, n'hésite pas à me demander des précisions conformément à la function 'inexistant_localement'." },
{"role": "user", "content": "N'oublie pas que ta réponse doit être concise et ne contenir que la syntaxe de la commande à exécuter, sans explications supplémentaires." },
{"role": "system", "content": "Si tu as d'autres questions ou besoin d'aide supplémentaire, n'hésite pas à me le faire savoir. Je suis là pour t'assister dans l'utilisation de l'application Tahoma."},
]

functions=[
    {"role": "function", "name" : "command", "content": """Lorsque je te demande explicitement d’exécuter une instance de tahoma ou lorsque je souhaite connaître et que tu me dises l'état d'un capteur et non de m'expliquer une action concernant mes équipements domotiques tu écriras seulement :'command: 'suivi de l'instance de tahoma correspondante, avec la syntaxe correcte des commandes. Tu utiliseras les arguments : actions, categories et noms réels fournis dans tes instructions. Tu n'écris rien d'autre que la syntaxe : 'command: tahoma 'suivi de la ou des commandes qui correspondent. Prends bien le temps de vérifier que l'action correspond à la catégorie, que la catégorie est la bonne et enfin que le nom correspond à la catégorie demandée et aux équipements de mon domicile. La liste des équipements est fournie dans tes instructions. Tu peux prendre ton temps pour exécuter la commande afin de bien t'assurer que les commandes sont bien exactes"""},
        {"role": "function", "name" : "explication", "content": """Lorsque je te demande de m'expliquer et non d’exécuter explicitement une instance de tahoma ou de demander l'état d'un capteur, tu écriras simplement la syntaxe relative à l'instance de tahoma qui correspond à ma demande sans l'expression 'command: ' au début.Par exemple : 'tahoma ACTION CATEGORY ["EXACT NAME"]. Tu essayeras de me fournir la catégorie, l'action qui correspond à la categorie et nom réel qui correspond à la categorie en fonction de la liste d'équipements présents dans mon domicile. Cette liste est fournie dans tes instructions. Tu me donneras une réponse d'explication. Tu peux prendre le temps pour répondre."""},
        {"role": "function", "name" : "inexistant_localement", "content": """Cette function doit-être vérifiée avant l'éventuel appel aux deux autres functions. Si je te demande d'ouvrir les volets dans la chambre 6123 tu appliques l'instruction concernant tes informations locales inexistantes car les "volets chambre 6123" ne sont pas dans tes instructions locales. Si tes instructions locales font apparaître les volets 6123 mais qu'ils ne sont pas dans la CATEGORY qui correspond à l'ACTION que je te demande tu feras de même. Pour résumer, si une commande n'est pas complètement présente dans tes instructions locales tu demandes de préciser la demande. Par exemple si j'ai un capteur 'porte couloir' dans mes instructions locales, cette porte fait partie de la CATEGORY capteur. Or, si je te demande d''ouvrir' la 'porte couloir'  il n'y a pas d'ACTION 'ouvrir' pour la CATEGORY  capteur et si la 'porte couloir' n’apparaît pas dans aucune autre CATEGORY qui a une ACTION 'ouvrir' dans tes instructions locales alors il est impossible d'établir une commande pour ouvrir cette porte avec les instructions locales dont tu disposes. Tu demanderas donc des précisions car la commande ouvrir porte ["porte couloir"] n'a pas l'ACTION ouvrir dans une quelconque  CATEGORY qui correspond à la porte du couloir """},

]

conversations=[]
messages=instructions+functions+conversations

def main(model):
    if engine_or_model == 'model':
        async def create_chat_completion(prompt):
    #        chat_completion_resp = await openai.ChatCompletion.create(
            chat_completion_resp = await openai.ChatCompletion.acreate(
        #        model="gpt-3.5-turbo",
                model=model,
                max_tokens=max_tokens,
#                temperature=temperature,
#                presence_penalty=presence_penalty,
#                frequency_penalty=frequency_penalty,
#                top_p=top_p,
                messages=messages+[{"role": "system", "content": "Répondez à la demande user qui suit en executant l'une des trois functions appropriée en fonction du type de question du user : Utiliser la function : 'inexistant_localement' si le user n'a pas spécifié un NOM ou une ACTION ou une CATEGORY existant dans tes instructions locales, 'command' si le user te demande d’exécuter une instance de tahoma pour obtenir l'état d'un capteur ou pour effectuer une action sur un équipement de la maison ou 'explication' si le user souhaite obtenir une explication sur le fonctionnement de tahoma."},{"role": "user", "content": prompt}]
            )
#            return chat_completion_resp.choices[0].message.content
            return chat_completion_resp

    elif engine_or_model == 'engine':
        async def create_chat_completion(prompt):
    #        chat_completion_resp = await openai.Completion.create(
            chat_completion_resp = await openai.Completion.acreate(
        #        model="gpt-3.5-turbo",
                model=engine,
                max_tokens=max_tokens,
#                temperature=temperature,
#                presence_penalty=presence_penalty,
#                frequency_penalty=frequency_penalty,
#                top_p=top_p,
#                prompt="Hello world"
                messages=messages+[{"role": "user", "content": prompt}]
            )
#            return(chat_completion_resp.choices[0].text)
            return chat_completion_resp
#
    async def chat_loop():
        if len(args) > 1 and sys.argv[1] != "":
            user_input = ' '.join(args[1:])
            response = await create_chat_completion(user_input)
            command = response['choices'][0]['message']['content']
            # Vérifie si la commande est "Command: echo 'Hello world'"
            if "command: tahoma" in command.lower():
#            if command.lower().startswith("command: tahoma"):
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
                response = await create_chat_completion(user_input)
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
                    user_input = "\nJe viens de te fournir de nouvelles instructions locales. As-tu bien pris en compte ces nouvelles instructions ainsi que les nouvelles function ?"
                    #conversations.append({"role": "user", "content": user_input})
                    #messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("1/6 : ok")
                except :
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("1/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES. Voici la première liste (1/2) des NOMS EXACTES : """+str(names1)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("2/6 : ok")
                except:
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("2/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER CES NOMS DANS TES REPONSES. Voici la deuxième liste (2/2) des NOMS EXACTES : """+str(names2)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("3/6 : ok")
                except:
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("3/6 : non ok")
                try:
                    user_input = """\nPeux-tu, intégrer ces informations le plus succinctement possible pour mieux les utiliser ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NAME, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NAME ENTIER PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Voici la liste des vraies ACTION : """+str(actions)+""". Ces informations te permettront ainsi de mieux élaborer les commandes tahoma dont la syntaxe est tahoma ACTION CATEGORY ["EXACTE NAME"] """
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("4/6 : ok")
                except:
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("4/6 : non ok")
                try:
                    user_input = """\nPeux-tu, conformément à tes instructions locales, à partir des deux listes de noms (1/2) et (2/2) me présenter la liste complète des noms par catégories présents dans mon domicile, puis la liste complète des actions par catégories ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES NOMS EXACTES, LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES "EXACTE NAME" ENTIERS PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Tu me répondras sans phrase d'accroche et sans phrase de politesse de conclusion mais en présentant cela comme une présentation des instructions générale."""
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("5/6 : ok")
                    print("\n\033[1mLISTE DES EQUIPEMENTS\033[0m \n", assistant_response)
                except:
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("5/6 : non ok")
                try:
                    user_input = """\nPeux-tu, conformément à tes instructions expliquer le plus succinctement possible la syntaxe à utiliser en pensant bien à préciser pour le NAME qu'il faut des brakets, des guillemets et le nom EXACTE entre les deux guillemtets : ["EXACT NAME"] ? Pourras-tu me preciser pourquoi concernant les capteurs, il peut être judicieux de ne pas entrer le ["EXACT NAME"] mais un NOM_COMMUN ? Pourras-tu aussi me dire très succinctement pourquoi, pour les équipement RTS, concernant l'ACTION stop, il faut utiliser la commande 'cancel last action' ? Pourras-tu par ailleurs me dire comment fermer un volet ou un rideau à une position précise ? ATTENTION, NE JAMAIS TRADUIRE OU MODIFIER LES ["EXACTE NAME"], LES NOMS D'ACTION ET LES NOMS DES CATEGORY DANS TES REPONSES ET FOURNI LES NOMS EXACTES ET PAS SEULEMENT UN PARTIE DU NAME dans la syntaxe ["EXACT NAME"]. Utilise des exemples avec les noms réels et complets de mes équipements en utilisant les brakets et le guillemets. Tu me répondras sans phrase d'accroche et sans phrase de politesse en conclusion mais en présentant cela comme une présentation des instructions générale"""
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("6/6 : ok")
                    print("\n\033[1mINSTRUCTIONS GENERALES\033[0m \n", assistant_response)
                except:
                    total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
                    print(str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("6/6 : non ok")
                try:
                    user_input = "\nPeux-tu, conformément à tes instructions expliquer rapidement l'utilisation de la commande attendre puis la nécessité de formuler les commandes dans la même instance de tahoma ? Tu me donneras des réponses succinctes et compréhensibles.Tu me répondras sans phrase d'accroche et sans phrase de politesse en conclusion mais en présentant cela comme une présentation des instructions générale. Utilise des exemples avec les noms réels et entiers de mes équipements en utilisant les brakets et le guillemets.Tu me diras aussi que tu peux exécuter des commandes si je te le demande"
#                    conversations.append({"role": "user", "content": user_input})
#                    messages=instructions+conversations
                    response = await create_chat_completion(user_input)
                    assistant_response = response['choices'][0]['message']['content']
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
#                    conversations.append({"role": "assistant", "content": assistant_response})
                    messages=instructions+conversations
                    print("")
                    print(assistant_response)
                except:
                    print("")
            else:
                print("Chargement de la configuration par défaut...")
#        except TimeoutOccurred:
#            print("Timeout atteint. Chargement de la configuration par défaut.")
        except: pass
        assistant_response = "Je suis tahoma-gpt. Le model d'intelligence utilisé est : "+ model +".\nVous pouvez quitter à tout moment en tapant 'exit'."
        print("\n\033[1mAssistant:\033[0m ", assistant_response)
#        conversations.append({"role": "assistant", "content": assistant_response})
        messages=instructions+conversations
        while True:
            total_tokens = int(sum(len(message['content'].split()) for message in messages)*1.7)
            while total_tokens > max_tokens_allowed:
                try:
                    old_conv = conversations[0]['content']
                    conversations.pop(0)
                    total_tokens -= len(old_conv.split())
                    messages=instructions+conversations
                    print("")
                    print("Suppression des anciennes conversations, limite max_tokens atteinte...")
    #                print("Suppression de la conversation :\n" +str(old_conv))
                    print("")
                    print( str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("")
                except:
                    old_inst = instructions[-1]['content']
                    instructions.pop(-1)
                    total_tokens -= len(old_inst.split())
                    messages=instructions+conversations
                    print("")
                    print("Suppression de l'instruction :\n" +str(old_inst))
                    print("\n\n")
                    print("ATTENTION !!!!!\nRisque que tahoma-gpt ne soit pas fonctionnel\nSuppression des anciennes instructions, limite max_tokens atteinte...\nAugmentez la valeur de max_tokens ou utilisez un modèle prenant en charge plus de tokens")
                    print("")
                    print( str(total_tokens) + "/" +str(max_tokens_allowed)+" tokens utilisés" )
                    print("")
                time.sleep(3)
                
            # Demande à l'utilisateur d'entrer une phrase d'instruction
            user_input = input("\n\033[1mInstruction:\033[0m ")
#            print(messages)
#            conversations.append({"role": "user", "content": user_input})
#            messages=instructions+conversations
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
#                if "command: tahoma" in command.lower() or "command: 'tahoma" in command.lower():
                if command.lower().startswith("command: tahoma") or command.lower().startswith("command: 'tahoma"):
                    # Exécute la commande en utilisant subprocess
                    try:
                        async def erreur_action():
                            print("Commande incorrecte : ", command)
                            print("")
                            user_input="La commande que tu as exécutée: "+command +" est incorrecte. \nVoici le message d'erreur : "+output.stdout.decode()+"\nRectifie ta commande selon les instructions de la function command"
#                            conversations.append({"role": "user", "content": user_input})
                            response = await create_chat_completion(user_input)
                            assistant_response = response['choices'][0]['message']['content']
#                            conversations.append({"role": "assistant", "content": assistant_response})
##                            conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
                            messages=instructions+conversations
                            #print("\n\033[1mAssistant:\033[0m ", assistant_response)
                        try:
                            output = subprocess.run(""+search('tahoma') +" "+ command.lower().replace('command: tahoma ', '') +"", shell=True, capture_output=True)
#                            print("Code de retour:", output.returncode)
                            if "version" in output.stdout.decode() or "exist" in output.stdout.decode() or "exact" in output.stdout.decode():
                                await erreur_action() 
                            elif output.returncode == 0:
                                print("\nExécution de la commande :", command.replace('command: ',''))
                                print("Résultat de la commande :", output.stdout.decode())
#                                conversations.append({"role": "assistant", "content": "La commande : '"+command+"' a fonctionné." })
##                                conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: 'La commande : '"+command+"' a fonctionné.'"})
                                messages=instructions+conversations
                            else:
                                await erreur_action()
                        except:
                            output = subprocess.run("python3 '"+search('tahoma.py') +"' "+ command.lower().replace('command: tahoma ', '') +"", shell=True, capture_output=True)
#                            print("Code de retour:", output.returncode)
                            if "version" in str(output.stdout.decode()) or "exist" in str(output.stdout.decode()):
                                await erreur_action()
                            elif output.returncode == 0:
                                print("\nExécution de la commande :", command.replace('command: ',''))
                                print("Résultat de la commande :", output.stdout.decode())
#                                conversations.append({"role": "assistant", "content": "La commande : '"+command+"' a fonctionné." })
##                                conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: 'La commande : '"+command+"' a fonctionné.'"})
                                messages=instructions+conversations
                            else:
                                await erreur_action()
                            print(conversations)
                    except Exception as e:
                        print(e)
                        user_input="La commande que tu as exécutée: "+command +" retourne l'erreur suivante :\n"+str(e)
#                        conversations.append({"role": "user", "content": user_input})
                        print("\nCommande incorrecte : \n", command)
                        response = await create_chat_completion(user_input)
                        assistant_response = response['choices'][0]['message']['content']
#                        conversations.append({"role": "assistant", "content": assistant_response})
##                        conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
                        messages=instructions+conversations
#                    print(conversations)
                else:
                    # Affiche la réponse de ChatGPT
                    assistant_response = response['choices'][0]['message']['content']
#                    conversations.append({"role": "assistant", "content": assistant_response})
##                    conversations.append({"role": "user", "content": "-Question user: '" + user_input + "' -Réponse assistant: '" + assistant_response + "'"})
                    messages=instructions+conversations
                    print("\n\033[1mAssistant:\033[0m ", assistant_response)
#            print(conversations[-1])
# Exécute la boucle de chat de manière asynchrone
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chat_loop())

main(model)
