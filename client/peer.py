from statemachine import PeerState
import tqdm
import socket
import logging
#import message
import random
import pickle
from decrypt_verify import Decryption
import time

class Peer(object):
    def __init__(self, ip, port, files): #socket, 
        self.read_buffer = b''
        self.socket = None
        self.ip = ip
        self.port = port
        self.files = files
        #self.completed_files = []
        #self.requested_files = []
        #self.ready_files = []
        #self.file_sizes = file_sizes
        
        """ self.state = {
            
        } """
    # def populate_files(self):
    #     for x in self.files:
    #         self.ready_files.append(x['path'][0])



    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)
    
    def connect(self):
        try:
            #self.socket.connect((self.ip, self.port))
            self.socket = socket.create_connection((self.ip, self.port), timeout=2)
            #self.socket.setblocking(False)
            logging.debug("Connected to peer ip: {} - port: {}".format(self.ip, self.port))
            #self.healthy = True

        except Exception as e:
            print("Failed to connect to peer (ip: %s - port: %s - %s)" % (self.ip, self.port, e.__str__()))
            return False

        return True
    
    # def create_request(self):
    #     file = random.choice(self.ready_files)
    #     while True:
    #         if file not in self.requested_files and file not in self.completed_files:
    #             logging.debug('created request for file: {}'.format(file))
    #             self.requested_files.append(file)
    #             return file
    #             #request = file
    #             #break
    #         logging.debug('created request for file: {}'.format(file))
    #         file = random.choice(self.ready_files)
        



    
    def send_request(self, request):
        try:
            #SEPARATOR = "<SEPARATOR>"
            self.socket.send(request.encode())
            logging.debug('sent request for file: {}'.format(request))
            #self.last_call = time.time()
        except Exception as e:
            #self.healthy = False
            logging.error("Failed to send to peer : %s" % e.__str__())

    def prep_for_file(self, request):
        for x in self.files:
            if request in x['path']:
                file_name = request
                size = x['length']
                return file_name, size

    def receive_from_peer(self, request, privKey):
        
        BUFFER_SIZE = 4096
        #received = self.socket.recv(BUFFER_SIZE).decode()
        #filename = filename
        #filesize = filesize
        # convert to integer
        #filesize = int(filesize)
        location = "blocks_folder/"
        filename, filesize = self.prep_for_file(request)
        length = 0
        data = b""
        # start receiving the file from the socket
        # and writing to the file stream
        file_loc = location+filename
        transf_start = time.perf_counter()
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", file=open('time/down1_progress.txt', 'a'), unit="B", unit_scale=True, unit_divisor=1024)
        if filesize < 52428800:  #50MB
            new_size = self.socket.recv(BUFFER_SIZE).decode()
            self.socket.send('Received encrypted size'.encode())
            with open(file_loc, "wb") as f:
                while length < int(new_size):
                    # read 1024 bytes from the socket (receive)
                    read = self.socket.recv(BUFFER_SIZE)
                    if not read:    
                    # nothing is received
                    # file transmitting is done
                        break
                    
                    length += len(read)
                    progress.update(len(read))
                    data += read

                #transf_stop = time.perf_counter()
                #postproc_start = time.perf_counter()
                encryptedMsg = pickle.loads(data)
                bytes_read = Decryption.decrypt_ECC(encryptedMsg, privKey)
                print('decrypt complete')   
                # write to the file the bytes we just received
                f.write(bytes_read)
                #postproc_end = time.perf_counter()
                transf_stop = time.perf_counter()
                #with open('postproc.txt', 'a') as out:
                #    out.write(filename+': '+str(postproc_end-postproc_start)+'\n')
                with open('time/down1_transfer.txt', 'a') as outfile:
                    outfile.write(filename+': '+str(transf_stop-transf_start)+'\n')
            #self.socket.send('Receive encrypted small file complete'.encode())
        
        else:
            (nonce) = pickle.loads(self.socket.recv(BUFFER_SIZE))
            self.socket.send('Received Nonce'.encode())
            (ciphertextPubKey) = pickle.loads(self.socket.recv(BUFFER_SIZE))
            self.socket.send('Received ciphertextPubkey'.encode())
            (secretKey) = Decryption.large_keyGen(privKey, ciphertextPubKey)
            aesCipher = Decryption.large_AES(secretKey, nonce)
        
            with open(file_loc, "wb") as f:
                while length < filesize:
                    # read 1024 bytes from the socket (receive)
                    #bytes_read = s.recv(BUFFER_SIZE)
                    read = self.socket.recv(BUFFER_SIZE)
                    
                    if not read:
                    #if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break

                    data = pickle.loads(read)
                    bytes_read = Decryption.large_decrypt_ECC(data, aesCipher)
                    f.write(bytes_read)
                    length += len(data)
                    progress.update(len(data))
                    #data += read
                #encryptedMsg = pickle.loads(data)
                
                # pickle.dump(data, open('data.pem', 'wb'))
                # pickle.dump(encryptedMsg, open('encryptedmsg.pem', 'wb'))
                
                #bytes_read = decrypt_ECC(encryptedMsg, privKey)
                self.socket.send('Receive encrypted large file complete'.encode())
                print('sent complete message')
                #s.listen()
            #print('we are okay')
            (authTag) = self.socket.recv(BUFFER_SIZE)
            print('received authTag')
            #transf_stop = time.perf_counter()
            print(f'authTag: {authTag}')
            #postproc_start = time.perf_counter()
            Decryption.large_verify(aesCipher, authTag)
                #print(s.recv(BUFFER_SIZE).decode())
            print('decrypt complete')
            transf_stop = time.perf_counter()
            #with open('postproc.txt', 'a') as out:
            #    out.write(filename+': '+str(postproc_end-postproc_start)+'\n')
            with open('time/down1_transfer.txt', 'a') as outfile:
                outfile.write(filename+': '+str(transf_stop-transf_start)+'\n')


            
    
