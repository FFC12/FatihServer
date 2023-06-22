import functools
import os
import threading

from framework import static_files
from framework.static_files import StaticFiles


class HttpRouter:
    """
    Route class for registering routes.
    """
    # instance
    _instance = None

    # lock for thread safety
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    # Thread-safe dictionary for storing routes (built-in dicts are already thread-safe)
                    cls.GET_PATHS = {}
                    cls.POST_PATHS = {}
                    cls.PATCH_PATHS = {}
                    cls.PUT_PATHS = {}
                    cls.DELETE_PATHS = {}
                    cls.STATIC_PATHS = []
                    cls.SERVED_STATIC_PATHS = {}

                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the class with empty dictionaries for each HTTP method.
        """
        pass


    def add_static_route(self, static: StaticFiles):
        """
        Add static route.
        :param static:
        :return:
        """
        if isinstance(static, static_files.StaticFiles):
            files = static.get_static_files()
            dirs = static.get_static_dirs()

            for path, file in files.items():
                # check if it conflicts with other routes
                if path in self.GET_PATHS \
                        or path in self.POST_PATHS \
                        or path in self.PATCH_PATHS \
                        or path in self.PUT_PATHS \
                        or path in self.DELETE_PATHS:
                    raise Exception("Static route (file) conflicts with other routes.")
                else:
                    # combine path and file
                    combined_path = path + file

                    # also check if in the STATIC_PATHS
                    for static_path in self.STATIC_PATHS:
                        if static_path['path'] == combined_path:
                            raise Exception("Static route (file) conflicts with other routes.")

                    # add to STATIC_PATHS
                    self.STATIC_PATHS.append({
                        'path': combined_path,
                        'is_dir': False,
                    })

            for path, directory in dirs.items():
                # check if it conflicts with other routes
                if path in self.GET_PATHS \
                        or path in self.POST_PATHS \
                        or path in self.PATCH_PATHS \
                        or path in self.PUT_PATHS \
                        or path in self.DELETE_PATHS:
                    raise Exception("Static route (directory) conflicts with other routes.")
                else:
                    # check if '/' is at the end of `path`
                    if directory[-1] != '/':
                        directory += '/'

                    # combine path and directory
                    combined_path = path + directory

                    # also check if in the STATIC_PATHS
                    for static_path in self.STATIC_PATHS:
                        if static_path['path'] == combined_path:
                            raise Exception("Static route (directory) conflicts with other routes.")

                    # add to STATIC_PATHS
                    self.STATIC_PATHS.append({
                        'path': path + directory,
                        'is_dir': True,
                    })
        else:
            raise Exception("Static route is not an instance of StaticFiles. "
                            "Please use framework.static_files.StaticFiles."
                            "We are not supporting other static file classes at the moment.")


    def add_route(self, method, path, func):
        """
        Add route to router.
        :param method:
        :param path:
        :param func:
        :return:
        """
        if method == 'GET':
            self.GET_PATHS[path] = func
        elif method == 'POST':
            self.POST_PATHS[path] = func
        elif method == 'PATCH':
            self.PATCH_PATHS[path] = func
        elif method == 'PUT':
            self.PUT_PATHS[path] = func
        elif method == 'DELETE':
            self.DELETE_PATHS[path] = func

    def get(self, path):
        """
        Decorator for registering GET routes.
        :param path:
        :return:
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.GET_PATHS[path] = func
            return wrapper

        return decorator

    def post(self, path):
        """
        Decorator for registering POST routes.
        :param path:
        :return:
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.POST_PATHS[path] = wrapper
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def patch(self, path):
        """
        Decorator for registering PATCH routes.
        :param path:
        :return:
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.PATCH_PATHS[path] = wrapper
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def delete(self, path):
        """
        Decorator for registering DELETE routes.
        :param path:
        :return:
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.DELETE_PATHS[path] = wrapper
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def serve_static_files(self):
        """
        Returns all static files. (finds all files in STATIC_PATHS)
        :return:
        """

        # check if path exists in STATIC_PATHS's 'path' key
        files_path = []
        for static_path in self.STATIC_PATHS:
            if static_path['is_dir']:
                # recursively add all files in directory
                for root, dirs, files in os.walk(static_path['path']):
                    for file in files:
                        # absolute system as full path in the system
                        path = os.path.join(root, file)

                        # remove '.' from path
                        path = path.replace('./', '')

                        files_path.append(path)
            else:
                # absolute path of file in the system
                files_path.append(static_path['path'])

        # prepare for serving static files
        for path in files_path:
            with open(path, 'rb') as f:
                # read file as binary
                data = f.read()

                # remove b and ' from data
                self.SERVED_STATIC_PATHS[path] = data


    def process(self):
        # all routes are registered to self.PATHS
        print(self.GET_PATHS.items())
        for path, func in self.GET_PATHS.items():
            func()

    def routes(self):
        """
        Returns all registered routes.
        :return:
        """
        return self.GET_PATHS, self.POST_PATHS, self.PATCH_PATHS, self.DELETE_PATHS

    def static_path_exists(self, path):
        """
        Check if path exists in registered static routes.
        :param path:
        :return:
        """
        if path in self.SERVED_STATIC_PATHS:
            return True, self.SERVED_STATIC_PATHS[path]
        else:
            return False, None

    def exist(self, path, method):
        """
        Check if path exists in registered routes.
        :param path:
        :param method:
        :return:
        """
        if method == 'GET':
            if path in self.GET_PATHS:
                return True, self.GET_PATHS[path]
            else:
                return False, None
        elif method == 'POST':
            if path in self.POST_PATHS:
                return True, self.POST_PATHS[path]
            else:
                return False, None
        elif method == 'PATCH':
            if path in self.PATCH_PATHS:
                return True, self.PATCH_PATHS[path]
            else:
                return False, None
        elif method == 'DELETE':
            if path in self.DELETE_PATHS:
                return True, self.DELETE_PATHS[path]
            else:
                return False, None
        else:
            return False, None
