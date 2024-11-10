import socket
import threading

# Asking for a nickname
nickname = input("Please choose your nickname, this will be shown for everyone in the chatroom.:")

# Clients call to connect to server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 1212))


def receiving():

    """
    This function mirrors the incoming messages from the server to the client

    This function runs in a loop, and keeps recieving messages from the server, it checks for
    NICK to validate if it's the users message or another clients message. If it's another clients 
    message, it prints the message directly to the terminal. If it's the users message it sends the message
    to the other clients
   
    If any error would occur, it prints an error message with the type of error. 
    """
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except Exception as e:
            print(f"Sorry, we seem to have run into an error: {e}")
            client.close()
            break

   
def write():
    
    """
    This function takes the users input, formats it with their nickname, encodes it 
    and sends the encoded formatted message to the server.  
    
    Note: 
        This function uses the global nickname, which will be the user's nickname when connecting.


    """
    
    while True:
            message = f"{nickname}: {input('')}"
            client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receiving) # Startíng thread for receiving function
receive_thread.start()

write_thread = threading.Thread(target=write) # Starting thread for write function
write_thread.start()