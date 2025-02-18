


import hashlib
from bcoding import bencode, bdecode
import logging
import os

class Torrent(object):
    def __init__(self):
        self.torrent_file = {}
        #self.total_length: int = 0
        #self.piece_length: int = 0
        #self.pieces: int = 0
        self.info_hash: str = ''
        #self.peer_id: str = ''
        self.nodes = ''
        self.file_names = []
        self.file_sizes = []
        self.number_of_pieces: int = 0
        self.files = []

    def load_from_path(self, path):
        with open(path, 'rb') as file:
            contents = bdecode(file)

        self.torrent_file = contents
        #self.piece_length = self.torrent_file['info']['piece length']
        self.pieces = self.torrent_file['info']['pieces']
        raw_info_hash = bencode(self.torrent_file['info'])
        self.info_hash = hashlib.sha1(raw_info_hash).digest()
        #self.peer_id = self.generate_peer_id()
        self.nodes = self.get_bootstrap_nodes()
        self.file_names = self.get_file_names()
        self.file_sizes = self.get_file_sizes()
        self.files = self.torrent_file['info']['files']
        #self.init_files()
        #self.number_of_pieces = math.ceil(self.total_length / self.piece_length)
        logging.debug(self.nodes)
        logging.debug(self.file_names)
        return self


    def get_bootstrap_nodes(self):
        if 'nodes' in self.torrent_file:
            return self.torrent_file['nodes']
    
    def get_file_names(self):
        files = self.torrent_file['info']['files']
        file_names = []
        for x in files:
            file_names.append(x['path'][0])
        return file_names

    def get_file_sizes(self):
        files = self.torrent_file['info']['files']
        file_sizes = []
        for x in files:
            file_sizes.append(x['length'])
        return file_sizes
        
    """ def all_pieces_completed(self):
        for piece in self.pieces:
            if not piece.is_full:
                return False

        return True """