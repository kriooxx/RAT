# RAT


# 🕵️‍♂️ Python Remote Access Tool (RAT)

> 📌 Projet réalisé dans le cadre d'un projet annuel scolaire – **à des fins exclusivement éducatives**.

---

## ⚠️ Disclaimer

**Ce projet est fourni uniquement à des fins éducatives.**  
Son usage est strictement réservé à un environnement de test ou de démonstration contrôlé.

⚠️ **Je décline toute responsabilité si ce code est utilisé à des fins illégales ou non éthiques.**  
Vous êtes seul·e responsable de ce que vous en faites.

---

## 📦 Fonctionnalités

Ce RAT (Remote Access Tool) développé en Python permet :

- 📡 Exécution de commandes shell à distance (`exec`)
- 🖼️ Capture d’écran (`screenshot`)
- 📷 Capture photo depuis la webcam (`webcam`)
- 📝 Enregistrement des frappes clavier (`start_keylogger`)
- 📁 Transfert de fichiers (`download`)
- 🔐 Récupération des mots de passe Wi-Fi (`get_wifi_creds`)
- 🔑 Extraction des mots de passe Firefox (`get_firefox_passwords`)
- 👁️ Liste des profils Firefox (`get_firefox_profiles`)

---

## 🧱 Architecture

- **client.py** : l’agent RAT installé sur la machine cible
- **server.py** : le centre de commande (C2) contrôlé par l’opérateur
- **firefox_decrypt.py** : script tiers intégré pour déchiffrer les mots de passe Firefox

---

## 💻 Commandes supportées (depuis le serveur)

| Commande                      | Description                                      |
|------------------------------|--------------------------------------------------|
| `exec <commande>`            | Exécute une commande shell sur le client        |
| `screenshot`                 | Capture d’écran locale                          |
| `webcam`                     | Capture photo via webcam                        |
| `start_keylogger`            | Lance un keylogger en tâche de fond             |
| `get_ip`                     | Renvoie l'adresse IP locale du client           |
| `generate_ssh_key`           | Génère une paire de clés SSH                    |
| `get_wifi_creds`             | Récupère les réseaux Wi-Fi enregistrés + PSK    |
| `get_firefox_profiles`       | Affiche les profils Firefox disponibles         |
| `get_firefox_passwords <n>`  | Extrait les mots de passe du profil choisi      |
| `download <f1>;<f2>;...`     | Télécharge un ou plusieurs fichiers du client   |

---

## 🛠️ Prérequis

Côté client :
- Python 3.8+
- Modules : `paramiko`, `pynput`, `pyautogui`, `opencv-python`, `libnss3` (Linux)

Installation :
```bash
pip install -r requirements.txt
sudo apt install libnss3

