import os.path

from server.http_server import HttpServer
from server.request_handler import Response, Request
from framework.router import HttpRouter
from framework.static_files import StaticFiles

router = HttpRouter()

static = StaticFiles()

example_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FatihServer</title>
</head>
<body>
    <h1>Hello World!</h1>
    <img src="/static/img.png" alt="FatihServer">
    
    <h2>Example template:</h2>
    <img src="/static/dir/example.png" alt="FatihServer">
</body>
</html>
"""


@router.get("/index")
def index(request: Request, name: str):
    response = Response(status_code=200, body=example_html)
    response.set_header("Content-Type", "text/html")
    response.set_header("Server", "FatihServer")
    response.set_header("Connection", "close")
    response.set_header("Content-Length", len(example_html))

    print(request)

    return response


static.add_static_dir(directory="static")
static.add_static_file(path='static', file="favicon.ico")
router.add_static_route(static)


def server_start():
    server = HttpServer(router=router, host="localhost", port=8080)
    server.start()


if __name__ == "__main__":
    server_start()
