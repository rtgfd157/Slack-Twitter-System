import socket
import pickle
import struct
import sys
import logging

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5679
#logging.basicConfig(level=logging.INFO)

logging.basicConfig(level=logging.DEBUG)
# HELPER SOCKET METHODS


def recieve_message(conn):

    data = conn.recv(1024).decode()
    data_variable = pickle.loads(data)
    logging.info(" client data recived ", data_variable)
    return data_variable


def send_message(conn, message):
    logging.info(" client message send ", message)
    data_string = pickle.dumps(message)
    print("data string: ", data_string)
    conn.send(data_string)


def connect():

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


if __name__ == '__main__':
    socket = connect()

    command = ''
    if len(sys.argv) >= 2:
        command = sys.argv[1]
    if command == 's':
        d = {'command': 's'}
    elif  command == 'now' :
        d = {'command': 'now'}
    elif  command == 'new-content' :
        if len(sys.argv) >= 3:
            d = {'command': 'new-content', 'username':str(sys.argv[2])}
        else:
            d = {'command': 'new-content', 'username':'null'}

    elif  command == 'tweet' :
        d = {'command': 'tweet', 'message': str(sys.argv[2])  }
    else:
        d = {'command': 'unknown command'}

    send_message(socket, d)
