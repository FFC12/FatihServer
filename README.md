## FatihServer (WIP)

FatihServer is a Web Framework that I developed for my personal website. I built the HttpServer from scratch (almost) and the framework is built on top of it. It is a very simple framework and needs still a lot of work. But, I will be adding more features to it as I go.

## Table of Contents
- [FatihServer (WIP)](#fatihserver-wip)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Usage](#usage)
  - [Routing](#routing)
  - [Static Files](#static-files)
  - [Templates](#templates)
  - [Conclusion](#conclusion)
  - [License](#license)

### Features
- [x] HttpServer
- [x] Routing
- [ ] Query Parameters (Not yet)
- [x] Static Files
- [x] Templates
- [x] Session (HttpSession)
- [x] Cookies
- [x] Request (simple)
- [x] Response (class based)
- [ ] Middleware (Not yet)
- [ ] Database (Not yet)
- [ ] Authentication (Not yet)
- [ ] CORS (Not yet)
- [ ] WebSockets (Not yet)
- [ ] SSL (Not yet)

### Usage
Here is a simple example of how to use the HttpServer.
```python
from server.http_server import HttpServer

server = HttpServer()
server.start()
```

### Routing
Routing is like Flask and FastAPI (I inspired a lot). You can use it like this:
```python
from server.http_server import HttpServer
from server.request_handler import Response, Request
from framework.router import HttpRouter

# Create a router
router = HttpRouter()

# Example html
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


# Add a route to the router
@router.get("/index")
def index(request: Request, name: str):
    response = Response(status_code=200, body=example_html)
    response.set_header("Content-Type", "text/html")
    response.set_header("Server", "FatihServer")
    response.set_header("Connection", "close")
    response.set_header("Content-Length", len(example_html))

    print(request)

    return response


# Start the server
def server_start():
    server = HttpServer(router=router, host="localhost", port=8080)
    server.start()

# Run the server
if __name__ == "__main__":
    server_start()
```

### Static Files
You can serve static files with FatihServer. You can use it like this:
```python
from server.http_server import HttpServer
from server.request_handler import Response, Request
from framework.router import HttpRouter
from framework.static import StaticFiles

# Create a router
router = HttpRouter()

# Create a static file handler
static = StaticFiles()

# Add a route to the router
@router.get("/index")
def index(request: Request, name: str):
    response = Response(status_code=200, body=example_html)
    response.set_header("Content-Type", "text/html")
    response.set_header("Server", "FatihServer")
    response.set_header("Connection", "close")
    response.set_header("Content-Length", len(example_html))

    print(request)

    return response


# Add a static file route
static.add_static_route("/static", "static")

# Start the server
def server_start():
    server = HttpServer(router=router, host="localhost", port=8080)
    server.start()

# Run the server
if __name__ == "__main__":
    server_start()
```

### Templates
You can use templates with FatihServer. You can use it like this:
```python
from server.http_server import HttpServer
from server.request_handler import Response, Request
from framework.router import HttpRouter
from framework.static import StaticFiles
from framework.templates import Templates

# Create a router
router = HttpRouter()

# Create a static file handler
static = StaticFiles()

# Create a template handler
templates = Templates()

# Add a route to the router
@router.get("/index")
def index(request: Request, name: str):
    response = Response(status_code=200, body=example_html)
    response.set_header("Content-Type", "text/html")
    response.set_header("Server", "FatihServer")
    response.set_header("Connection", "close")
    response.set_header("Content-Length", len(example_html))

    print(request)

    return response


# Add a static file route
static.add_static_route("/static", "static")

# Add a template route
templates.add_template_route("/templates", "templates")

# Start the server
def server_start():
    server = HttpServer(router=router, host="localhost", port=8080)
    server.start()

# Run the server
if __name__ == "__main__":
    server_start()
```

### Conclusion
This project is for my personal website and right now, my website at [here](https://google.com) is running on FatihServer. 

### Why FatihServer?

I named it FatihServer because my name is Fatih and I'm not really good at naming things. Sorry for that

### License
MIT License


