#!/bin/bash

# Function to download a file from URL
download_file() {
  local url=$1
  local filename=$2
  wget -O "$filename" "$url"
}

# Ask if the user wants to install venv
read -p "Do you want to install venv? (Yes/No): " install_venv

# Check user's response
if [[ $install_venv =~ ^(Oui|oui|OUI|Yes|yes|YES|O|o|Y|y)$ ]]; then
  python3 -m pip install virtualenv
else
  echo "Venv was not installed."
fi

# Ask for the installation directory path
read -p "Enter the installation directory path (default: ~/tahoma-gpt): " install_dir
install_dir=${install_dir:-"$HOME/tahoma-gpt"}

# Create the installation directory and navigate into it
mkdir -p "$install_dir"
cd "$install_dir"

# Download files from GitHub
download_file "https://github.com/pzim-devdata/tahoma/raw/main/requirements_tahoma-gpt.txt" "requirements_tahoma-gpt.txt"
download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma-gpt.py" "tahoma-gpt.py"
download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma_chatgpt.sh" "tahoma_chatgpt.sh"

# Install venv
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Ask if the user wants to install Tahoma
read -p "Do you want to install Tahoma? (Yes/No): " install_tahoma

# Check user's response
if [[ $install_tahoma =~ ^(Yes|yes|YES|O|o)$ ]]; then
  # Install Tahoma
  python3 -m pip install -U tahoma

  # Configure Tahoma
  echo ""
  tahoma -c

  # Get the list of devices
  echo ""
  tahoma -g

  sleep 6
fi

# Install dependencies
python3 -m pip install -r requirements_tahoma-gpt.txt

# Ask for the OpenAI API key
echo ""
echo "To get the OpenAI API key, please visit the OpenAI website: https://platform.openai.com/apps"
read -p "Enter the OpenAI API key: " openai_api_key

# Modify the tahoma-gpt.py file with the API key
sed -i "s|openai.api_key =.*|openai.api_key = '$openai_api_key'|" tahoma-gpt.py

# Ask if the user wants to create a desktop shortcut for Tahoma-GPT
read -p "Do you want to create a desktop shortcut for Tahoma-GPT? (Yes/No): " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')

if [[ $response == "yes" || $response == "y" ]]; then
    desktop_dir=$(xdg-user-dir DESKTOP)
    if [ "$desktop_dir" ]; then
        echo "[Desktop Entry]
Version=1.0
Type=Application
Name=Tahoma-GPT
Comment=Shortcut to run Tahoma-GPT
Icon=$(dirname "$(readlink -f "$0")")/tahoma-gpt.png
Exec='$(dirname "$(readlink -f "$0")")/tahoma_chatgpt.sh'
Terminal=true" > "$desktop_dir/tahoma-gpt.desktop"

        # Make the desktop shortcut executable
        chmod +x "$desktop_dir/tahoma-gpt.desktop"

        echo "The desktop shortcut for Tahoma-GPT has been created successfully and made executable."
    else
        echo "Could not find the Desktop directory, unable to install the shortcut."
    fi
fi

# Execute the tahoma-gpt.py script
python3 tahoma-gpt.py

# Deactivate the virtual environment
deactivate
