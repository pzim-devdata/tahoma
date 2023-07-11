@echo off
rem Vous pouvez donner votre instruction Tahoma directement en argument de ce script :
rem "C:\tahoma-gpt\tahoma_chatgpt.bat ferme les volets de la cuisine"
rem You can give your Tahoma instruction directly as an argument to this script.
rem "C:\tahoma-gpt\tahoma_chatgpt.bat please close the kitchen shutters"

rem Déplacement vers le dossier contenant le script
set curdir=%~dp0
cd /d "%curdir%"

rem Activation de l'environnement virtuel Python
call env\Scripts\activate

rem Récupération des arguments
set phrase=
:loop
if "%~1"=="" goto run
set phrase=%phrase% %1 
shift
goto loop
:run

rem Lancement du script tahoma-gpt.py avec l'instruction Tahoma
python tahoma-gpt.py %phrase%
