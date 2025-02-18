#from statemachine import PeerState

import time
import peers_manager
#import pieces_manager
import torrent
import dht
import logging
import os
#import message
import socket
import sys
import asyncio
import threading
from kademlia.network import Server
from bcoding import bdecode
import subprocess

class Run(object):
    #percentage_completed = -1
    #last_log_line = ""

    def __init__(self):
        try:
            torrent_file = sys.argv[1]
        except IndexError:
            logging.error("No torrent file provided!")
            sys.exit(0)
        
        #self.socket = socket.socket()
        #self.socket.bind(('127.0.0.1', 8469))
        self.torrent = torrent.Torrent().load_from_path(torrent_file)
        self.dht = dht.Dht(self.torrent)#, self.socket)

        #self.pieces_manager = pieces_manager.PiecesManager(self.torrent)
        self.peers_manager = peers_manager.PeersManager(self.torrent.files) #, self.socket)

        #
        #logging.info("PeersManager Started")
        #logging.info("PiecesManager Started")

    #def start(self, node_list):
    def start(self):
        peers_dict, peers_list = self.dht.get_peers_from_dht()
        self.peers_manager.add_peers(peers_list)
        print(self.peers_manager.peers)
        
        #async def starun():
        #    server = Server()
        #    await server.listen(8469)
        #    await asyncio.Event().wait()


        #v = threading.Thread(target = self.peers_manager.start)
        #v.start()
        #asyncio.create_task(starun())
        cmd = "python3 serve.py &"
        subprocess.run(cmd, shell=True)
        self.peers_manager.start() 


        """ peers_dict = []
        for node in node_list:
            new_node = list(node)
            peers_dict.append(new_node) """
        #peers_dict = node_list    
        #print(peers_dict)
        #self.peers_manager.add_peers(peers_dict.values())
        #new_peer.populate_files()
        #print(new_peer.ready_files)
        """ while new_peer.ready_files:
            
            request = new_peer.create_request()
            new_peer.send_request(request, self.socket)
            new_peer.receive_from_peer(request)
            print('received file: {}'.format(request)) """


        
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


""" device = PeerState()

with open("Statetest.txt") as file:
    for i in file.readlines():
        device.on_event(str.strip(i))  """



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    run = Run()
    run.start()
