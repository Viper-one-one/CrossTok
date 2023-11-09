import socket
import sys
import threading

thread_stop1 = False
thread_stop2 = False
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
    print("EXIT: terminate CrossTok and all active connections\n")
    print("\n")  
    
def recieve_connections():
    global socket
    global thread_stop1
    while not thread_stop1:
        try:
            client, address = client_socket.accept()
            if (address not in clients_list):
                connections.append((address[0], address[1]))
                clients_list.append(client)
                print("a new user has connected")
                thread2 = threading.Thread(target=receive_messages, args=(client,))
                thread2.start()
            else:
                print("user you connected to tried to connect again")
        except RuntimeError:
            print("\nruntime error with the message handler")
        except socket.error:
            if (not thread_stop1):
                print("\nsomething went wrong with an attempted connection")
    thread_stop1 = False
    
def receive_messages(client: socket):
    global socket
    global thread_stop2
    while not thread_stop2:
        try:
            message = client.recv(buffer_size)
            message = message.decode()
            if (message.startswith("EXIT")):                          #if user sent disconnect message
                try:
                    print(f"client {clients_list.index(client)} has closed connection")
                    connections.remove(client.getpeername())
                    clients_list.remove(client)
                    client.close()
                    thread_stop2 = True
                except ValueError:
                    print("\na user tried to disconnect who did not exist in the connections list")
            elif (client.getpeername() in connections):
                print(f"\nUser ID: {connections.index(client.getpeername())}\nsays: {message}")
        except OSError:
            connections.remove(client.getpeername())
            clients_list.remove(client)
            client.close()
            thread_stop2 = True
        except Exception as e:
            print(f"Error: {e}")
    thread_stop2 = False

def send_message(message: str, client: socket):
    # encode and send the message
    client.send(message.encode())

def main():
    # create the thread for handeling new connections
    thread1 = threading.Thread(target=recieve_connections)
    thread1.start()
    global thread_stop1
    global thread_stop2
    global socket
    
    # create the clear string lambda function and print the help screen for users to get started
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
                    if ((target_ip, target_port) in connections):
                        print("you are already connected to that user")
                    else:
                        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connection_socket.connect((target_ip, target_port))                         #failed due to str cannot be interpreted as integer
                        connection_socket.send("connected".encode())
                        connections.append((target_ip, target_port))
                        clients_list.append(connection_socket)
                        #start listening for messages from the newly connected client
                        thread2 = threading.Thread(target=receive_messages, args=(connection_socket,))
                        thread2.start()
                        print(f"Successfully Connected to : {target_ip}:{target_port}")
                except ValueError:
                    print("please ensure you are using the correct format for ip and port")
                except socket.gaierror:
                    print(f"invalid address or hostname: {target_ip} {target_port}")
                except socket.timeout:
                    print("connection timed out")
                except ConnectionRefusedError:
                    print("the user you targeted refused your connection")
                except Exception as e:
                    print(f"Unknown Failure")
            else:
                print("\nplease see the help menu for information on how to use the connect command")
        elif (user_choice[0] == "LIST"):
            print("Connection list: ")
            for i, (conn_ip, conn_port) in enumerate(connections, start=0):
                print(f"ID: {i} IP: {conn_ip} Port: {conn_port}")
            if (len(user_choice) == 2 and user_choice[1] == "sockets"):
                print("Sockets list: ")
                for i, client in enumerate(clients_list, start=0):
                    print(f"ID: {i} Socket: {client}")
        elif (user_choice[0] == "TERMINATE"):
            try:
                conn_id = int(user_choice[1])
                if (0 <= conn_id <= len(connections) and 0 <= conn_id <= len(clients_list)):
                    print(f"\nTerminating connection with: {conn_id}") 
                    clients_list[conn_id].send("EXIT".encode())
                    #this causes all threads to stop?
                    thread_stop2 = True
                    clients_list[conn_id].close()
                    clients_list.pop(conn_id)
                    connections.pop(conn_id)
            except Exception as e:
                print("Did you enter an ip or wrong number? Try entering a valid connection\nCheck out LIST for valid entries")
        elif (user_choice[0] == "SEND"):
            try:
                if (int(user_choice[1]) in range(0, len(connections))):
                    conn_id = int(user_choice[1])
                    #conn_ip, conn_port = connections[conn_id]
                    message = " ".join(user_choice[2:])
                    print(f"Sending to {conn_id}...")
                    send_message(message, clients_list[int(user_choice[1])])
                else:
                    print("please select a value in range of the id's listed")
            except Exception as e:
                print(f"Uh-oh, looks like something went wrong!\nCheck the id you entered and try again!\n{e}")
        elif (user_choice[0] == "EXIT"):
            thread_stop1 = True
            thread_stop2 = True
            try:
                for client in clients_list:
                    client.send("EXIT".encode())
                    clients_list.remove(client)
                for connection in connections:
                    connections.remove(connection)
                print(f"Connections closed.")
            except:
                print("nothing connected")
            print("Sorry to see you go!")
            client_socket.close()
            quit()
        else:
            print("\nERROR: invalid entry\n")

if __name__ == "__main__":
    main()
