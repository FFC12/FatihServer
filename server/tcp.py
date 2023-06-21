import socket
import threading
from socketserver import BaseRequestHandler, ThreadingMixIn, TCPServer


# TODO: We will implement our own TCP Server in the future
class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass
