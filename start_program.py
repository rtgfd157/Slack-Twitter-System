import logging
import pickle # working with dictionaries
import time
import asyncio
import random
import threading 
from  sockets.server_socket import socket_controller as sc
from  sockets.server_socket import operate_command 
from datetime import datetime


async def main( ):
    """
    2 methods
    1 - will be our server socket
    2 - will call method with data that will be parse to now time send to content channel in slack
    """
    await asyncio.gather(
        sc(),
        update_time_every_sleep_awake()
    )
    
async def update_time_every_sleep_awake():
    while True:
        await asyncio.sleep(3600)
        data =  {'command': 'now'}
        await operate_command(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(' This is an info message')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    