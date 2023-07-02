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
if [[ $install_venv =~ ^(Oui|oui|OUI|Yes|yes|YES|O|o|Y|y)$ ]]; then
  python3 -m pip install virtualenv
else
  echo "Venv n'a pas été installé."
fi
# Demander l'emplacement du dossier d'installation
echo ""
echo "Entrez le chemin du dossier d'installation :"
read -p "Ou presser Entrée pour installer dans : ~/tahoma-gpt " install_dir
install_dir=${install_dir:-"$HOME/tahoma-gpt"}

# Créer le dossier d'installation et se déplacer dedans
mkdir -p "$install_dir"
cd "$install_dir"

# Télécharger les fichiers depuis GitHub
download_file "https://github.com/pzim-devdata/tahoma/raw/main/requirements_tahoma-gpt.txt" "requirements_tahoma-gpt.txt"
download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma-gpt_french.py" "tahoma-gpt_french.py"
download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma_chatgpt.sh" "tahoma_chatgpt.sh"
download_file "https://raw.githubusercontent.com/pzim-devdata/tahoma/main/tahoma-gpt.png" "tahoma-chatgpt.png"

chmod +x "tahoma_chatgpt.sh"
chmod +x "tahoma-gpt_french.py"
chmod -x "tahoma-chatgpt.png"

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

# Modifier le fichier tahoma-gpt_french.py avec la clé API
sed -i "s|openai.api_key =.*|openai.api_key = '$openai_api_key'|" tahoma-gpt_french.py

# Demande à l'utilisateur s'il souhaite créer un raccourci bureau
read -p "Voulez-vous créer un raccourci bureau pour Tahoma-GPT ? (Oui/Non) " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
if [[ $response == "oui" || $response == "o" || $response == "yes" || $response == "y" ]]; then
    desktop_dir=$(xdg-user-dir DESKTOP)
    if [ "$desktop_dir" ]; then
        sed -i 's/tahoma-gpt.py/tahoma-gpt_french.py/g' tahoma_chatgpt.sh
        echo "[Desktop Entry]
        rm "$desktop_dir/tahoma-gpt.desktop"
Version=1.0
Type=Application
Name="Tahoma-GPT en français"
Comment=Raccourci pour exécuter Tahoma-GPT
Icon=$(dirname "$(readlink -f "$0")")/tahoma-chatgpt.png
Exec='$(dirname "$(readlink -f "$0")")/tahoma_chatgpt.sh'
Terminal=true" > "$desktop_dir/tahoma-gpt.desktop"
      chmod +x "$desktop_dir/tahoma-gpt.desktop"
      echo "Le raccourci bureau pour Tahoma-GPT a été créé avec succès et rendu exécutable. Les autres raccourcis ont été supprimés"
      echo "Le fichier $install_dir/tahoma_chatgpt.sh a été modifié pour lancer $install_dir/tahoma-gpt_french.py"
    else
      echo "Je n'ai pas trouvé le dossier Desktop, impossible d'installer le raccourci"
    fi
fi

# Exécuter le script tahoma-gpt_french.py
python3 -m venv env
source env/bin/activate
python3 tahoma-gpt_french.py

# Désactiver l'environnement virtuel
deactivate

