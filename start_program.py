import logging
import pickle # working with dictionaries
import time
import asyncio
import random
import threading 
from  sockets.server_socket import socket_controller as sc
import slack_communicator
from datetime import datetime


async def main( ):
    """
    2 methods
    1 - will be our server socket
    2 - will update time every 1 hour
    """
    await asyncio.gather(
        sc(),
        update_time_every_sleep_awake()
    )
    
async def update_time_every_sleep_awake():
    while True:
        await asyncio.sleep(3600)
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        slack_communicator.post_message_to_slack(current_time)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(' This is an info message')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    