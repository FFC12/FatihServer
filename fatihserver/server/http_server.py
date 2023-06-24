import threading

from fatihserver.server.tcp import ThreadedTCPServer
from fatihserver.server.request_handler import RequestHandler

from fatihserver.framework.router import HttpRouter

from loguru import logger


class HttpServer:
    """
    HttpServer class for FatihServer

    Here are some TODOs:
        TODO: Add support for HTTPS
        TODO: Add more HTTP methods
        TODO: Add static file serving
        TODO: Add support for middlewares
        (Also, there are TODOs in the request_handler.py)
    """
    def __init__(self, router=None, host="localhost", port=8080):
        """
        Initialize HttpServer class with router, host and port.
        :param router:
        :param host:
        :param port:
        """
        self.host = host
        self.port = port
        self.server = None

        if router is None:
            self.router = HttpRouter()
        else:
            self.router = router

    def add_route(self, path, handler):
        """
        Add route to router.
        :param path:
        :param handler:
        :return:
        """
        self.router.add_route(path, handler)

    def start(self):
        """
        Start the server.
        :return:
        """
        self.router.serve_static_files()

        # We need to set allow_reuse_address to True because we want to be able to restart the server
        ThreadedTCPServer.allow_reuse_address = True

        # Create server
        server = ThreadedTCPServer((self.host, self.port), RequestHandler(self.router))

        # Get server address
        ip, port = server.server_address
        logger.info("🚀 FatihServer has launched at http://{}:{}".format(ip, port))

        # Set server
        self.server = server

        # Serve forever
        with server:
            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            server_thread = threading.Thread(target=server.serve_forever())

            # Exit the server thread when the main thread terminates
            server_thread.daemon = True

            # Start the server thread
            server_thread.start()

            logger.info("Spawned Thread: ", server_thread.name)


    def stop(self):
        """
        Stop the server.
        :return:
        """
        self.server.shutdown()
        logger.info("Server stopped")
