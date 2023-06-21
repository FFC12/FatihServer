import functools
import threading


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

                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the class with empty dictionaries for each HTTP method.
        """
        pass

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
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.DELETE_PATHS[path] = wrapper
                return func(*args, **kwargs)

            return wrapper

        return decorator

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
