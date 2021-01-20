#imports
import socket
import threading

#ChatServer class
class ChatServer:

    clients_list = [] #maintain a list of the clients

    last_received_message = ""

    def __init__(self): #constructor that is called when object is instantiated
        self.server_socket = None
        self.create_listening_server()

    #listen for incoming connection
    def create_listening_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket using TCP port and ipv4
            local_ip = '127.0.0.1'
            local_port = 10319
            # this will allow you to immediately restart a TCP server
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # this makes the server listen to requests coming from other computers on the network
            self.server_socket.bind((local_ip, local_port))
            print("Waiting For Connections...")
            self.server_socket.listen(5) #listen for incoming connections / max 5 clients
            self.receive_messages_in_a_new_thread()
        except:
            print("Max limit of clients exceeded");


    #function to receive new messages
    def receive_messages(self, so):
        while True:
            try:
                incoming_buffer = so.recv(256) #initialize the buffer
                if not incoming_buffer:
                    break
                self.last_received_message = incoming_buffer.decode('utf-8')
                self.broadcast_to_all_clients(so)  # send to all clients
            except: #error handling
                print("A client has left the chat");
                break;
        so.close()


    #broadcast the message to all clients
    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket: #send the message to the clients except the client who has sent us the message
                try:
                    socket.sendall(self.last_received_message.encode('utf-8'))
                except:
                    socket.close();


    #receive messages
    def receive_messages_in_a_new_thread(self):
        while True:
            try:
                client = so, (ip, port) = self.server_socket.accept() #Server accepts connection
                self.add_to_clients_list(client) #add the client
                print('Connected to ', ip, ':', str(port)) #display on server side
                t = threading.Thread(target=self.receive_messages, args=(so,))
                t.start()
            except Exception as e:  #error handling
                print(e)
                

    #add a new client
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client) #add client to the list


if __name__ == "__main__":
    ChatServer()
