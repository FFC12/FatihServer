from fatihserver.server.request_handler import Request
from fatihserver.framework.router import HttpRouter
from fatihserver.framework.static_files import StaticFiles
from fatihserver.framework.templates import Templates, TemplateResponse

from fatihserver.framework.app import App, set_log_level

set_log_level('INFO')

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
    if request.query_params is None:
        return TemplateResponse(templates, 'index', {'name': 'Fatih'})
    else:
        return TemplateResponse(templates, 'index', request.query_params)


if __name__ == "__main__":
    app = App(router=router, host="localhost", port=8080)
    app.run()
