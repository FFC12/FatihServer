import socket
import unittest
from src.fatihserver.server.http_server import HttpServer

# TODO: Test is not working yet

case0 = """POST /cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/y-www-form-urlencoded
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

licenseID=string&content=string&/paramsXML=string
"""

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))


class TestHttpServer(unittest.TestCase):
    def test_http_server(self):
        server = HttpServer()
        server.start()

    def client_send(self):
        client("localhost", 8080, case0)