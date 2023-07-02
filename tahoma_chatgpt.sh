#!/bin/bash
#Vous pouvez donner votre instruction tahoma directement en argument de ce script : "~/Bureau/tahoma_chatgpt.sh ferme les volets de la cuisine"
#You can give your Tahoma instruction directly as an argument to this script. "~/Desktop/tahoma_chatgpt.sh please close the kitchen shutters"

#$echo "$(dirname "$0")"
#cd 'foler/of/tahoma-gpt';
cd "$(dirname "$0")"
python3 -m venv env;
source env/bin/activate;


#Récupération des arguments
phrase=""
for word in "$@"; do
  phrase="$phrase$word "
done
#echo "$phrase"

python3 tahoma-gpt.py "$phrase"
