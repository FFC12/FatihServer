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
</body>
</html>
"""

templates.add_template_as_text('index', example_html)


@router.get("/index")
def index(request: Request):
    return TemplateResponse(templates, 'index', request.query_params)


@router.post("/index")
def index_post(request: Request):
    request_body = request['body']


if __name__ == "__main__":
    app = App(router=router, host="localhost", port=8080)
    app.run()
