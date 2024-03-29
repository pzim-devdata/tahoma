Tahoma est une API simple pour contrôler les appareils Somfy Tahoma en utilisant Python 3, grâce à l'API pyoverkiz. Avec seulement trois mots, vous pouvez contrôler vos appareils. 
Elle a été initialement créée pour Tahoma mais fonctionne également avec Somfy Connectivity Kit, Connexoon, et Cozytouch.


![Somfy](https://www.voletsdusud.com/wp-content/uploads/2018/04/logo-tahoma.jpg)



[ ![Licence GitHub](https://img.shields.io/github/license/pzim-devdata/tahoma?style=plastic)](https://github.com/pzim-devdata/tahoma/blob/main/LICENSE) ![](https://img.shields.io/badge/Works%20with-Python%203-red?style=plastic) ![GitHub issues](https://img.shields.io/github/issues/pzim-devdata/tahoma?style=plastic) [](https://github.com/pzim-devdata/tahoma/issues) ![GitHub repo size](https://img.shields.io/github/repo-size/pzim-devdata/tahoma?style=plastic) [ ![Visits Badge](https://badges.strrl.dev/visits/pzim-devdata/tahoma)](https://badges.strrl.dev) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/pzim-devdata/tahoma?style=plastic) [ ![GitHub commits](https://img.shields.io/github/commits-since/pzim-devdata/tahoma/v2.2.0.svg?style=plastic)](https://GitHub.com/pzim-devata/tahoma/commit/)    
<!---
CE TAG NE FONCTIONNE PAS, N'Y FEREZ PAS CONFIANCE : ![GitHub All Releases](https://img.shields.io/github/downloads/pzim-devdata/tahoma/total?style=plastic) 
-->
[![Downloads](https://static.pepy.tech/personalized-badge/tahoma?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20downloads)](https://pepy.tech/project/tahoma)  

<a href="https://github.com/pzim-devdata/tahoma" title="Click here to access the English version of the site"><img src="https://cdn.countryflags.com/thumbs/united-kingdom/flag-round-250.png" width="30" height="30" alt="British flag"></a>

# Fonctionnalités

![GifTahoma.gif](GifTahoma.gif)


- Contrôlez les appareils Somfy Tahoma avec une API simple écrite en Python 3
- Créez des scripts ou des raccourcis pour contrôler votre maison depuis un serveur domestique ou votre ordinateur
- Avec cette API, vous pouvez intégrer les produits Somfy avec d'autres appareils compatibles Matter
- Fonctionne avec Somfy Connectivity Kit, Connexoon, Cozytouch et plus encore
- Prend en charge différents appareils Somfy : alarme, volet, prise, chauffage, capteurs, scènes, etc.
- Compatible avec les systèmes d'exploitation Windows et Linux
- 100 % fonctionnel avec ChatGPT


# Processus facile pour tester et installer Tahoma et Tahoma-GPT

Si vous souhaitez installer Tahoma et Tahoma-GPT à l'aide d'un script simple sous Linux, suivez ces étapes :

1. Ouvrez votre terminal et accédez au répertoire dans lequel vous souhaitez télécharger le script `install_tahoma-gpt.sh`.

   Par exemple :
   - `mkdir $HOME/tahoma-gpt`
   - `cd $HOME/tahoma-gpt`

3. Téléchargez le script `install_tahoma-gpt_french.sh` en utilisant la commande suivante :

   - `wget -O "install_tahoma-gpt_french.sh" "https://github.com/pzim-devdata/tahoma/raw/main/install_tahoma-gpt_french.sh"`

5. Rendez le script d'installation exécutable en exécutant la commande suivante :

   - `chmod +x install_tahoma-gpt_french.sh`
    
6. Exécutez le script d'installation dans le terminal en utilisant la commande suivante :

   - `bash -c './install_tahoma-gpt_french.sh'`

7. Vous pouvez maintenant démarrer tahoma-gpt_french.py dans un environnement virtuel :

   - `cd $HOME/tahoma-gpt` (ou accédez au dossier d'installation avec le terminal)
   - `python3 -m venv env`
   - `source env/bin/activate`
   - `python3 tahoma-gpt_french.py`
   
     Si vous souhaitez exécuter tahoma sans tahoma-gpt dans le même environnement virtuel :
     
   - `python3 tahoma.py` et suivez les instructions [ici](https://github.com/pzim-devdata/tahoma/blob/main/README_FR.md#4-récupérez-vos-commandes-personnelles)

     Vous pouvez également exécuter des commandes en tant qu'arguments :
     
   - `python3 "tahoma-gpt_french.py" Pourrais-tu ouvrir les volets dans la cuisine ?` 

En suivant ces étapes, Tahoma et Tahoma-GPT seront installés sur votre système Linux dans un environnement virtuel.


# Processus étape par étape pour tester et installer Tahoma et Tahoma-PGT

Vous pouvez créer un environnement virtuel en Python si vous souhaitez d'abord le tester. Tout sera installé dans le répertoire tahoma-gpt.

Tout d'abord, vous devez installer venv : `pip install virtualenv` ou `python3 -m pip install virtualenv` ou `pipx install virtualenv` pour installer l'environnement virtuel.
1. Créez un répertoire contenant `tahoma-gpt_french.py` et `requirements_tahoma-gpt.txt` à l'intérieur

. Téléchargez-les depuis [ici](https://github.com/pzim-devdata/tahoma/blob/main/requirements_tahoma-gpt.txt) et [ici](https://github.com/pzim-devdata/tahoma/blob/main/tahoma-gpt_french.py).

2. Ouvrez un terminal.

3. Accédez au répertoire que vous venez de créer.

4. Exécutez : `python3 -m venv env` (Windows : `virtualenv --python C:\Chemin\Vers\Python\python.exe venv`)

5. Exécutez : `source env/bin/activate` (Windows : `.\venv\Scripts\activate`)

6. Installez Tahoma et configurez-le (si ce n'est pas déjà fait) :

    6.1. Exécutez : `python3 -m pip install -U tahoma`

    6.2 Configurez Tahoma : `tahoma -c`

    6.3 Obtenez la liste de vos appareils : `tahoma -g`

7. Exécutez : `python3 -m pip install -r requirements_tahoma-gpt.txt`

8. Modifiez le script `tahoma-gpt_french.py` avec un éditeur de texte pour ajouter la clé API OpenAI

9. Exécutez : `python3 tahoma-gpt_french.py`

10. Jouez avec Tahoma et ChatGPT.

11. Exécutez : `exit` (pour quitter tahoma-gpt)

12. Exécutez : `exit()` (pour quitter Python)

11. Exécutez : `deactivate` (pour désactiver l'environnement virtuel)


![Image tahoma-gpt](https://github.com/pzim-devdata/tahoma/blob/main/picture_tahoma-gpt.png)


(Ceci est un tutoriel rapide)

##############################################################################

# Installation depuis ce dépot Git de tahoma
**Note:** Il s'agit d'une version portable à télécharger directement. Il ne s'agit pas d'un paquetage installé. Pour lancer l'application, il suffit d'exécuter `python3 tahoma.py` dans votre dossier importé. Si vous voulez installer le paquet en utilisant PyPI (version pip), allez à : [Comment installer tahoma avec pip ?](https://github.com/pzim-devdata/tahoma/blob/main/README_FR.md#installer-le-paquet-principal-) ou visitez directement le [site Pypi du projet](https://pypi.org/project/tahoma/#description) pour un processus d'installation plus facile.

Si vous aimez ce programme, veuillez lui attribuer une étoile sur GitHub pour améliorer la visibilité de Tahoma et permettre à d'autres personnes d'en bénéficier. :star :

# Démarrage rapide

#### 1. Télécharger
Télécharger le fichier zip et l'extraire dans un dossier choisi :

[Download :inbox_tray:](https://github.com/pzim-devdata/tahoma/releases/latest/download/tahoma.zip)

#### 2. Installer les dépendances
Exécutez les commandes suivantes dans votre dossier importé :


- `python3 -m pip install -r requirements.txt` afin d'installer les dépendances
et
- `python3 tahoma.py` pour s'assurer que Tahoma démarre.

#### 3. Configurer
Il n'y a que deux commandes à exécuter une fois pour configurer Tahoma :

Tous les détails sont expliqués dans `python3 tahoma.py --help-french` et `python3 tahoma.py --info`.


1. Spécifiez vos informations de connexion Somfy-connect et choisissez le serveur Somfy : :

- `python3 tahoma.py --configure` ou `python3 tahoma.py -c`

2.  Récupérez la liste de vos appareils Somfy personnels : :

- `python3 tahoma.py --getlist` ou `python3 tahoma.py -g`

#### 4. Récupérez vos commandes PERSONNELLES 
**USAGE:** `python3 tahoma.py [ACTION] [CATEGORIES] [NOM]`

Par exemple : `tahoma open shutter kitchen` ou `tahoma ouvrir volet cuisine`

Pour retrouver vos commandes personnelles, vous pouvez utiliser les options suivantes :

1. Lister toutes les [ACTIONS] possibles pour chaque [CATEGORIES] : 

- `python3 tahoma.py --list-actions` ou `tahoma -la`
ou
- `python3 tahoma.py --list-actions-french` ou `tahoma -laf`
 
2. Liste des [CATEGORIES] disponibles :

- `python3 tahoma.py --list-categories` ou `tahoma -lc`
ou 
- `python3 tahoma.py --list-categories-french` ou `tahoma -lcf`

3. Récupérez les [NOMS] que vous avez assignés à vos appareils personnels dans l'application Somfy :

- `python3 tahoma.py --list-names` ou `tahoma -ln`
ou
- `python3 tahoma.py --list-names-french` ou `tahoma -lnf`


Vous êtes maintenant prêt à utiliser tahoma

Pour plus d'informations, consultez `python3 tahoma.py -h` ou `python3 tahoma.py -i` 



# Cas d'usage : 
**Utilisation:** `python3 tahoma.py [ACTION] [CATEGORIE] [NOM]`

Par exemple : `tahoma open shutter kitchen` ou `tahoma ouvrir volet cuisine`


- Vous pouvez spécifier le niveau de fermeture des volets ou des écrans solaires avec une valeur numérique en tant qu'ACTION.

Par exemple, pour fermer un volet ou un pare-soleil à 25 % : 

`tahoma 25 shutter kitchen`
`tahoma 25 sunscreen kitchen`.

Veuillez noter que cette fonction ne fonctionne qu'avec les protocoles IO et non avec RTS.

- Vous pouvez utiliser un mot unique : `bath` ou le nom complet d'un dispositif entre crochets `[""]` : `["bath 1st floor"]`) comme paramètre NAME.

Par exemple :

`tahoma ouvrir volet jardin`

`tahoma arme l'alarme ["porte du jardin"]`

- Plusieurs commandes peuvent être exécutées dans le même processus sans redémarrer Tahoma. 

Par exemple : 

`tahoma arm alarm garden open shutter ["room 6"] confort heater dining off plug office 25 sunscreen kitchen launch scene morning`

- Il existe également une fonctionnalité d'attente avec `wait for` ou `sleep for` ou `attendre pendant` :

Par exemple : 

`tahoma ouvrir volet cuisine attendre pendant 20 fermer volet cuisine`

- Comme il est impossible d'arrêter un périphérique RTS en cours d'execution, vous pouvez annuler la commande précédente immédiate (sans affecter une commande "attendre pendant <SECONDES>"). Pour cela, utilisez la commande "cancel last action" ou "annuler précédente commande" juste après une commande qui ouvre ou ferme un périphérique RTS.

Par exemple :

`tahoma ouvrir volet cuisine attendre pendant 2 annuler precedente commande` : Cela va arreter le volet de la cuisine après 2 secondes

`tahoma ouvrir volet cuisine ouvrir volet chambre6 annuler precedente commande` : Cela va seulement arreter le volet de la chambre 6


# Exemples :
Voici quelques exemples de commandes :

- tahoma ouvrir volet cuisine
- tahoma 25 volet Velux3 (Ferme le volet à 25%)
- tahoma etat capteur ["Luminance sensor garden"] (Vous pouvez utiliser le nom complet du dispositif avec `["<NOM>"]`)
- tahoma obtenir capteur door (Fournit des informations sur tous les capteurs nommés "door" dans la maison)
- tahoma recuperer capteur ["Porte d'entrée"] 
- tahoma on prise bureau
- tahoma ouvrir volet ["chambre 6"]
- tahoma armer alarme jardin
- tahoma confort chauffage manger
- tahoma get sensor ["chauffage salle à manger"]
- tahoma lancer scenario matin
- tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]
- tahoma confort chauffage manger attendre pour 3 recup capteur ["Chauffage salle à manger"]
- tahoma ouvrir volet cuisine ouvrir volet chambre6 attendre pendant 10 annuler precedente commande` : Cela va seulement arreter le volet de la chambre 6 après 10 secondes




# Créer un PATH vers tahoma :

Pour pouvoir lancer tahoma directement dans le terminal, sans aller au dossier source, vous devez ajouter le dossier de tahoma au PATH :

En faisant cela, au lieu de taper `python3 '/place/du/dossier/source/tahoma/tahoma.py ouvrir volet cuisine'`,

 vous pourrez directement taper dans le terminal : `tahoma ouvrir volet cuisine`.


Ensuite, exécutez tahoma comme ceci : `tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]` et c'est tout !


## Sous Linux :

Sous Linux, on peut le faire en permanence en exécutant : `sudo gedit ~/.bashrc` et en ajoutant, à la fin du document, cette ligne :

`export PATH=$PATH:/place/du/dossier/source/tahoma`


Si vous voulez le tester temporairement avant, vous pouvez simplement exécuter cette commande dans le terminal : 

`export PATH=$PATH:/place/du/dossier/source/tahoma` 

Il sera restauré au prochain redémarrage.

Vous devez également renommer `tahoma.py` en `tahoma`

Ensuite, exécutez tahoma comme ceci : `tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]` et c'est tout !


## Sur Windows :

[Comment créer un PATH sous Windows](https://www.computerhope.com/issues/ch000549.htm)

Grâce au programme ``tahoma.exe``, vous pourrez exécuter tahoma en entrant cette commande : ``tahoma`` au lieu de ``python3 tahoma.py`` sur Windows 10. Ne fonctionne pas avec Windows 11 depuis la derniere mise à jour.

Ensuite, exécutez tahoma comme ceci : `tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]` et c'est tout !


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

SI VOUS VOULEZ INSTALLER LE PAQUET UTILISEZ PyPi (version pip) :

# Installer le paquet principal :
[Site du projet PyPi](https://pypi.org/project/tahoma/#description)

Installer tahoma :

``python
sudo python3 -m pip install -U tahoma
``

! !! Il est très important d'utiliser la commande `sudo` car de cette façon tahoma peut stocker vos logins dans un endroit sûr.



# Configurer :



C'est très facile à configurer, il y a juste deux commandes à exécuter une fois pour toutes la première fois

Tout est expliqué dans tahoma --help-french et tahoma --info


1. Spécifiez votre login Somfy-connect et choisissez le serveur Somfy (la commande `sudo` est nécessaire) :


- `sudo tahoma --configure` ou `sudo tahoma -c`

2. Configurez l'API et obtenez la liste de vos appareils Somfy personnels (la commande `sudo` est également requise) :


- `sudo tahoma --getlist` ou `sudo tahoma -g`


3. Et maintenant, vous êtes prêt à utiliser tahoma :


# Utilisation : `tahoma [ACTION] [CATEGORIE] [NOM]`


Par exemple : `tahoma open shutter kitchen` ou `tahoma ouvrir volet cuisine`

Vous pouvez également fermer un volet ou un écran solaire à un niveau spécifique. Par exemple, pour fermer à 25%, vous pouvez utiliser les commandes : `tahoma 25 shutter kitchen` ou `tahoma 25 sunscreen kitchen`. Veuillez noter que cette fonction ne fonctionne qu'avec les protocoles IO et non avec RTS.

Vous pouvez également exécuter plusieurs commandes au cours du même processus sans redémarrer tahoma ;

Par exemple : `tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]`



# Mais d'abord, vous devez récupérer vos commandes PERSONELLES :


## Obtenir une liste de toutes les [ACTIONS] possibles pour chaque [CATEGORIES] : 


- `tahoma --list-actions` ou `tahoma -la`

ou

- `tahoma --list-actions-french` ou `tahoma -laf`
 
 
 
## Obtenir une liste des [CATEGORIES] disponibles  :


- `tahoma --list-categories` ou `tahoma -lc`

ou 

- `tahoma --list-categories-french` ou `tahoma -lcf`



## Récupérez les [NOMS] que vous avez donnés à vos appareils personnels dans l'application Somfy :


- `tahoma --list-names` ou `tahoma -ln`

ou

- `tahoma --list-names-french` ou `tahoma -lnf`



Pour plus d'informations `tahoma -hf` ou `tahoma -i` 



# Créer un PATH vers tahoma :


Sous Linux, si vous avez installé tahoma sans la commande `sudo`, vous devrez créer un PATH pour lancer tahoma avec la commande `tahoma`.

En effet, pour pouvoir lancer tahoma directement dans le terminal, sans passer par le paquet source, vous devez ajouter le dossier de tahoma au PATH :

Cela peut être fait de manière permanente en exécutant : `sudo gedit ~/.bashrc` et en ajoutant, à la fin du document, cette ligne :

`export PATH=$PATH:/place/du/dossier/source/tahoma`



Si vous voulez le tester temporairement avant, vous pouvez simplement exécuter cette commande dans le terminal : 

`export PATH=$PATH:/place/du/dossier/source/tahoma` 

Il sera restauré au prochain redémarrage.



En faisant cela, au lieu de taper `python3 '/place/du/dossier/source/tahoma/tahoma.py ouvrir volet cuisine'`,

 vous pourrez taper directement dans le terminal : `tahoma ouvrir volet cuisine`.


Ensuite, exécutez tahoma comme ceci : `tahoma activer alarme jardin attendre pendant 10 ouvrir volet chambre6 attendre for 7 confort chauffage manger eteindre prise bureau 25 rideau cuisine lancer scenario matin obtenir capteur ["salle à manger"]` et c'est tout !




-------------------------------------------------------------------------------------

Pour :


Kit de connectivité Somfy
Somfy Connexoon IO
Somfy Connexoon RTS
Somfy TaHoma
Somfy TaHoma Beecon
Somfy TaHoma Switch
Thermor Cozytouch
Et plus encore...

Appareils pris en charge :
Alarme
Volet
Rideaux
Chauffage
Capteur
Scenarios
et plus encore si vous me demandez sur github : 

[@pzim-devdata GitHub Pages](https://github.com/pzim-devdata/tahoma/issues)
