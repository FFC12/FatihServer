import os
from loguru import logger


class HttpRequestParser:
    """
    HTTP request parser class

    This class parses HTTP request and returns a dictionary with the following keys:
    - method
    - path
    - version
    - headers
          - key: value
    - body
    """

    def __init__(self):
        self.headers = {}
        self.request_method = None
        self.body = None
        self.raw_body = None
        self.query_params = None

    def _parse_method(self, lines):
        """
        Parse method, path and version and pass the rest to _parse_headers

        :param lines:
        :return:
        """
        parts = lines[0].split(' ')

        if len(parts) == 3:
            method = lines[0].split(' ')[0]
            path = lines[0].split(' ')[1]
            version = lines[0].split(' ')[2]
        else:
            if len(parts) < 2:
                method = lines[0].split(' ')[0]
                path = '/'
                version = ''
            else:
                method = lines[0].split(' ')[0]
                path = lines[0].split(' ')[1]
                version = ''

        # trim ' ' from method, path and version
        method = method.strip()
        version = version.strip()

        # query string '?'
        if '?' in path:
            # split path by '?'
            path, query_string = path.split('?')

            # parse query string
            query_string = query_string.split('&')

            # create a dictionary
            query_string_dict = {}
            for query in query_string:
                query_string_dict[query.split('=')[0]] = query.split('=')[1]

            self.query_params = query_string_dict

        # split path by '/' and trim ' ' from each part
        path = path.strip().split('/')

        # if path is empty, set it to '/'
        if path == ['']:
            path = ['/']

        # if path is absolute uri, split it by third '/'
        # and set path to the last part
        if path[0] == 'http:' or path[0] == 'https:':
            path = path[3:]
        else:
            path = path[1:]

        path = '/' + '/'.join(path)

        # pop the first line
        lines.pop(0)

        self.request_method = {
            'method': method,
            'path': path,
            'version': version
        }

        # now first line is headers
        return self._parse_headers(lines)

    def _parse_headers(self, lines):
        """
        Parse headers and pass the rest to _parse_body

        :param lines:
        :return:
        """
        counter = 0
        for line in lines:
            counter += 1
            line = line.replace('\r', '').strip()

            if line == '':
                # end of headers
                break

            # split line by ':' and trim ' ' from key and value
            key = (line.split(':')[0]).strip()
            value = (line.split(':')[1]).strip()

            # if key is 'Cookie', split it by ';'
            # and add it to headers as a dictionary
            cookies = {}
            if key == 'Cookie':
                # split cookies by ';'
                cookie_list = value.split(';')
                for cookie in cookie_list:
                    # split cookie by '='
                    cookie_key = cookie.split('=')[0].strip()
                    cookie_val = cookie.split('=')[1].strip()

                    cookies[cookie_key] = cookie_val

            self.headers[key] = value if key != 'Cookie' else cookies

        for i in range(counter):
            lines.pop(0)

        # now first line is body
        return self._parse_body(lines)

    def _parse_body(self, lines):
        """
        Parse body and return the result

        :param lines:
        :return:
        """
        # if there's only spaces left
        if lines[0].strip() != '':
            # we have only body left so join them
            # if you are using windows, use '\r\n' instead of '\n'
            if os.name == 'posix':
                body = '\n'.join(lines)
            else:
                body = '\r\n'.join(lines)

            # save raw body
            self.raw_body = body

            # parse body by 'Content-Type' header
            if 'Content-Type' in self.headers:
                try:
                    if self.headers['Content-Type'] == 'application/y-www-form-urlencoded':
                        # parse body as url encoded
                        body = {
                            "type": "url_encoded",
                            "data": self._parse_url_encoded(body)
                        }
                    elif self.headers['Content-Type'] == 'application/json':
                        # parse body as json
                        body = {
                            "type": "json",
                            "data": self._parse_json(body)
                        }
                    elif self.headers['Content-Type'] == 'text/plain':
                        # parse body as text
                        body = {
                            "type": "text",
                            "data": self._parse_text(body)
                        }
                    elif 'multipart/form-data' in self.headers['Content-Type']:
                        # parse body as multipart
                        body = {
                            "type": "multipart",
                            "data": self._parse_text(body)
                        }

                        logger.warning('Multipart form data is not supported yet')
                        #boundary = self.headers['Content-Type'].split(';')[1].split('=')[1]
                        #body = self._parse_multipart(body, boundary)
                    else:
                        # parse body as text
                        body = {
                            "type": "text",
                            "data": self._parse_text(body)
                        }
                except Exception as e:
                    logger.error(e)
                    # parse body as text
                    body = {
                            "type": "text",
                            "data": self._parse_text(body)
                    }
            else:
                # parse body as text
                body = {
                    "type": "text",
                    "data": self._parse_text(body)
                }
        else:
            body = None

        self.body = body
        return {
            'method': self.request_method['method'],
            'path': self.request_method['path'],
            'version': self.request_method['version'],
            'headers': self.headers,
            'body': self.body,
            'raw_body': self.raw_body,
            'query_params': self.query_params
        }

    def _parse_url_encoded(self, body):
        """
        Parse url encoded body

        :param body:
        :return:
        """
        # split body by '&'
        body = body.split('&')

        # parse body
        result = {}
        for item in body:
            key = item.split('=')[0]
            value = item.split('=')[1].strip('\n')

            result[key] = value

        return result

    def _parse_json(self, body):
        """
        Parse json body

        :param body:
        :return:
        """
        import json

        return json.loads(body)

    def _parse_text(self, body):
        """
        Parse text body

        :param body:
        :return:
        """
        return body

    def parse(self, data):
        # split data into lines
        # if it's windows, use '\r\n' instead of '\n'
        if os.name == 'posix':
            lines = data.split('\n')
        else:
            lines = data.split('\r\n')

        # Top-down parsing of HTTP request
        return self._parse_method(lines)

    def _parse_multipart(self, body, boundary):
        #FIXME: complete this method
        #BUG: this method is not working properly

        # split body by boundary
        body = body.split('--' + boundary.strip('"'))

        # remove first and last element
        body.pop(0)
        body.pop(len(body) - 1)


        # parse body
        result = {}
        for item in body:
            # split item by '\n\n'
            item = item.split('\n\n')

            # first part is headers
            headers = item[0].split('\n')

            # parse headers
            headers_dict = {}
            for header in headers:
                # split header by ':' and trim ' ' from key and value
                key = (header.split(':')[0]).strip()
                value = (header.split(':')[1]).strip()

                headers_dict[key] = value

            # second part is body
            body = item[1]

            body = body.replace('\n', '').replace('\r', '').strip()

            # add to result
            result[headers_dict['name']] = {
                'headers': headers_dict,
                'body': body
            }

        return result
