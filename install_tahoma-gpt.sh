#!/bin/bash

# Fonction pour télécharger un fichier depuis une URL
download_file() {
  local url=$1
  local filename=$2
  wget -O "$filename" "$url"
}

# Demander si l'utilisateur souhaite installer venv
read -p "Voulez-vous installer venv? (Oui/Non): " install_venv

# Vérifier la réponse de l'utilisateur
if [[ $install_venv =~ ^(Oui|oui|OUI|Yes|yes|YES|O|o)$ ]]; then
  python3 -m pip install virtualenv
else
  echo "Venv n'a pas été installé."
fi
# Demander l'emplacement du dossier d'installation
read -p "Entrez le chemin du dossier d'installation (par défaut: ~/tahoma-gpt): " install_dir
install_dir=${install_dir:-"$HOME/tahoma-gpt"}

# Créer le dossier d'installation et se déplacer dedans
mkdir -p "$install_dir"
cd "$install_dir"

# Télécharger les fichiers depuis GitHub
download_file "https://github.com/pzim-devdata/tahoma/raw/main/requirements_tahoma-gpt.txt" "requirements_tahoma-gpt.txt"
download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma-gpt.py" "tahoma-gpt.py"

# Installer venv
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate

# Demander si l'utilisateur souhaite installer tahoma
read -p "Voulez-vous installer tahoma? (Oui/Non): " install_tahoma

# Vérifier la réponse de l'utilisateur
if [[ $install_tahoma =~ ^(Oui|oui|OUI|Yes|yes|YES|O|o)$ ]]; then
  # Installer tahoma
  python3 -m venv env
  source env/bin/activate
  python3 -m pip install -U tahoma
  # Configurer tahoma
  echo ""
  tahoma -c
  # Obtenir la liste des appareils
  echo ""
  tahoma -g
  sleep 6
fi

# Installer les dépendances
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements_tahoma-gpt.txt

# Demander la clé API OpenAI
echo ""
echo "Pour la création de la clé API OpenAI rendez-vous sur le site d'OpenAI : https://platform.openai.com/apps"
read -p "Entrez la clé API OpenAI :" openai_api_key

# Modifier le fichier tahoma-gpt.py avec la clé API
sed -i "s|openai.api_key =.*|openai.api_key = '$openai_api_key'|" tahoma-gpt.py


# Exécuter le script tahoma-gpt.py
python3 -m venv env
source env/bin/activate
python3 tahoma-gpt.py



# Désactiver l'environnement virtuel
deactivate

