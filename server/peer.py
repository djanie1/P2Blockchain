from statemachine import PeerState

#import socket
import logging
import message
import tqdm
import pickle
import io
from hash_encrypt import Encryption
import time

#import errno

class Peer(object):
    def __init__(self, files, address, socket):
        self.socket = socket
        self.ip = address[0]
        self.port = address[1]
        self.files = files
        
        #self.file_sizes = file_sizes
        #self.files = files
        """ self.state = {
            
        } """

    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)
    
    

    #return True
    
    #def send_to_peer(self, msg):
        #try:
            #self.socket.send(msg)
            #self.last_call = time.time()
        #except Exception as e:
            #self.healthy = False
            #logging.error("Failed to send to peer : %s" % e.__str__())

    def handle_request_from_peer(self, request):
        for x in self.files:
            if request in x['path']:
                file_name = request
                size = x['length']
                return file_name, size
            
    
    def send_to_peer(self, request, sharedECCKey, ciphertextPubKey):
        #preproc_start = time.perf_counter()
        transf_start = time.perf_counter()
        filename, filesize = self.handle_request_from_peer(request)
        #filename, filesize = self.wait_message()
        location = "blocks_folder/"
        file_loc = location+filename
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", file= open('time/up1_progress.txt', 'a'), unit="B", unit_scale=True, unit_divisor=1024)
        
        if filesize < 52428800:  #50MB
            with open(file_loc, "rb") as f:
                data = f.read()
                encryptedMsg = io.BytesIO(pickle.dumps(Encryption.encrypt_ECC(data, sharedECCKey, ciphertextPubKey)))
                self.socket.send(str(encryptedMsg.getbuffer().nbytes).encode())
                print(self.socket.recv(4096).decode())
                #preproc_end = time.perf_counter()
                #transf_start = time.perf_counter()
                while True:
                    BUFFER_SIZE = 4096
                    # read the bytes from the file
                    bytes_read = encryptedMsg.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in 
                    # busy networks
                    #sock is client socket
                    #try:    
                    self.socket.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
            #self.socket.send('Complete'.encode())
            print('send complete')
            transf_stop = time.perf_counter()
            #with open('preproc.txt', 'a') as out:
            #    out.write(filename+': '+str(preproc_end-preproc_start)+'\n')
            with open('time/up1_transfer.txt', 'a') as outfile:
                outfile.write(filename+': '+str(transf_stop-transf_start)+'\n')
            #print(self.socket.recv(BUFFER_SIZE).decode())
                    #""" except IOError as e:
                    #    if e.errno == errno.EPIPE:
                    #        pass """
        else:
            (aesCipher, nonce) = Encryption.large_AES(sharedECCKey)
            self.socket.send(pickle.dumps(nonce))
            print(self.socket.recv(4096).decode())
            self.socket.send(pickle.dumps(ciphertextPubKey))
            print(self.socket.recv(4096).decode())
            #preproc_end = time.perf_counter()
            #transf_start = time.perf_counter()
            with open(file_loc, "rb") as f:
                while True:
                    BUFFER_SIZE = 4078
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    #print(len(pickle.dumps(Encryption.large_encrypt_ECC(aesCipher, data))))
                    self.socket.sendall(pickle.dumps(Encryption.large_encrypt_ECC(aesCipher, data)))
                    progress.update(len(data))
                    #print(self.socket.recv(4096).decode())
            print(self.socket.recv(BUFFER_SIZE).decode())
            (authTag) = Encryption.large_digest(aesCipher)
            #print(f'authTag: {authTag}')
            self.socket.send(authTag)
            transf_stop = time.perf_counter()
            #with open('preproc.txt', 'a') as out:
            #    out.write(filename+': '+str(preproc_end-preproc_start)+'\n')
            with open('time/up1_transfer.txt', 'a') as outfile:
                outfile.write(filename+': '+str(transf_stop-transf_start)+'\n')

