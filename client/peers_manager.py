import select
from threading import Thread
#from pubsub import pub
#import rarest_piece
import logging
#import message
#import peer
import errno
import socket
import random
import tqdm
import time
from decrypt_verify import Decryption
import pickle

class PeersManager(Thread):
    def __init__(self, files): #, socket):
        Thread.__init__(self)
        self.peers = []
        #self.socket = socket
        self.files = files
        self.completed_files = []
        self.requested_files = []
        self.ready_files = []
        self.decryption = Decryption()
        #self.pieces_manager = pieces_manager
        #self.rarest_pieces = rarest_piece.RarestPieces(pieces_manager)
        #self.pieces_by_peer = [[0, []] for _ in range(pieces_manager.number_of_pieces)]
        #self.is_active = True

    def populate_files(self):
        for x in self.files:
            self.ready_files.append(x['path'][0])


    #def get_peer():

    def add_peers(self, peers):
        for peer in peers:
            self.peers.append(peer)

    def begin(self, peer):
        #time.sleep(13.85)
        print('beginning')
        print(self.ready_files)
        privKey, pubKey = self.decryption.keygen()
        peer.socket.send(pickle.dumps(pubKey))
        #while len(self.ready_files) > 0:
        print(peer.socket.recv(4096).decode())
        while True:
            if len(self.ready_files) > 0:
                request = PeersManager.create_request(self)
                peer.send_request(request)
                peer.receive_from_peer(request, privKey)
                print('received file: {}'.format(request))
                self.completed_files.append(request)
                self.requested_files.remove(request)
                print(self.ready_files)
                # self.ready_files.remove(request)
                # print(self.ready_files)
            elif not len(self.ready_files):
                print('done with everything, thanks')
                Decryption.verify()
                quit()





    #def remove_peer():


    def run(self):
        self.populate_files()
        print(self.ready_files)
        #while self.ready_files:
        for peer in self.peers:
            print('ready to go')
            Thread(target=PeersManager.begin, args=(self, peer)).start()
        

    def create_request(self):
        file = random.choice(self.ready_files)
        while True:
            if file not in self.requested_files and file not in self.completed_files:
                logging.debug('created request for file: {}'.format(file))
                self.requested_files.append(file)
                self.ready_files.remove(file)
                print(self.ready_files)
                return file
            elif len(self.ready_files) == 1:
                logging.debug('created request for file: {}'.format(file))
                self.requested_files.append(file)
                self.ready_files.remove(file)
                print(self.ready_files)
                return file
                #request = file
                #break
            #logging.debug('created request for file: {}'.format(file))
            file = random.choice(self.ready_files)
        



    
    # def send_request(self, request, socket):
    #     try:
    #         #SEPARATOR = "<SEPARATOR>"
    #         socket.send(request.encode())
    #         logging.debug('sent request for file: {}'.format(request))
    #         #self.last_call = time.time()
    #     except Exception as e:
    #         #self.healthy = False
    #         logging.error("Failed to send to peer : %s" % e.__str__())

    # def prep_for_file(self, request):
    #     for x in self.files:
    #         if request in x['path']:
    #             file_name = request
    #             size = x['length']
    #             return file_name, size

    # def receive_from_peer(self, request):
        
    #     BUFFER_SIZE = 4096
    #     #received = self.socket.recv(BUFFER_SIZE).decode()
    #     #filename = filename
    #     #filesize = filesize
    #     # convert to integer
    #     #filesize = int(filesize)
    #     filename, filesize = self.prep_for_file(request)
    #     length = 0
    #     # start receiving the file from the socket
    #     # and writing to the file stream
    #     progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #     with open(filename, "wb") as f:
    #         while int(filesize) > length:
    #             # read 1024 bytes from the socket (receive)
    #             bytes_read = self.socket.recv(BUFFER_SIZE)
    #             #print(int(filesize))
    #             #print(progress.total)
    #             length += len(bytes_read)
    #             #if not bytes_read or bytes_read == b'Complete':    
    #                 # nothing is received
    #                 # file transmitting is done
    #              #   print('done')
    #              #   break
    #             #elif :
                    
    #             # write to the file the bytes we just received
    #             f.write(bytes_read)
    #             # update the progress bar
    #             progress.update(len(bytes_read))
        


#     def read_from_socket(self, filename, filesize):
        
#         BUFFER_SIZE = 4096
#         #received = self.socket.recv(BUFFER_SIZE).decode()
#         #filename = filename
#         #filesize = filesize
#         # convert to integer
#         #filesize = int(filesize)

#         # start receiving the file from the socket
#         # and writing to the file stream
#         progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
#         with open(filename, "wb") as f:
#             while True:
#                 # read 1024 bytes from the socket (receive)
#                 bytes_read = s.recv(BUFFER_SIZE)
#                 if not bytes_read:    
#                     # nothing is received
#                     # file transmitting is done
#                     break
#                 # write to the file the bytes we just received
#                 f.write(bytes_read)
#                 # update the progress bar
#                 progress.update(len(bytes_read))
        
    
#     def run(self):
        

#         #threading
        
        






#         while self.is_active:
#             read = [peer.socket for peer in self.peers]
#             read_list, _, _ = select.select(read, [], [], 1)

#             for socket in read_list:
#                 peer = self.get_peer_by_socket(socket)
#                 if not peer.healthy:
#                     self.remove_peer(peer)
#                     continue

#                 try:
#                     payload = self._read_from_socket(socket)
#                 except Exception as e:
#                     logging.error("Recv failed %s" % e.__str__())
#                     self.remove_peer(peer)
#                     continue

#                 peer.read_buffer += payload

#                 for message in peer.get_messages():
#                     self._process_new_message(message, peer)

#     def add_peers(self, peers):
#         for peer in peers:
#             #if self._do_handshake(peer):
#             self.peers.append(peer)

#     def remove_peer(self, peer):
#         if peer in self.peers:
#             try:
#                 peer.socket.close()
#             except Exception:
#                 logging.exception("")

#             self.peers.remove(peer)

#     def get_peer_by_socket(self, socket):
#         for peer in self.peers:
#             if socket == peer.socket:
#                 return peer

#         raise Exception("Peer not present in peer_list")

# threading.activeCount() - 1
    """ def _process_new_message(self, new_message: message.Message, peer: peer.Peer):
        if isinstance(new_message, message.Handshake) or isinstance(new_message, message.KeepAlive):
            logging.error("Handshake or KeepALive should have already been handled")

        elif isinstance(new_message, message.Choke):
            peer.handle_choke()

        elif isinstance(new_message, message.UnChoke):
            peer.handle_unchoke()

        elif isinstance(new_message, message.Interested):
            peer.handle_interested()

        elif isinstance(new_message, message.NotInterested):
            peer.handle_not_interested()

        elif isinstance(new_message, message.Have):
            peer.handle_have(new_message)

        elif isinstance(new_message, message.BitField):
            peer.handle_bitfield(new_message)

        elif isinstance(new_message, message.Request):
            peer.handle_request(new_message)

        elif isinstance(new_message, message.Piece):
            peer.handle_piece(new_message)

        elif isinstance(new_message, message.Cancel):
            peer.handle_cancel()

        elif isinstance(new_message, message.Port):
            peer.handle_port_request()

        else:
            logging.error("Unknown message") """
