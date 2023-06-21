import threading

from server.tcp import ThreadedTCPServer
from server.request_handler import RequestHandler, Response

from framework.router import HttpRouter

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
            # Create a router if not provided
            # FIXME: It's not good to be dependent on the router in the HttpServer class. (I will fix it later)
            self.router = HttpRouter()

            # Create a default response
            response = Response(status_code=200, body="Hello World!")

            # Set content type to text/plain
            response.set_header("Content-Type", "text/plain")

            # Server name `FatihServer`
            response.set_header("Server", "FatihServer")

            # Add a default route
            self.router.add_route("/", lambda x: response)
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
        server = ThreadedTCPServer((self.host, self.port), RequestHandler)
        ip, port = server.server_address
        logger.info("🚀 FatihServer has launched at http://{}:{}".format(ip, port))

        self.server = server

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
