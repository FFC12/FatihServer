from src.fatihserver.server.request_handler import Request
from src.fatihserver.framework.router import HttpRouter
from src.fatihserver.framework.static_files import StaticFiles
from src.fatihserver.framework.templates import Templates, TemplateResponse

from src.fatihserver.framework.app import App

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
