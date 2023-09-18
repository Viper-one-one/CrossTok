import argparse
from asyncio.windows_events import NULL
import socket
import sys
from time import sleep

host = socket.gethostbyname(socket.gethostname())
if sys.argv.__sizeof__() == 1:
    port = sys.argv[1]
else:
    port = 5959

def print_menu():
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
    print("CMD: ", end='')      

def main():

    while True:
       
        print_menu()
        user_choice = input()
        user_choice = user_choice.upper()
        
        match user_choice:
            case "MYIP":
                print(socket.gethostbyname(socket.gethostname()) + "\n")
            case "MYPORT":
                print(str(port) + "\n")
            case "SEND":
                print("sent")
            case "TERMINATE":
                print("Sorry to see you go!")
                sleep(1)
                quit()
            case _:
                print("\n\nERROR: invalid entry\n\n")

if __name__ == "__main__":
    main()


