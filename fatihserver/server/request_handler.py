"""
Request handler for *FatihServer*
- It is not a complete web server, it is just a simple web server but it works as expected

Note: This is a simple web server that I developed for my own website (for fun and learning purposes)

- Author
    FFC12 ![ffc12](github.com/ffc12)
"""

import asyncio
import json
import socketserver
import sys
from datetime import datetime
from socketserver import BaseRequestHandler
import threading
from hashlib import sha256
from traceback import print_exc
import inspect
from typing import get_type_hints

from fatihserver.parsers.http_parser import HttpRequestParser
import mimetypes

from loguru import logger


class HttpResult:
    """
    HttpResult class for FatihServer

    Contains status code, headers and body for many HTTP status codes
    """

    @staticmethod
    def r404():
        response = Response(status_code=404, body="Not Found")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r500():
        response = Response(status_code=500, body="Internal Server Error")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r501():
        response = Response(status_code=501, body="Not Implemented")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r200():
        response = Response(status_code=200, body="OK")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r400():
        response = Response(status_code=400, body="Bad Request")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r403():
        response = Response(status_code=403, body="Forbidden")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r405():
        response = Response(status_code=405, body="Method Not Allowed")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r301():
        response = Response(status_code=301, body="Moved Permanently")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r302(self):
        response = Response(status_code=302, body="Found")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r201():
        response = Response(status_code=201, body="Created")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r204():
        response = Response(status_code=204, body="No Content")
        response.set_header("Content-Type", "text/plain")

        return response

    @staticmethod
    def r202():
        response = Response(status_code=202, body="Accepted")
        response.set_header("Content-Type", "text/plain")

        return response


class Request:
    """
    Request class for FatihServer
    """

    def __init__(self, method=None, path=None, raw_body=None, headers=None, body=None, query_params=None):
        """
        Initialize Request class with method, path, headers, body and query parameters.
        :param method:
        :param path:
        :param headers:
        :param body:
        """
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.raw_body = raw_body
        self.query_params = query_params


class Response:
    """
    Response class for FatihServer
    """

    def __init__(self,
                 status_code=200,
                 session=None,
                 method=None,
                 headers=None,
                 content_type=None,
                 body=None):
        """
        Initialize Response class with status code, method, headers and body.
        :param status_code:
        :param method:
        :param headers:
        :param body:
        """
        self.status_code = status_code
        self.method = method
        self.headers = headers
        self.body = body
        self.content_type = content_type
        self.session = session

        if self.session is None:
            self.session = Session()

        self.set_session(self.session)

    def set_cookie(self, key, value):
        """
        Set cookie
        :param key:
        :param value:
        :return:
        """
        self.set_header('Set-Cookie', f"{key}={value}")

    def _set_session_id(self, session_id):
        """
        Set session id
        :param session_id:
        :return:
        """
        self.set_cookie('session_id', session_id)
        self.set_cookie('SameSite', 'Lax')

    def set_session(self, session):
        """
        Set session
        :param session:
        :return:
        """
        self.session = session

        if session is not None:
            self._set_session_id(session.session_id)
        else:
            logger.warning("Session is None. Session id will not be set.")

    def set_header(self, key, value):
        """
        Set header
        :param key:
        :param value:
        :return:
        """
        if self.headers is None:
            self.headers = {}

        if key in self.headers:
            logger.debug(f"Header with key {key} already exists. Appending value to existing cookie.")
            self.headers[key] += f"; {value}"
        else:
            self.headers[key] = value

    def set_cache_control(self, cache_control):
        """
        Set cache control
        :param cache_control:
        :return:
        """
        self.set_header('Cache-Control', cache_control)

    def set_content_length(self, content_length):
        """
        Set content length
        :param content_length:
        :return:
        """
        self.set_header('Content-Length', content_length)

    def set_content_type(self, content_type):
        """
        Set content type
        :param content_type:
        :return:
        """
        self.content_type = content_type
        self.set_header('Content-Type', content_type)

    def set_date(self, date):
        """
        Set date
        :param date:
        :return:
        """
        self.set_header('Date', date)

    def set_body(self, body):
        """
        Set body
        :param body:
        :return:
        """
        self.body = body

    def as_bytes(self):
        """
        String representation of Response class *FatihServer*
        :return:
        """
        headers = ""
        if self.headers is not None:
            for key, value in self.headers.items():
                headers += f"{key}: {value}\r\n"

        method_str = ""
        if self.status_code == 200:
            method_str = 'OK'
        elif self.status_code == 201:
            method_str = 'Created'
        elif self.status_code == 204:
            method_str = 'No Content'
        elif self.status_code == 404:
            method_str = 'Not Found'
        elif self.status_code == 405:
            method_str = 'Method Not Allowed'
        elif self.status_code == 403:
            method_str = 'Forbidden'
        elif self.status_code == 501:
            method_str = 'Not Implemented'
        elif self.status_code == 500:
            method_str = 'Internal Server Error'
        elif self.status_code == 400:
            method_str = 'Bad Request'
        else:
            method_str = 'Unknown'

        if self.content_type is not None:
            if self.content_type == 'application/json':
                return bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" \
                             f"{headers} \r\n\r\n" \
                             f"{json.dumps(self.body)}", 'utf-8')
            elif self.content_type == 'text/html':
                return bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" \
                             f"{headers} \r\n\r\n" \
                             f"{self.body}", 'utf-8')
            elif self.content_type == 'text/plain':
                return bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" \
                             f"{headers} \r\n\r\n" \
                             f"{self.body}", 'utf-8')
            elif self.content_type == 'image/png' \
                    or self.content_type == 'image/jpeg' \
                    or self.content_type == 'image/jpg' \
                    or self.content_type == 'image/gif' \
                    or self.content_type == '.otf' \
                    or self.content_type == '.woff' \
                    or self.content_type == '.ttf' \
                    or self.content_type == '.woff2' \
                    or self.content_type == '.eot':
                # binary
                pack = bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" f"{headers} \r\n\r\n", 'utf-8')
                print(self.content_type)
                data = self.body

                return pack + data
            else:
                return bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" \
                             f"{headers} \r\n\r\n" \
                             f"{self.body}", 'utf-8')
        else:
            return bytes(f"HTTP/1.1 {self.status_code} {method_str}\n" \
                         f"{headers} \r\n\r\n" \
                         f"{self.body}", 'utf-8')


class Session:
    ACTIVE = {}

    def __init__(self, session_id=None, data=None, created_at=None):
        """
        Session class
        :param session_id:
        :param data:
        :param created_at:
        """
        if session_id is not None:
            self.session_id = session_id
        else:
            # Generate session id
            self.session_id = Session.generate_session_id()
            Session.ACTIVE[self.session_id] = {
                'session_id': self.session_id,
                'data': {} if data is None else data,
                'created_at': datetime.now() if created_at is None else created_at
            }

    def __repr__(self):
        return f"{self.session_id}"

    def __str__(self):
        return f"{self.session_id}"

    @staticmethod
    def get_session(session_id):
        """
        Get session
        :param session_id:
        :return:
        """
        if session_id in Session.ACTIVE:
            return Session.ACTIVE[session_id]
        else:
            return None

    @staticmethod
    def check_session_id_is_valid(session_id):
        """
        Check if session id is valid
        :param session_id:
        :return:
        """
        if session_id in Session.ACTIVE:
            return True
        else:
            return False

    @staticmethod
    def generate_session_id():
        """
        Generate a session id

        :return:
        """
        # Generate a random string
        random_string = datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Hash the string
        hashed_string = sha256(random_string.encode()).hexdigest()

        # Return the hashed string
        return hashed_string


class RequestHandler(BaseRequestHandler):
    """
    Currently, I use socketserver. So I need to use this class to handle requests
    But I will implement my TCP server in the future (I hope so - if I have time)
    """

    def __init__(self, router=None):
        self.parser = None
        # get the router from args
        self.router = router
        self.lock = None

    def __call__(self, request, client_address, server):
        """
        Call method for RequestHandler (we need to override this method
        because we need to pass router to RequestHandler)
        :param request:
        :param client_address:
        :param server:
        :return:
        """
        h = RequestHandler(self.router)
        socketserver.BaseRequestHandler.__init__(h, request, client_address, server)

    def setup(self) -> None:
        self.lock = threading.Lock()

        logger.debug(f"New connection from {self.client_address}")

    def handle(self):
        # Get data from client
        data = str(self.request.recv(1024), 'ascii')

        # Create a new HttpRequestParser (I know it is not efficient)
        # FIXME: Make it efficient (instance for each request is not efficient)
        http_parser = HttpRequestParser()

        try:
            # Parse data
            result = http_parser.parse(data)
        except Exception as e:
            logger.error(e)

            print_exc()

            # 400 Bad Request (if we cannot parse the request)
            result = HttpResult.r400()

            # Send data to client
            return self.request.sendall(result.as_bytes())

        # Get method
        method = result['method']

        # Check if method is supported (GET, POST, PUT, DELETE, OPTIONS, HEAD)
        # Still not implemented all of them (not standardized responses)
        try:
            if method == 'GET' \
                    or method == 'POST' \
                    or method == 'PUT' \
                    or method == 'DELETE' \
                    or method == 'OPTIONS' \
                    or method == 'HEAD':

                if (method == 'GET' or method == 'OPTIONS') \
                        and result['body'] is not None:
                    # GET and OPTIONS should not have body (RFC 7231)
                    # https://www.rfc-editor.org/rfc/rfc7231#section-4.3.1
                    result = HttpResult.r400()
                    return self.request.sendall(result.as_bytes())

                result = self._handle_method(result)
            else:
                logger.warning(f"Method not supported - {result['method']} - {result['path']}")
                result = HttpResult.r400()
        except Exception as e:
            logger.error(e)
            print_exc()
            result = HttpResult.r405()

        cur_thread = threading.current_thread()
        logger.debug(f"{cur_thread}: {result.headers} - {result.body}")
        self.request.sendall(result.as_bytes())

    def _handle_method(self, result):
        """
        Handle GET request

        :param result:
        :return:
        """
        # Get path
        path = result['path']

        user_agent = None
        if result['headers'] is not None:
            if 'User-Agent' in result['headers']:
                user_agent = result['headers']['User-Agent']

        cookies = None
        if result['headers'] is not None:
            if 'Cookie' in result['headers']:
                cookies = result['headers']['Cookie']

        # Check if path exists in router and get function to execute
        exists, func = self.router.exist(path, result['method'])

        # If path exists, execute function
        if exists:
            # Lock the thread
            self.lock.acquire()

            func, args = self._handle_func_args(func, result)

            # check if function is a coroutine
            if asyncio.iscoroutinefunction(func):
                logger.debug("Function is a coroutine")

            # Execute function
            result = func(*args)

            # Release the thread
            self.lock.release()

            if isinstance(result, Response):
                if cookies is None or 'session_id' not in cookies:
                    # Add session id to cookies
                    result.set_session(Session())
                else:
                    # Check session id is valid
                    session_id = cookies['session_id']

                    if Session.check_session_id_is_valid(session_id):
                        # Set session id to cookies
                        result.set_session(Session(session_id=session_id))
                    else:
                        # Add session id to cookies
                        result.set_session(Session())

                return result
            else:
                # Check if session id exists
                if cookies is not None and 'session_id' in cookies:
                    # Session id exists, set it from cookies
                    session_id = cookies['session_id']

                    # Create response. result is not 'Response' instance
                    if not isinstance(result, str):
                        result = str(result)

                    # we create a respone for raw-text
                    response = Response(status_code=200, body=result)

                    # Content-Type is Text-plain
                    response.set_header('Content-Type', 'text/plain')

                    # Set session id to cookies
                    response.set_session(Session(session_id=session_id))
                else:
                    # Create response
                    response = HttpResult.r200()

                # Set session id to cookies
                return response
        else:
            # it would be static file

            # To adapt the path to static path, '/' should be removed
            path = path[1:]

            # Check if static file exists and get it
            exists, static_file = self.router.static_path_exists(path)

            logger.debug(f"Static file exists: {exists}")
            logger.debug(f"Path {path}")

            if exists:
                # Check if static file exists
                if static_file is not None:
                    # Get file extension
                    file_extension = path.split('.')[-1]

                    # Create response
                    response = Response(status_code=200)

                    # check if it's a mime-type
                    if f'.{file_extension}' in mimetypes.types_map:
                        # Get content type
                        content_type = mimetypes.types_map[f".{file_extension}"]

                        # Set content type
                        response.set_content_type(content_type)
                    else:
                        response.set_content_type(f'.{file_extension}')

                    # Set content length
                    response.set_content_length(len(static_file))

                    # Set cache control
                    response.set_cache_control('max-age=3600')

                    # Set body
                    response.set_body(static_file)

                    # Set date
                    response.set_date(datetime.now())

                    # Check if session id exists
                    if cookies is None or 'session_id' not in cookies:
                        # Set session id to cookies
                        response.set_session(Session())
                    else:
                        # Session id exists, set it from cookies
                        session_id = cookies['session_id']

                        # Check session id is valid
                        if Session.check_session_id_is_valid(session_id):
                            # Set session id to cookies
                            response.set_session(Session(session_id=session_id))
                        else:
                            # Add session id to cookies
                            response.set_session(Session())

                    # Return response
                    return response
                else:
                    # Static file does not exist, return 404
                    logger.warning(f"Static file does not exist - {result['method']} - {path}")
                    logger.error("Unexpected behaviour")
                    return HttpResult.r404()

        # Path does not exist, return 404
        logger.warning(f"Path does not exist - {result['method']} - {path}")
        return HttpResult.r404()

    def _handle_func_args(self, func, result):
        """
        Handle arguments of router function
        :param func:
        :param result:
        :return:
        """
        # Get cookies
        try:
            cookies = result['headers']['Cookie']
        except KeyError:
            cookies = None

        method = result['method']

        # Create local thread for arguments
        local = threading.local()
        local.args = []

        # check if func has parameters
        if func.__code__.co_argcount > 0:
            # get parameters of function
            params = inspect.signature(func).parameters

            # get type hints of function
            type_hints = get_type_hints(func)

            # TODO: Add more types?
            # TODO: Query parameters will be added
            for param_name, param in params.items():
                # get type of parameter
                try:
                    param_type = type_hints[param_name]
                except KeyError:
                    param_names = func.__code__.co_varnames
                    logger.debug(f'The parameter `{param_names}` does not have any type hints. '
                                 f'It must have type hints; otherwise, the arguments of the route '
                                 f'function will be set as `None`.')
                    local.args.append(None)
                    continue

                # check the name of type of parameter
                if param_type == Request:
                    # Request type, add the request
                    request = Request(method=result['method'],
                                      path=result['path'],
                                      headers=result['headers'],
                                      raw_body=result['raw_body'],
                                      body=result['body'],
                                      query_params=result['query_params'])

                    local.args.append(request)
                elif param_type == Session:
                    if cookies is not None and 'session_id' in cookies:
                        # Session id exists, get the session
                        session_id = cookies['session_id']

                        # Add the session to the arguments
                        local.args.append(Session.get_session(session_id))
                else:
                    logger.warning(f"Unknown parameter type - {param_name} - {param_type}")
                    logger.warning(f"Probably we don't support this type yet but we need to add as argument")
                    local.args.append(None)

        # return the function and the arguments
        return func, local.args
