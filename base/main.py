import socket 
import threading 

import rsa

choice = input("Do you want to host (1) or to connect (2)? ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.77",9999)) # hna n7ato locall ipv4 te3na
    server.listen()
    print("Server is listening...")

    client, _ = server.accept()
    print("Client connected")
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.77",9999)) #mostly we should specify his ip adrees bsa7 since locally f same pc ndiro the same ip
    print("Connected to server")
else:
    print("Invalid choice")
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(message.encode())
        print("You: " + message)
       


def receiving_messages(c):
    while True:
        message = c.recv(1024).decode()
        print("Partner: " + message)


threading.Thread(target=sending_messages, args=(client,))
threading.Thread(target=receiving_messages, args=(client,))