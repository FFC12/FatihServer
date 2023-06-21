import chevron
from loguru import logger


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

    def add_template_as_file(self, name, path):
        """
        Add template as file.
        :param name:
        :param path:
        :return:
        """
        with open(path, "r") as f:
            self.templates[name] = {
                'content': f.read(),
                'path': path,
                'type': 'file'
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

    print(templates.render('index', {'name': 'Fatih'}))
