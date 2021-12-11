import errno
import queue
import select
import socket
import sys

class ServerSocket:

    def __init__(self, mode, port, onReceiveMsg, onCreateConn, onCloseConn, max_connections=1000, recv_bytes=2048):
        # Handle the socket's mode.
        # The socket's mode determines the IP address it binds to.
        # mode can be one of two special values:
        # localhost -> (127.0.0.1)
        # public ->    (0.0.0.0)
        # otherwise, mode is interpreted as an IP address.
        if mode == "localhost":
            self.ip = mode
        elif mode == "public":
            self.ip = socket.gethostname()
        else:
            self.ip = mode
            
        self.controlSocket = None
        self.clientSocket = []
        
        # Handle the socket's port.
        # This should be a high (four-digit) for development.
        self.port = port
        if type(self.port) != int:
            print("port must be an int", file=sys.stderr)
            raise ValueError

        # Save the callback
        self.onReceiveMsg = onReceiveMsg
        self.onCreateConn = onCreateConn
        self.onCloseConn = onCloseConn
        
        # Save the number of maximum connections.
        self._max_connections = max_connections
        if type(self._max_connections) != int:
            print("max_connections must be an int", file=sys.stderr)
            raise ValueError
        # Save the number of bytes to be received each time we read from
        # a socket
        self.recv_bytes = recv_bytes

    def run(self):
        # Start listening
        # Actually create an INET, STREAMing socket.socket.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Make it non-blocking.
        self._socket.setblocking(0)
        # Bind the socket, so it can listen.
        self._socket.bind((self.ip, self.port))

        self._socket.listen(self._max_connections)
        # Create a list of readers (sockets that will be read from) and a list
        readers = [self._socket]
        # Create a similar dictionary that stores IP addresses.
        # This dictionary maps sockets to IP addresses
        IPs = dict()
        self._stop = False

        # Now, the main loop.
        print("TCP 服务器已启动")
        while readers and not self._stop:
            #print("Block until a socket is ready for processing.")
            read, _, err = select.select(readers, [], readers)
            # Deal with sockets that need to be read from.
            for sock in read:
                if sock is self._socket:
                    # We have a viable connection!
                    try:
                        client_socket, client_ip = self._socket.accept()
                    except Exception:
                        break
                    
                    # Make it a non-blocking connection.
                    client_socket.setblocking(0)
                    # Add it to our readers.
                    readers.append(client_socket)
                    # Make a queue for it.
                    # queues[client_socket] = queue.Queue()
                    IPs[client_socket] = client_ip
                    self.onCreateConn(self, client_socket, client_ip)
                    print(f"readers length {len(readers)}")
                else:
                    # Someone sent us something! Let's receive it.
                    try:
                        data = sock.recv(self.recv_bytes)
                    except socket.error as e:
                        if e.errno == errno.ECONNRESET:
                            # Consider 'Connection reset by peer'
                            # the same as reading zero bytes
                            data = None
                        else:
                            raise e
                    if data:
                        self.onReceiveMsg(self, sock, IPs[sock], data)
                    else:
                        #print("We received zero bytes, so we should close the stream")
                        # Stop writing to it.
                        # Stop reading from it.
                        readers.remove(sock)
                        sock.close()
                        self.onCloseConn(self, sock, IPs[sock])
                        
            # Deal with erroring sockets.
            for sock in err:
                #print("Remove the socket from every list.")
                readers.remove(sock)
                # Close the connection.
                sock.close()

    def stop(self):
        self._stop = True
        self._socket.close()