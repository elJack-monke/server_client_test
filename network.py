
import socket
import pickle
# Going to send and receive objects intead of strings -> use pickle instead of having to incode/decode

class network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '10.6.50.178'  # Home PC local IP address -> server host
<<<<<<< HEAD
        self.port = 5569
=======
        self.port = 6969
>>>>>>> e2554049d4494043debcf90963327a0f1306d9d1
        self.addr = (self.server, self.port)
        self.p = self.connect()  # This will be the player object thats created upon client connecting

    def get_p(self):
        return self.p  # gets the player object

    def connect(self):
        try:
            try: self.client.connect(self.addr)
            except: print('[network.py] connect(self.addr) failed work :(')
            
            try: return self.client.recv(2048).decode()  # initial info from server if player number
            except: print('[network.py] recv(2048) failed work :(')
        
        except: return 9

    def send(self, data):
        try:
            self.client.send( str.encode(data) )   # send string data to server

            test = self.client.recv(4096)
            gme = pickle.loads( test )

            return gme  # receive game object from server
        except socket.error as e: print(str(e))






