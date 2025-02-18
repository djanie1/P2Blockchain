class State(object):
    def __init__(self):
        print('Current state:', str(self))

    def __repr__(self):
        return self.__str__()

    def __str__(self):    
        return self.__class__.__name__


class Idle(State):
    def run(self):
        print("Idling \n")

    def next(self, input):
        if input == "received Meta File Location":
            return Ready()
        return self


class Ready(State):
    def run(self):
        print("I am Ready for work \n")

    def next(self, input):
        if input == "requested Meta File":
            return WaitingResponse()
        
        if input == "Wait for connection requests": #Uploader
            return Unconnected()
        return self


class WaitingResponse(State):
    def run(self):
        print("Waiting for Response \n")

    def next(self, input):
        if input == "Received meta file":
            return Unconnected()
        elif input == "Connection Timeout":
            return Ready()
        elif input == "No response from handshake":
            return Unconnected()
        elif input == "Received Handshake":
            return Connected()
        return self


class Unconnected(State):
    def run(self):
        print("Unconnected: Waiting to connect to peers \n")

    def next(self, input):
        if input == "sent handshake":
            return WaitingResponse()
        
        if input == "Received Handshake": #Uploader
            return Connecting()
        return self

class Connected(State):
    def run(self):
        print("Connected to peer: \n")

    def next(self, input):
        if input == "Begin File sharing process":
            return DontHave()
        elif input == "Connection Timeout":
            return Unconnected()
        
        if input == "Begin File sharing process": #Uploader
            return Have()
        return self

class DontHave(State):
    def run(self):
        print("I Don't have piece \n")

    def next(self, input):
        if input == "Request File Piece":
            return Interested()
        elif input == "Connection Timeout":
            return Unconnected()
        return self


class Interested(State):
    def run(self):
        print("I'm Interested in piece: \n")

    def next(self, input):
        if input == "receive file piece":
            return Receiving()
        elif input == "Connection Timeout":
            return Unconnected()
        return self
    

class Receiving(State):
    def run(self):
        print("Receiving piece \n")

    def next(self, input):
        if input == "Receiving completed":
            return Have()
        elif input == "Receive Failed":
            return Interested()
        return self


class Have(State):
    def run(self):
        print("I have piece: \n")

    def next(self, input):
        if input == "Cancel File Request":
            return NotInterested()
        elif input == "Received piece corrupted":
            return DontHave()
        elif input == "Update with acquired pieces": #needs an update
            return PrepareNext()
        elif input == "Complete data received": #needs an update for updating with acquired pieces after download complete
            return DownComplete()
        
        if input == "File piece requested": #Uploader
            return Sending()
        return self


class NotInterested(State):
    def run(self):
        print("Not interested in that piece anymore \n")

    def next(self, input):
        if input == "Wait for next piece":
            return DontHave()
        return self


class PrepareNext(State):
    def run(self):
        print("Preparing for next piece \n")

    def next(self, input):
        if input == "Wait for next piece":
            return DontHave()
        elif input == "Connection Timeout":
            return Unconnected()
        return self


class DownComplete(State):
    def run(self):
        print("All downloading complete, data received \n")

    def next(self, input):
        if input == "close connections":
            return Idle()
        return self


class Connecting(State):
    def run(self):
        print("Connecting to peer \n")

    def next(self, input):
        if input == "Establish connection to peer":
            return Connected()
        return self
    

class Cancelling(State):
    def run(self):
        print("Cancelling send \n")

    def next(self, input):
        if input == "Upload to peer cancelled":
            return Have()
        return self


class Sent(State):
    def run(self):
        print("I have sent the piece \n")

    def next(self, input):
        if input == "Ready for next request":
            return Have()
        elif input == "Upload to peer completed":
            return UpComplete()
        return self


class Sending(State):
    def run(self):
        print("Sending piece to peer \n")

    def next(self, input):
        if input == "Sending file piece":
            return Sent()
        elif input == "Sending file piece failed":
            return Have()
        elif input == "Received request to cancel upload":
            return Cancelling()
        elif input == "Error sending file piece":
            return Sending()
        return self


class UpComplete(State):
    def run(self):
        print("Piece upload complete \n")

    def next(self, input):
        if input == "Close Connection to Peer":
            return Disconnected()
        elif input == "All uploads to peers completed":
            return Idle()
        return self


class Disconnected(State):
    def run(self):
        print("Disconnected from peer \n")

    def next(self, input):
        if input == "Wait for connection requests":
            return Unconnected()
        return self


class StateMachine():
    def __init__(self, initialState):
        self.currentState = initialState
        #self.currentState.run()
    
    def on_event(self, event):
        print(event)
        self.currentState = self.currentState.next(event)
        #print(type(self.currentState))
        self.currentState.run()
        return self.currentState
        
        
class PeerState(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Idle())