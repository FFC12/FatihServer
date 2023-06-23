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
- [x] Static Files
- [x] Templates
- [x] Session (HttpSession)
- [x] Cookies
- [x] Request (simple)
- [x] Response (class based)


### TODOs
- [ ] Add more tests
- [ ] Query Parameters (very soon)
- [ ] Uvicorn support
- [ ] Middleware Layer
- [ ] Database (Middleware, ORM, etc.)
- [ ] Authentication (JWT, OAuth, etc.)
- [ ] CORS (Middleware)
- [ ] WebSockets (Middleware)
- [ ] SSL (Middleware)
- [ ] Make it async (change the HttpServer to async?)
- [ ] Package it and upload to PyPI

### Usage
Here is a simple example of how to use the HttpServer.

```python
from fatihserver.framework import App

app = App()
app.run()
```

### Routing
Routing is like Flask and FastAPI (I inspired a lot). You can use it like this:

```python
from fatihserver.framework import App
from fatihserver.server.request_handler import Response, Request
from fatihserver.framework import HttpRouter

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

  return response


# Run the server
if __name__ == "__main__":
  app = App(router=router, host="localhost", port=8080)
  app.run()
```

### Static Files
You can serve static files with FatihServer. You can use it like this:

```python
from fatihserver.framework import App
from fatihserver.server.request_handler import Response, Request
from fatihserver.framework import HttpRouter
from fatihserver.framework import StaticFiles

# Create a router
router = HttpRouter()

# Create a static file handler
static = StaticFiles()

# Example html
example_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FatihServer</title>
</head>
<body>
    <h1>Hello World</h1>
    <img fatihserver="/static/example.jpg" alt="FatihServer">
</body>
</html>
"""


# Add a route to the router
@router.get("/index")
def index(request: Request):
  response = Response(status_code=200, body=example_html)
  response.set_header("Content-Type", "text/html")
  response.set_header("Server", "FatihServer")
  response.set_header("Connection", "close")
  response.set_header("Content-Length", len(example_html))

  return response


# Add a static file route
static.add_static_dir(directory="static")
router.add_static_route(static)

# Run the server
if __name__ == "__main__":
  app = App(router=router, host="localhost", port=8080)
  app.run()
```

### Templates
You can use templates with FatihServer. You can use it like this:

```python
from fatihserver.server.request_handler import Response, Request
from fatihserver.framework import HttpRouter
from fatihserver.framework.static_files import StaticFiles
from fatihserver.framework import Templates, TemplateResponse

from fatihserver.framework import App

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
    <img fatihserver="/static/example.jpg" alt="FatihServer">
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
```

### Conclusion
This project is for my personal website and right now, my website at [here](https://google.com) is running on FatihServer. 

### Why FatihServer?

I named it FatihServer because my name is Fatih and I'm not really good at naming things. Sorry for that

### License
MIT License


