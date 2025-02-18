import select
from threading import Thread
#from pubsub import pub
#import rarest_piece
import logging
import message
import peer
import errno
#import socket
import random
import tqdm
import pickle
from hash_encrypt import Encryption


MAX_PEERS_TRY_CONNECT = 30
MAX_PEERS_CONNECTED = 8

class SockAddr:
    def __init__(self, ip, port, allowed=True):
        self.ip = ip
        self.port = port
        self.allowed = allowed

    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)


class PeersManager(Thread):
    def __init__(self, files, socket, torrent):
        Thread.__init__(self)
        self.peers = []
        self.socket = socket
        self.files = files
        self.connected_peers = {}
        self.dict_sock_addr = {}
        self.torrent = torrent
        self.encryption = Encryption()
        #self.connection_list = []

        #self.pieces_manager = pieces_manager
        #self.rarest_pieces = rarest_piece.RarestPieces(pieces_manager)
        #self.pieces_by_peer = [[0, []] for _ in range(pieces_manager.number_of_pieces)]
        #self.is_active = True

        # Events
        #pub.subscribe(self.peer_requests_piece, 'PeersManager.PeerRequestsPiece')
        #pub.subscribe(self.peers_bitfield, 'PeersManager.updatePeersBitfield')

    """ def peer_requests_piece(self, request=None, peer=None):
        if not request or not peer:
            logging.error("empty request/peer message")

        piece_index, block_offset, block_length = request.piece_index, request.block_offset, request.block_length

        block = self.pieces_manager.get_block(piece_index, block_offset, block_length)
        if block:
            piece = message.Piece(piece_index, block_offset, block_length, block).to_bytes()
            peer.send_to_peer(piece)
            logging.info("Sent piece index {} to peer : {}".format(request.piece_index, peer.ip)) """

    
    # def get_peer():

    # def remove_peer():
    def begin(self, peer):
        print('beginning')
        print(self.files)
        self.socket.listen()
        key = peer.socket.recv(4096)
        pubKey = pickle.loads(key)
        (sharedECCKey, ciphertextPubKey, ciphertextPrivKey) = self.encryption.ecc_calc_encryption_keys(pubKey)
        peer.socket.send('Received Pubkey'.encode())
        while True:
            print('waiting to send')
            self.socket.listen()
            request = peer.socket.recv(4096).decode()
            logging.debug('received request for file: {}'.format(request))
            peer.send_to_peer(request, sharedECCKey, ciphertextPubKey)


    def run(self):
        while True:
            self.socket.listen()
            client_socket, address = self.accept_connect()
            s = SockAddr(address[0], address[1])
            new_peer = peer.Peer(self.torrent.files, address, client_socket)
            self.dict_sock_addr[s.__hash__()] = s
            print('Connected to %d/%d peers' % (len(self.connected_peers), MAX_PEERS_CONNECTED))
            self.connected_peers[new_peer.__hash__()] = new_peer
            self.peers.append(new_peer)
            print('Connected to %d/%d peers' % (len(self.connected_peers), MAX_PEERS_CONNECTED))
            Thread(target=PeersManager.begin, args=(self, new_peer)).start()

    


    def accept_connect(self):
        try:
            client_socket, address = self.socket.accept()
            return client_socket, address

        except Exception as e:
            print("Failed to connect to peer (ip: %s - port: %s - %s)" % (self.ip, self.port, e.__str__()))
            return False


    # while not peer:
    #     close socket
    #     remove peer from peers
        
    # def wait_message(self):
    #     SEPARATOR = "<SEPARATOR>"
    #     received = self.socket.recv(4096).decode()
    #     filename, filesize = received.split(SEPARATOR)
    #     return filename, filesize

    #def run(self):
        #threading

    # def add_peers(self, peers):
    #     for peer in peers:
    #         #if self._do_handshake(peer):
    #         self.peers.append(peer)

    # def remove_peer(self, peer):
    #     if peer in self.peers:
    #         try:
    #             peer.socket.close()
    #         except Exception:
    #             logging.exception("")

    #         self.peers.remove(peer)














        # while self.is_active:
        #     read = [peer.socket for peer in self.peers]
        #     read_list, _, _ = select.select(read, [], [], 1)

        #     for socket in read_list:
        #         peer = self.get_peer_by_socket(socket)
        #         if not peer.healthy:
        #             self.remove_peer(peer)
        #             continue

        #         try:
        #             payload = self._read_from_socket(socket)
        #         except Exception as e:
        #             logging.error("Recv failed %s" % e.__str__())
        #             self.remove_peer(peer)
        #             continue

        #         peer.read_buffer += payload

        #         for message in peer.get_messages():
        #             self._process_new_message(message, peer)

    

    # def get_peer_by_socket(self, socket):
    #     for peer in self.peers:
    #         if socket == peer.socket:
    #             return peer

    #     raise Exception("Peer not present in peer_list")

    # def _process_new_message(self, new_message: message.Message, peer: peer.Peer):
    #     if isinstance(new_message, message.Handshake) or isinstance(new_message, message.KeepAlive):
    #         logging.error("Handshake or KeepALive should have already been handled")

    #     elif isinstance(new_message, message.Choke):
    #         peer.handle_choke()

    #     elif isinstance(new_message, message.UnChoke):
    #         peer.handle_unchoke()

    #     elif isinstance(new_message, message.Interested):
    #         peer.handle_interested()

    #     elif isinstance(new_message, message.NotInterested):
    #         peer.handle_not_interested()

    #     elif isinstance(new_message, message.Have):
    #         peer.handle_have(new_message)

    #     elif isinstance(new_message, message.BitField):
    #         peer.handle_bitfield(new_message)

    #     elif isinstance(new_message, message.Request):
    #         peer.handle_request(new_message)

    #     elif isinstance(new_message, message.Piece):
    #         peer.handle_piece(new_message)

    #     elif isinstance(new_message, message.Cancel):
    #         peer.handle_cancel()

    #     elif isinstance(new_message, message.Port):
    #         peer.handle_port_request()

    #     else:
    #         logging.error("Unknown message")