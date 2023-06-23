from fatihserver.server.http_server import HttpServer

from loguru import logger


class App:
    """
    App class for FatihServer

    TODO:
        - App startup and shutdown hooks (router)
    """

    def __init__(self, app_name=None, router=None, host="localhost", port=8080):
        """
        Initialize App class with app_name.
        :param app_name:
        """
        self.app_name = app_name
        self.server = HttpServer(router=router, host=host, port=port)

    def run(self):
        """
        Run the server.
        :return:
        """
        logger.info("🧞‍♂️ Web app has started. Creating and launching the FatihServer...")
        self.server.start()
