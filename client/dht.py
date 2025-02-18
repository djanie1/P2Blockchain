import peer
#from message import UdpTrackerConnection, UdpTrackerAnnounce, UdpTrackerAnnounceOutput
#from peers_manager import PeersManager

import requests
import logging
from bcoding import bdecode
import socket
from urllib.parse import urlparse
from kademlia.network import Server
import asyncio

MAX_PEERS_TRY_CONNECT = 30
MAX_PEERS_CONNECTED = 8

class SockAddr:
    def __init__(self, ip, port, allowed=True):
        self.ip = ip
        self.port = port
        self.allowed = allowed

    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)


class Dht(object):
    def __init__(self, torrent):#, socket):
        self.torrent = torrent
        self.threads_list = []
        self.connected_peers = {}
        self.peers_list = []
        self.dict_sock_addr = {}
        #self.socket = socket

    def get_peers_from_dht(self):
        #for i, tracker in enumerate(self.torrent.nodes):
                   
        y = asyncio.run(Dht.run(self))
        for p in y:
            if len(self.dict_sock_addr) >= MAX_PEERS_TRY_CONNECT:
                break

            s = SockAddr(p[0], p[1])
            self.dict_sock_addr[s.__hash__()] = s
            """ tracker_url = tracker[0]

            if str.startswith(tracker_url, "http"):
                try:
                    self.http_scraper(self.torrent, tracker_url)
                except Exception as e:
                    logging.error("HTTP scraping failed: %s " % e.__str__())

            elif str.startswith(tracker_url, "udp"):
                try:
                    self.udp_scrapper(tracker_url)
                except Exception as e:
                    logging.error("UDP scraping failed: %s " % e.__str__())

            else:
                logging.error("unknown scheme for: %s " % tracker_url) """
        
        #Needs to be removed
        self.try_peer_connect()

        return self.connected_peers, self.peers_list

    def try_peer_connect(self):
        logging.info("Trying to connect to %d peer(s)" % len(self.dict_sock_addr))

        for _, sock_addr in self.dict_sock_addr.items():
            if len(self.connected_peers) >= MAX_PEERS_CONNECTED:
                break

            #new_peer = peer.Peer(self.socket, sock_addr.ip, sock_addr.port)
            new_peer = peer.Peer(sock_addr.ip, sock_addr.port, self.torrent.files)
            #new_peer.connect()
            if not new_peer.connect():
                continue

            print('Connected to %d/%d peers' % (len(self.connected_peers), MAX_PEERS_CONNECTED))

            self.connected_peers[new_peer.__hash__()] = new_peer
            print('Connected to %d/%d peers' % (len(self.connected_peers), MAX_PEERS_CONNECTED))
            self.peers_list.append(new_peer)
            #Needs to be removed
            #return new_peer
            """ for x, y in self.torrent.file_names, self.torrent.file_sizes: 
                new_peer.send_to_peer(x,y)
                new_peer.read_from_socket(x,y)
 """

    def load_bootstrap_nodes(self):
        boot_strap = []
        for i in self.torrent.nodes:
            node = tuple(i)
            boot_strap.append(node)
        return boot_strap

    async def run(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        
        server = Server()
        await server.listen(8469)
        #boot_server = '0.0.0.0'
        #boot_port = 5432
        key = 'pi1_key'
        value = 'pi1_value'
        bootstrap_nodes = Dht.load_bootstrap_nodes(self)
        #bootstrap_node = (sys.argv[1], int(sys.argv[2]))
        nodes = []
        for boot_server in bootstrap_nodes:
            boot_node = tuple(boot_server)
            nodes.append(boot_node)
        
        await server.bootstrap(nodes)
        #await server.set(sys.argv[3], sys.argv[4])
        await server.set(key, value)
        server.stop()
        #await asyncio.Event().wait()
        return server.bootstrappable_neighbors()




    """ def send_message(self, conn, sock, tracker_message):
        message = tracker_message.to_bytes()
        trans_id = tracker_message.trans_id
        action = tracker_message.action
        size = len(message)

        sock.sendto(message, conn)

        try:
            response = PeersManager._read_from_socket(sock)
        except socket.timeout as e:
            logging.debug("Timeout : %s" % e)
            return
        except Exception as e:
            logging.exception("Unexpected error when sending message : %s" % e.__str__())
            return

        if len(response) < size:
            logging.debug("Did not get full message.")

        if action != response[0:4] or trans_id != response[4:8]:
            logging.debug("Transaction or Action ID did not match")

        return response """
