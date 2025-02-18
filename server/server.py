import socket
import tqdm
import os
import sys
import errno

import logging
import asyncio
import threading
import time

#from kademlia.network import Server

# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log = logging.getLogger('kademlia')
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)

#dht service
# async def starun():
#         server = Server()
#         await server.listen(5432)
#         await server.set('my_key', 'valupack')
#         await asyncio.Event().wait()


def send():
    # device's IP address
    SERVER_HOST = '192.168.1.3' #192.168.1.7, 192.168.1.8, 192.168.1.9
    SERVER_PORT = 5438
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    # accept connection if there is any
    # the name of file we want to send, make sure it exists
    filename = "blocks_folder.torrent"
    # get the file size
    filesize = os.path.getsize(filename)

    # create the server socket
    # TCP socket
    s = socket.socket()

    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))

    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, address = s.accept() 
        # if below code is executed, that means the sender is connected
        # print(f"[+] {address} is connected.")
        # print(address[0])
        # print(address[1])
        # print(client_socket)
        # print(s)
        torTran_start = time.perf_counter()

        try:
        # send the filename and filesize
            client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass
        #start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                client_socket.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        client_socket.close()
        TorTran_stop = time.perf_counter()
        with open('time/Torrent_transfer.txt', 'a') as outfile:
            outfile.write(filename+': '+str(TorTran_stop-torTran_start)+'\n')
        #s.listen()


#spool thread for data transfer
x = threading.Thread(target=send)
x.start()

#start dht service
#asyncio.run(starun())
