import time
import peers_manager
#import pieces_manager
import torrent
#import dht
import logging
import os
#import message
import socket
import sys
import server

import asyncio
import threading
from kademlia.network import Server
from bcoding import bdecode
#from hash_encrypt import Encryption



class Run(object):
    percentage_completed = -1
    last_log_line = ""

    def __init__(self):
        try:
            torrent_file = sys.argv[1]
        except IndexError:
            logging.error("No torrent file provided!")
            sys.exit(0)
        
        self.socket = socket.socket()
        self.socket.bind(('192.168.1.3', 5432))
        #self.torrent_file_name = torrent_file.split('.')[1]

        self.torrent = torrent.Torrent().load_from_path(torrent_file)
        #self.dht = dht.Dht(self.torrent, self.socket)
        

        #self.pieces_manager = pieces_manager.PiecesManager(self.torrent)
        self.peers_manager = peers_manager.PeersManager(self.torrent.files, self.socket, self.torrent)

        #self.peers_manager.start()
        #logging.info("PeersManager Started")
        #logging.info("PiecesManager Started")

#CHeck if file exists and prevent overwriting


    #def start(self, node_list):
    def start(self):
        print('Ready to send')
        self.peers_manager.start()

        # peers_dict, new_peer = self.dht.get_peers_from_dht()
        # while True:
        #     #self.socket.listen()
        #     print('waiting to send')
        #     request = new_peer.socket.recv(4096).decode()
        #     logging.debug('received request for file: {}'.format(request))
        #     new_peer.send_to_peer(request)

        """ peers_dict = []
        for node in node_list:
            new_node = list(node)
            peers_dict.append(new_node) """
        #peers_dict = node_list    
        #print(peers_dict)
        #self.peers_manager.add_peers(peers_dict.values())
        
        """ while not self.pieces_manager.all_pieces_completed():
            if not self.peers_manager.has_unchoked_peers():
                time.sleep(1)
                logging.info("No unchocked peers")
                continue

            for piece in self.pieces_manager.pieces:
                index = piece.piece_index

                if self.pieces_manager.pieces[index].is_full:
                    continue

                peer = self.peers_manager.get_random_peer_having_piece(index)
                if not peer:
                    continue

                self.pieces_manager.pieces[index].update_block_status()

                data = self.pieces_manager.pieces[index].get_empty_block()
                if not data:
                    continue

                piece_index, block_offset, block_length = data
                piece_data = message.Request(piece_index, block_offset, block_length).to_bytes()
                peer.send_to_peer(piece_data) """


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    async def starun():
        server = Server()
        await server.listen(5432)
        await asyncio.Event().wait()

    run = Run()
    z = threading.Thread(target=server.send)
    y = threading.Thread(target=run.start)
    #z.start()
    y.start()
    asyncio.run(starun())











    # def load_bootstrap_nodes(self):
    #     boot_strap=[]
    #     for i in self.torrent.nodes:
    #         node = tuple(i)
    #         boot_strap.append(node)
    #     return boot_strap
