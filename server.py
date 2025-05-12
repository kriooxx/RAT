import socket

HOST = '0.0.0.0'  # écoute sur toutes les interfaces réseau
PORT = 12345

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #liberer le port après une interruption
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serveur en attente de connexion sur {HOST}:{PORT}")

clients = []

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
                response = c.recv(4096).decode()
                print(f"[{addr}] Response : \n{response}")
            except:
                print(f"Failed to send to {addr}")


