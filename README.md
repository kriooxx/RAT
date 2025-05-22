# 🕵️‍♂️ Python Remote Access Tool (RAT)

> 🎓 Projet réalisé dans le cadre d’un projet annuel scolaire – **à des fins strictement éducatives**.

---

## ⚠️ Disclaimer

Ce projet est fourni **uniquement** à des fins pédagogiques et de tests en environnement contrôlé.

🔒 **L’auteur décline toute responsabilité** en cas d’utilisation abusive, illégale ou non éthique du code fourni.  
**Vous êtes seul·e responsable** de votre usage de cet outil.

---

## 🚀 Fonctionnalités

Ce RAT (Remote Access Tool) développé en Python permet à un opérateur :

- 📡 D’exécuter des commandes shell à distance
- 🖼️ De capturer des captures d’écran (`screenshot`)
- 📷 De prendre une photo depuis la webcam (`webcam`)
- ⌨️ D’enregistrer les frappes clavier (`start_keylogger`)
- 📁 De transférer un ou plusieurs fichiers (`download`)
- 🔐 De récupérer les réseaux Wi-Fi + mots de passe (`wifi`)
- 🔑 D’extraire les mots de passe Firefox (`firefox_password`)
- 👁️ De lister les profils Firefox disponibles (`firefox_profiles`)
- 👥 De gérer plusieurs clients simultanément (**multi-client threading**)

---

## 🧱 Architecture

- `client.py` → Agent RAT à déployer sur la machine cible
- `server.py` → Serveur C2 (Command & Control) CLI ou Flask
- `firefox_decrypt.py` → Script embarqué pour extraire les credentials Firefox
- `templates/` → Fichiers HTML pour l’interface web Flask

---

## 💻 Commandes serveur disponibles

| Commande                      | Description                                      |
|------------------------------|--------------------------------------------------|
| `<cmd>`                 | Exécute une commande shell                      |
| `screenshot`                 | Capture d’écran du client                       |
| `webcam`                     | Capture photo via webcam                        |
| `start_keylogger`            | Lance un keylogger discret                      |
| `get_ip`                     | Affiche l’adresse IP du client                  |
| `generate_ssh_keypair`       | Génère une paire de clés SSH                    |
| `wifi`                       | Récupère les infos Wi-Fi enregistrées           |
| `firefox_profiles`           | Liste les profils Firefox                       |
| `firefox_password <id>`      | Extrait les mots de passe du profil Firefox     |
| `download <f1>;<f2>;...`     | Télécharge un ou plusieurs fichiers             |
| `disconnect`                 | Déconnecte proprement le client                 |
| `exit`                       | Quitte la session avec le client                |

---

## 🌐 Interface Web (optionnelle)

Une interface en Flask avec Bootstrap est disponible :

- 📋 Liste des clients connectés
- 🎮 Interface de contrôle par client
- 🔁 Rafraîchissement automatique toutes les 60s
- 🔐 Accès restreint possible via loopback ou future auth
- 📜 Historique des commandes/retours par client

---

## 👨‍🔧 Prérequis (client)

- **Python ≥ 3.8**
- 📦 Modules :
  - `paramiko`
  - `pynput`
  - `pyautogui`
  - `opencv-python`
  - `Pillow`
- 🐧 Sous Linux :
  - `libnss3` (pour Firefox)

### Installation rapide :
```bash
pip install -r requirements.txt
sudo apt install libnss3
