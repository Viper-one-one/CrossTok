from asyncio.windows_events import NULL
import socket
import sys
import threading

#TODO: implement a server socket and a client socket
#TODO: server socket will bind, listen, accept, loop thru recv, send; close
#TODO: client socket will connect, loop thru send, recv; close

host = socket.gethostbyname(socket.gethostname())
listen_port = 5959
max_conn = 10
connections = []    #stored as (IP, Port) pairs

if sys.argv.__sizeof__() == 1:
    listen_port = sys.argv[1]
      

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
    
def connection_handler(listen_socket):
    while True:
        conn, addr = listen_socket.accept()
        connections.append((conn, addr))
        conn.send("connection recieved".encode(encoding='utf-8'))
    
def incoming_message_handler(target_socket, sender_addr, sender_port):
    while True:
        try:
            message = target_socket.recv(2048).decode('utf-8')
            if message == "exit":
                print(f"User {sender_addr} on port {sender_port} disconnected")
                break
            print(f"\nMessage from {sender_addr}")
            print(f"Sender's Port: {sender_port}")
            print(f"Message: \"{message}\"")
        except Exception as e:
            print(f"Exception {e} caught")
            break
    target_socket.close()
    connections.remove((sender_addr, sender_port))

# TODO: make terminate and send work
# TODO: terminate error: connection number does not exist
# TODO: send error: "something went wrong, check id, try again"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, listen_port))
    server.listen(max_conn)
    threading.Thread(target=connection_handler, args=(server, )).start()    
    print_help()
    
    while True: 
        print("CMD: ", end='')  
        user_choice = input()
        user_choice = user_choice.split()
        user_choice[0] = user_choice[0].upper()
        
        
        if (user_choice[0] == "MYIP"):
            print("Your IP Address: " + socket.gethostbyname(socket.gethostname()) + "\n")
        elif (user_choice[0] == "MYPORT"):
            print("Your port: " + str(listen_port) + "\n")
        elif (user_choice[0] == "HELP"):
            print_help()
        elif (user_choice[0] == "CONNECT"):
            if len(user_choice) == 3:
                target_ip = user_choice[1]
                target_port = int(user_choice[2])
                try:
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.connect((target_ip, target_port))
                    connections.append((target_ip, target_port))
                    print(f"Successfully Connected to : {target_ip}:{target_port}")
                    threading.Thread(target=incoming_message_handler, args=(target_socket, target_ip, target_port)).start()
                except Exception as e:
                    print(f"Failed due to: {e}")
            else:
                print("Error: please use connect <dest_ip> <port#>")
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
            if len(user_choice) >= 3:
                try:
                    conn_id = int(user_choice[1])
                    conn_ip, conn_port = connections[conn_id]
                    message = user_choice[2:]
                    print(f"Sending to {conn_id}...")       #fails after here
                    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target.connect((conn_ip, conn_port))            #this is being read as a socket type, must be str, byte, or bytearray
                    target.send(message)
                except Exception as e:          #hits this 
                    print("Uh-oh, looks like something went wrong!\nCheck the id you entered and try again!")
            else:
                print("Error: please use send <conn_id> <message...>")
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

if __name__ == "__main__":
    main()


