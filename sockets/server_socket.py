import socket
import select
import random
import pickle
import asyncio
import logging
import os
import slack_communicator
import twitter_communicator
from datetime import datetime
logging.basicConfig(level=logging.INFO)



# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5679
SERVER_IP = "127.0.0.1"

def recieve_message(conn):

    data = conn.recv(4096)
    print("date  ",data)
    data_variable = pickle.loads(data)
    logging.info(" server message get: ",data_variable)
    return data_variable

def send_message(conn, message):
    data_string = pickle.dumps(message)
    logging.info(" server message send: ",data_string)
    conn.send(data_string)


# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""

	print("Setting up server...")
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()
	print("Listening for clients...")
	return server_socket


async def socket_controller():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    
    server_socket = setup_socket()
    client_sockets = []
    loop = asyncio.get_event_loop()
    out =False
    while True and out == False:
        await asyncio.sleep(1)
        #await loop.run_in_executor()
        ready_to_read, ready_to_write, in_error =  select.select(
            [server_socket] + client_sockets, [], [], 0.1)
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
            else:
                print("New data from client ",str(current_socket))
                data = recieve_message(current_socket)
                
                print(data)
                client_sockets.remove(current_socket)
                current_socket.close()
                if data['command'] == 's':
                    #server_socket.remove(current_socket)
                    server_socket.close()
                    out = True
                    os._exit(1)
                elif data['command'] == 'now':
                    now = datetime.now()
                    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    slack_communicator.post_message_to_slack(current_time)
                elif data['command'] == 'new-content' and data['username'] == 'null':
                    print("-----")
                    twitter_communicator.check_users_new_tweets()
                elif data['command'] == 'tweet':
                    message = data['message']
                    twitter_communicator.make_tweet(message)
                elif data['command'] == 'new-content':
                    username = data['username']
                    twitter_communicator.get_last_hour_user_tweet(username)
                
                