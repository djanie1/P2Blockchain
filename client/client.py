import socket
import tqdm
import os

import logging
import asyncio
import sys
import time

#from kademlia.network import Server


# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log = logging.getLogger('kademlia')
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)

# async def run():
#     server = Server()
#     await server.listen(8471)
#     bootstrap_node = ('0.0.0.0', 5432)
#     #await server.bootstrap([bootstrap_node,('0.0.0.0', 8467)])
#     await server.bootstrap([bootstrap_node])
#     await server.set('key', 'valuejet')
#     return server.bootstrappable_neighbors()
#     #server.stop()

def receive():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    # the ip address or hostname of the server, the receiver
    host = '192.168.1.3' #192.168.1.7, 192.168.1.8, 192.168.1.9
    # the port, let's use 5001
    port = 5438
   
    # create the client socket
    s = socket.socket()

    #print(f"[+] Connecting to {host}:{port}")
    #s.bind(('127.0.0.1', 8471))
    s.connect((host, port))
    print("[+] Connected.")

    torrRec_start = time.perf_counter()
    # receive the file infos
    # receive using client socket, not server socket
    received = s.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", file=open('Torrent_progress.txt', 'a'), unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:  #filename
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()
    torrRec_stop = time.perf_counter()
    with open('TorrentRec_transfer.txt', 'a') as outfile:
        outfile.write(filename+': '+str(torrRec_stop-torrRec_start)+'\n')

#x = asyncio.run(run())
receive()