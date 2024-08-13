# server.py
import socket
import threading

clients = {}
usernames = {}

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith('/nick '):
                    username = message.split(' ', 1)[1]
                    usernames[client_socket] = username
                    clients[username] = client_socket
                    broadcast(f"{username} has joined the chat.")
                elif message.startswith('/msg '):
                    target_user, msg = message.split(' ', 2)[1:3]
                    if target_user in clients:
                        clients[target_user].send(f"Private from {usernames[client_socket]}: {msg}".encode('utf-8'))
                else:
                    broadcast(f"{usernames.get(client_socket, 'Unknown')}: {message}")
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    remove(client_socket)

def broadcast(message):
    for client in clients.values():
        try:
            client.send(message.encode('utf-8'))
        except:
            pass

def remove(client_socket):
    username = usernames.pop(client_socket, None)
    if username:
        clients.pop(username, None)
        broadcast(f"{username} has left the chat.")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    print("Server started on port 5555")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.send("Welcome to the chat server! Type /nick <username> to set your username.".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
