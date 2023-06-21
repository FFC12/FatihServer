from server.http_server import HttpServer
from server.request_handler import Response, Request
from framework.router import HttpRouter


router = HttpRouter()


example_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FatihServer</title>
</head>
<body>
    <h1>Hello World!</h1>
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


def server_start():
    server = HttpServer(router=router, host="localhost", port=8080)
    server.start()


if __name__ == "__main__":
    server_start()