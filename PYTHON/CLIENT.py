# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, message + '\n')
            text_area.config(state=tk.DISABLED)
        except:
            break

def send_message(client_socket, entry):
    message = entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        entry.delete(0, tk.END)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    def on_send():
        send_message(client_socket, entry)

    def on_join_group():
        group = group_entry.get()
        if group:
            client_socket.send(f"/join {group}".encode('utf-8'))

    def on_set_nick():
        username = username_entry.get()
        if username:
            client_socket.send(f"/nick {username}".encode('utf-8'))

    # GUI setup
    root = tk.Tk()
    root.title("Chat Client")

    text_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    entry = tk.Entry(root)
    entry.pack(padx=10, pady=10, fill=tk.X)

    send_button = tk.Button(root, text="Send", command=on_send)
    send_button.pack(pady=5)

    username_entry = tk.Entry(root)
    username_entry.pack(padx=10, pady=5, fill=tk.X)
    set_nick_button = tk.Button(root, text="Set Nickname", command=on_set_nick)
    set_nick_button.pack(pady=5)

    group_entry = tk.Entry(root)
    group_entry.pack(padx=10, pady=5, fill=tk.X)
    join_group_button = tk.Button(root, text="Join Group", command=on_join_group)
    join_group_button.pack(pady=5)

    threading.Thread(target=receive_messages, args=(client_socket, text_area), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    start_client()

