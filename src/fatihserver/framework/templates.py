import os

import chevron
from loguru import logger

from src.fatihserver.server.request_handler import Response



class TemplateResponse(Response):
    """
    TemplateResponse class for FatihServer
    """

    def __init__(self, template, name, payload):
        """
        Initialize TemplateResponse class with name and payload.
        :param name:
        :param payload:
        """
        super().__init__(status_code=200)
        self.name = name
        self.payload = payload
        self.template = template

        if self.template is None:
            raise Exception("Template is not defined.")

        if self.name is None:
            raise Exception("Template name is not defined.")

        if self.payload is None:
            raise Exception("Payload is not defined.")

        if not isinstance(self.payload, dict):
            raise Exception("Payload must be a dictionary.")

        if not isinstance(self.name, str):
            raise Exception("Template name must be a string.")

        if not isinstance(self.template, Templates):
            raise Exception("Template must be a Templates class.")

        # Render template
        self._render(self.template)

    def _render(self, template):
        """
        Render template.
        :param template: Templates class
        :return:
        """

        # Render template
        body = template.render(self.name, self.payload)

        # Set body
        self.set_body(body)

        # Set headers
        self.set_header("Content-Type", "text/html")

        # Set content length
        self.set_header("Content-Length", len(body))

        # Set server
        self.set_header("Server", "FatihServer")

        # Set connection
        self.set_header("Connection", "close")


class Templates:
    """
    Templates class for FatihServer

    TODO: I use `chevron` for template rendering. (but I will add support for jinja2 - no time for now)

    But technically, you can use any template engine you want, no restrictions with FatihServer.
    """

    def __init__(self):
        """
        """
        self.templates = {}

    def add_template_as_text(self, name, template):
        """
        Add template as text.
        :param name:
        :param template:
        :return:
        """
        self.templates[name] = {
            'content': template,
            'path': None,
            'type': 'text'
        }

    def add_template(self, name, path):
        """
        Add template as file.
        :param name:
        :param path:
        :return:
        """
        # check if path is file
        if not os.path.isfile(path):
            raise Exception("Path is not a file.")

        # open file
        with open(path, "r") as f:
            self.templates[name] = {
                'content': f.read(),
                'path': path,
                'type': 'file'
            }

    def add_templates(self, name, path):
        """
        Add template as directory.
        :param name:
        :param path:
        :return:
        """
        # check if path is directory
        if not os.path.isdir(path):
            raise Exception("Path is not a directory.")

        # walk recursively through the directory
        for root, dirs, files in os.walk(path):
            for file in files:
                # check if file is binary format
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot')):
                    continue

                # check if file is hidden
                if file.startswith(('.', '_')):
                    continue

                # check if file is 'html*', 'css*', 'js*', 'txt', 'json', 'xml'
                # TODO: add support for other file types
                if not file.endswith(('.html', '.css', '.js', '.txt', '.json', '.xml')):
                    continue

                # absolute system as full path in the system
                path = os.path.join(root, file)

                # remove '.' from path
                path = path.replace('./', '')

                # add template
                self.templates[path] = {
                    'content': path,
                    'path': path,
                    'type': 'directory'
                }

    def get_template(self, name):
        """
        Get template.
        :param name:
        :return:
        """
        try:
            return self.templates[name]
        except KeyError:
            logger.error("Template not found.")
            raise Exception("Template not found.")

    def render(self, name, payload):
        """
        Render template.
        :param name:
        :param payload:
        :return:
        """
        try:
            data = chevron.render(self.templates[name]['content'], payload)
            return data
        except KeyError:
            logger.error("Template not found.")
            raise Exception("Template not found.")
        except Exception as e:
            logger.error("Error while rendering template: " + str(e))
            raise Exception("Error while rendering template: " + str(e))



if __name__ == "__main__":
    templates = Templates()
    templates.add_template_as_text('index', """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FatihServer</title>
    </head>
    <body>
        <h1>Hello {{ name }}!</h1>
    </body>
    </html>
    """)


    s = TemplateResponse(templates, 'index', {'name': 'Fatih'})
    print(s)