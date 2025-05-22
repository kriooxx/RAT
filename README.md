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
- 👥 **Contrôle multi-clients simultanés** (thread safe + menu interactif)

---

## 🧱 Architecture

- **`client.py`** : l’agent RAT installé sur la machine cible
- **`server.py`** : le serveur C2 (Command & Control) contrôlé par l’opérateur
- **`firefox_decrypt.py`** : outil intégré pour extraire les mots de passe Firefox

---

## 💻 Commandes disponibles (depuis le serveur)

| Commande                      | Description                                      |
|------------------------------|--------------------------------------------------|
| `exec <commande>`            | Exécute une commande shell sur le client        |
| `screenshot`                 | Capture d’écran locale                          |
| `webcam`                     | Capture photo via webcam                        |
| `start_keylogger`            | Lance un keylogger en tâche de fond             |
| `get_ip`                     | Affiche l'adresse IP locale du client           |
| `generate_ssh_keypair`       | Génère une paire de clés SSH                    |
| `wifi`                       | Récupère les réseaux Wi-Fi + mots de passe      |
| `firefox_profiles`           | Affiche les profils Firefox disponibles         |
| `firefox_password <id>`      | Extrait les mots de passe du profil Firefox     |
| `download <f1>;<f2>;...`     | Télécharge un ou plusieurs fichiers du client   |
| `disconnect`                 | Ferme proprement la session avec un client      |
| `exit`                       | Quitte le mode client et retourne au menu       |

---

## 🧑‍💻 Interface multi-clients

- Liste dynamique des clients connectés
- Contrôle interactif d’un client à la fois
- Possibilité de **retourner au menu principal**
- Déconnexion propre et gestion des sockets avec `threading.Lock`

---

## 🛠️ Prérequis (client)

- Python 3.8+
- Modules :
  - `paramiko`
  - `pynput`
  - `pyautogui`
  - `opencv-python`
  - `Pillow`
- Linux uniquement :
  - `libnss3` (pour le support de Firefox)

Installation :

```bash
pip install -r requirements.txt
sudo apt install libnss3
