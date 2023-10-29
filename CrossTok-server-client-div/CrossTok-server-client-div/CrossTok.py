from asyncio.windows_events import NULL
import socket
import sys
import threading

#TODO: implement a server socket and a client socket
#TODO: server socket will bind, listen, accept, loop thru recv, send; close
#TODO: client socket will connect, loop thru send, recv; close
#
#
#

host = socket.gethostbyname(socket.gethostname())
port = 5959
max_conn = 10
connections = []    #stored as (IP, Port) pairs

if sys.argv.__sizeof__() == 1:
    port = int(sys.argv[1])
else:
    pass

#server function
#needs to listen on port for new connections, add to connection list when new connection spawned
def server_func(server, host, port):
    while True:
        try:
            connections.append((host, port))
            ip_address, port = server.accept()
        except Exception as e:
            print(f"Error accepting a connection: {e}")
        

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
    
def incoming_message_handler(target_socket, sender_addr, sender_port):
    while True:
        try:
            message = target_socket.recv(2048).decode('utf-8')
            if message == NULL:
                print(f"User {sender_addr} on port {sender_port} disconnected")
                break
            print(f"Message from {sender_addr}")
            print(f"Sender's Port: {sender_port}")
            print(f"Message: \"{message}\"")
        except Exception as e:
            print(f"Exception {e} caught")
            break
    target_socket.close()
    connections.remove((sender_addr, sender_port))
    
def client_func():
    return 0

# TODO: make connect and list work
# TODO: list should find all unique connected clients, store conn list in list
# TODO: new connections establishing TCP link should be checked against list, then added if unique
# TODO: connect should ping the target ip with TCP connection request which triggers addition to the connected clients list

def main():
    try:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen(max_conn)
            
        except Exception as e:
            print(f"Error initializing the server socket: {e}")
            
        threading.Thread(target=server_func, args=(server,host, port)).start()
        while True: 
        
            print_help()
            print("CMD: ", end='')  
            user_choice = input()
            user_choice = user_choice.split()
            user_choice[0] = user_choice[0].upper()
        
        
            if (user_choice[0] == "MYIP"):
                print("Your IP Address: " + socket.gethostbyname(socket.gethostname()) + "\n")
            elif (user_choice[0] == "MYPORT"):
                print("Your port: " + str(port) + "\n")
            elif (user_choice[0] == "HELP"):
                print_help()
            elif (user_choice[0] == "CONNECT"):
                target_ip = user_choice[1]
                try:
                     target_port = int(user_choice[2])
                except ValueError:
                     print("Invalid port number. Please enter a valid integer.")
                try:
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.connect((target_ip, target_port))                         #failed due to str cannot be interpreted as integer
                    connections.append((target_ip, target_port))
                    print(f"Successfully Connected to : {target_ip}:{target_port}")
                    threading.Thread(target=incoming_message_handler, args=(target_socket, target_ip, target_port)).start()
                except Exception as e:
                    print(f"Failed due to: {e}")
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
                    conn_id = int(user_choice[1])
                    conn_ip, conn_port = connections[conn_id]
                    message = user_choice[2:]
                    print(f"Sending to {conn_id}...")
                    conn_ip.send(message)
                except Exception as e:
                    print("Uh-oh, looks like something went wrong!\nCheck the id you entered and try again!")
            elif (user_choice[0] == "EXIT"):
                for conn_ip, conn_port in connections:
                    try:
                        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        target.connect((conn_ip, conn_port))
                        target.send('exit'.encode('utf-8'))
                        target.close()
                        print(f"Connection to {conn_ip}:{conn_port} closed.")
                    except:
                        pass
                print("Sorry to see you go!")
                quit()
                break
            else:
                print("\n\nERROR: invalid entry\n\n")
    except Exception as e:
        print(f"An error occurred in server initialization: {e}")
if __name__ == "__main__":
    main()


