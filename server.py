import socket
import threading

HOST = "127.0.0.1"
PORT = 1212



# Starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()



# initalizing empty lists for both clients and their nicknamnes
clients = []
nicks = []



#broadcasting a message to all clients using a simple for loop
def broadcast(message):
    for client in clients:
        client.send(message)

    

def manage_message(client):
    """
    This function manages messages for clients

    I have decided to run this function in a seperate thread
    for each client, to recieve and broadcast them to all the connected clients. 
    It also handles client dissonnections, and ensures the client is removed from the list 
    of connected clients.  
    
    Args:
        the clients socket connection
    """
    while True:
    # Receiving client message
        try:
            message = client.recv(2048)
            broadcast(message)
        # Handling client dissconnection
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicks[index]
            broadcast(f"{nickname} has dissconnected!".encode("utf-8"))
            nicks.remove(nickname)
            break


   

def receiving():
    """ 
    Main function, this ensures we accept new clients.

    This function runs in a loop, it makes sure to take on new
    clients and starts a thread for each new client to handle their messages.
    This function also takes care of inital contact, and broadcasts all news to 
    all the connected clients. 
    """
    while True:
        
        client, address = server.accept()
        print(f"You have successfully connected with {str(address)}")

        # Make sure to recieve a nickname from client. 
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(2048).decode("utf-8")
        nicks.append(nickname)
        clients.append(client)

        # Inform everyone that a new client has connected
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} has now joined the chat!".encode("utf-8"))
        client.send("Connected to server!".encode("utf-8"))

        thread = threading.Thread(target=manage_message, args=(client,))
        thread.start()


print(f"Server is now starting on {HOST}:{PORT}")
receiving()
