import socket
import threading
import rsa

# Generate RSA key pair
public_key, private_key = rsa.newkeys(2048)

choice = input("Do you want to host (1) or to connect (2)? ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.77", 9999))  # hna n7ato locall ipv4 te3na
    server.listen()
    print("Server is listening...")

    client, _ = server.accept()
    print("Client connected")

    # Exchange public keys
    client.send(public_key.save_pkcs1(format='PEM'))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.77", 9999)) #mostly we should specify his ip adrees bsa7 since locally f same pc ndiro the same ip
    print("Connected to server")

    # Exchange public keys
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1(format='PEM'))
else:
    print("Invalid choice")
    exit()

def sending_messages(c):
    while True:
        try:
            message = input("")
            if message == "/exit": 
                print("Disconnecting...")
                c.close()
                break
            encrypted_message = rsa.encrypt(message.encode(), public_partner)
            c.send(encrypted_message)
            print("You: " + message)
        except Exception as e:
            print(f"Error sending message: {e}")
            break


def receiving_messages(c):
    while True:
        try:
            encrypted_message = c.recv(1024)
            if not encrypted_message:
                print("Connection closed by partner.")
                break
            message = rsa.decrypt(encrypted_message, private_key).decode()
            print("Partner: " + message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    c.close()  


# Start threads for sending and receiving messages
if choice == "1":
    send_thread = threading.Thread(target=sending_messages, args=(client,))
    recv_thread = threading.Thread(target=receiving_messages, args=(client,))
    send_thread.start()
    recv_thread.start()
    send_thread.join() 
    recv_thread.join()  
elif choice == "2":
    send_thread = threading.Thread(target=sending_messages, args=(client,))
    recv_thread = threading.Thread(target=receiving_messages, args=(client,))
    send_thread.start()
    recv_thread.start()
    send_thread.join()  
    recv_thread.join() 

print("Program terminated.")