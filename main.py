from server.request_handler import Response, Request
from framework.router import HttpRouter
from framework.static_files import StaticFiles
from framework.templates import Templates, TemplateResponse

from framework.app import App

router = HttpRouter()

static = StaticFiles()
templates = Templates()

example_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FatihServer</title>
</head>
<body>
    <h1>Hello {{ name }}</h1>
    <img src="/static/example.jpg" alt="FatihServer">
</body>
</html>
"""

templates.add_template_as_text('index', example_html)


@router.get("/index")
def index(request: Request):
    return TemplateResponse(templates, 'index', {'name': 'Fatih'})


static.add_static_dir(directory="static")
router.add_static_route(static)


if __name__ == "__main__":
    app = App(router=router, host="localhost", port=8080)
    app.run()
