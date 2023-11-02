from asyncio.windows_events import NULL
from concurrent.futures import thread
import socket
import sys
import os
import threading

#TODO: implement a server socket and a client socket
#TODO: server socket will bind, listen, accept, loop thru recv, send; close
#TODO: client socket will connect, loop thru send, recv; close

host = socket.gethostbyname(socket.gethostname())
port = 5959
max_conn = 10
buffer_size = 1024
connections = []    #stored as (IP, Port) pairs
clients_list = []   #contains sockets as items

if len(sys.argv) == 2:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Bad value provided, defaulting to: {port}")
elif (len(sys.argv) > 2):
    print("you have used too many system arguments \n using program defaults")
        
#we'll use this socket to listen
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((host, port))
client_socket.listen(5)


#we'll use this socket to send messages out
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
def print_help():
    print("******************* Welcome to CrossTok *****************\n")
    print("In this application you can do the following:")
    print("MYIP: returns your IPv4 address")
    print("HELP: returns commands you can type to use the program")
    print("MYPORT: returns the port CrossTok is using to listen on")
    print("CONNECT <dest IP> <port #>: establishes TCP connection to the <dest IP> on <port #>")
    print("LIST: Display a numbered list of all connections CrossTok is using with an id number")
    print("TERMINATE: <connection id>: close connection denoted with <connection id>")
    print("SEND: <connection id> <message>: send a message to <connection id> with string <message>")
    print("CLS: clears the current screen")
    print("SOCKET: recreates the socket if a fatal error occured")
    print("EXIT: terminate CrossTok and all active connections\n")
    print("\n")  
    
def recieve_connections():
    while True:
        try:
            client, address = client_socket.accept()
            connections.append((address[0], address[1]))
            clients_list.append(client)
        except socket.error:
            print("something went wrong with an attempted connection")
    
def receive_messages():
    while True:
        try:
            message = client_socket.recv(buffer_size).decode()
            if message.startswith("EXIT"):                          #if user disconnected
                remove_id = client_socket.recvfrom(buffer_size)     #(ip, port) tuple
                try:
                    connections.remove(remove_id)
                except ValueError:
                    print("a user tried to disconnect who did not exist in the connections list")
            else:
                print(message)
        except Exception as e:
            print(f"Error: {e}")
            print("socket must close, you will have to recreate the socket")
            client_socket.close()
            break

def send_message(message: str, client: socket):
    # encode and send the message
    client.send(message.encode())
    print("debug")

#new
# TODO: get send to work

#old
# TODO: make connect and list work
# TODO: list should find all unique connected clients, store conn list in list
# TODO: new connections establishing TCP link should be checked against list, then added if unique
# TODO: connect should ping the target ip with TCP connection request which triggers addition to the connected clients list

def main():
    # create the thread for handeling new connections
    thread1 = threading.Thread(target=recieve_connections)
    thread1.start()
    # create the thread for handeling new messages
    
    # create the clear string lambda function and print the help screen for users to get started
    clear = lambda: os.system('cls' if os.name == 'nt' else clear)
    print_help()
    
    while True: 
        
        # split the user input into substrings based on spaces
        print("CMD: ", end='')  
        user_choice = input()
        user_choice = user_choice.split()
        user_choice[0] = user_choice[0].upper()
        
        # user command branch
        if (user_choice[0] == "MYIP"):
            print("Your IP Address: " + host)
        elif (user_choice[0] == "MYPORT"):
            print("Your port: " + str(port))
        elif (user_choice[0] == "HELP"):
            print_help()
        elif (user_choice[0] == "CONNECT"):
            if (len(user_choice) == 3):
                target_ip = user_choice[1]
                try:
                    target_port = int(user_choice[2])
                    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    connection_socket.connect((target_ip, target_port))                         #failed due to str cannot be interpreted as integer
                    connection_socket.send("connection attempt".encode())
                    connections.append((target_ip, target_port))
                    print(f"Successfully Connected to : {target_ip}:{target_port}")
                    #thread2 = threading.Thread(target=receive_messages)
                    #thread2.start()
                except ValueError:
                    print("please ensure you are using the correct format for ip and port")
                except socket.gaierror:
                    print(f"invalid address or hostname: {target_ip} {target_port}")
                except socket.timeout:
                    print("connection timed out")
                except ConnectionRefusedError:
                    print("the user you targeted refused your connection")
                except Exception as e:
                    print(f"Unknown Failure {e}")
            else:
                print("\nplease see the help menu for information on how to use the connect command")
        elif (user_choice[0] == "LIST"):
            print("Connection list: ")
            for i, (conn_ip, conn_port) in enumerate(connections, start=0):
                print(f"ID: {i} IP: {conn_ip} Port: {conn_port}")
        elif (user_choice[0] == "TERMINATE"):
            try:
                conn_id = int(user_choice[1])
                conn_ip, conn_port = connections[conn_id]
                print("Terminating connection with: " + conn_id)
                connections.pop(conn_id)
            except Exception as e:
                print("Did you enter an ip or wrong number? Try entering a valid connection\nCheck out LIST for valid entries")
        elif (user_choice[0] == "SEND"):
            try:
                if (int(user_choice[1]) in range(len(connections))):
                    conn_id = int(user_choice[1])
                    conn_ip, conn_port = connections[conn_id]
                    message = " ".join(user_choice[2:])
                    print(f"Sending to {conn_id}...")
                    send_message(message, clients_list[int(user_choice[1]) - 1])
                else:
                    print("please select a value in range of the id's listed")
            except Exception as e:
                print(f"Uh-oh, looks like something went wrong!\nCheck the id you entered and try again!\n{e}")
        elif (user_choice[0] == "CLS"):
            clear()
        elif (user_choice[0] == "SOCKET"):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.bind((host, port))
            client_socket.listen(5)
        elif (user_choice[0] == "EXIT"):
            try:
                client_socket.sendall("EXIT".encode())
                client_socket.close()
                for connection in connections:
                    connections.remove()
                print(f"Connections closed.")
            except:
                print("nothing connected")
            print("Sorry to see you go!")
            quit()
        else:
            print("\n\nERROR: invalid entry\n\n")

if __name__ == "__main__":
    main()
