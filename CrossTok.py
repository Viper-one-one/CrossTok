from collections import UserString
import socket
import argparse
 
def print_menu():
    print("******************* Welcome to CrossTok *****************\n")
    print("In this application you can do the following:\n")
    print("MYIP: returns your IPv4 address\n")
    print("HELP: returns commands you can type to use the program\n")
    print("MYPORT: returns the port CrossTok is using to listen on\n")
    print("CONNECT <dest IP> <port #>: establishes TCP connection to the <dest IP> on <port #>\n")
    print("LIST: Display a numbered list of all connections CrossTok is using with an id number\n")
    print("TERMINATE: <connection id>: close connection denoted with <connection id>\n")
    print("SEND: <connection id> <message>: send a message to <connection id> with string <message>\n")
    print("EXIT: terminate CrossTok and all active connections\n")
    

def main():
    while True:
        print_menu()
        user_choice = input()
        match user_choice:
            case "MYIP":
                print(socket.gethostbyname(socket.gethostname()) + "\n")
            case _:
                print("\nERROR: invalid entry\n")

if __name__ == "__main__":
    main()
    