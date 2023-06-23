import os


class StaticFiles:
    def __init__(self):
        self.static_dir = {}
        self.static_files = {}


    def add_static_dir(self, path='', directory=''):
        """
        Add static route.
        :param path:
        :param directory:
        :return:
        """
        # check if `directory` exists and is a directory
        if not os.path.isdir(directory):
            # TODO: Maybe instead of raising an exception, just log it?
            raise Exception("Directory does not exist.")

        # check if '/' is at the end of `path`
        if path != '':
            if path[-1] != '/':
                path += '/'

        self.static_dir[path] = directory


    def add_static_file(self, path='', file=''):
        """
        Add static file.
        :param path:
        :param file:
        :return:
        """
        # check if `path` is empty, means current directory
        if path == '':
            path = '/'

        # check if '/' is at the end of `path`
        if path[-1] != '/':
            path += '/'

        # check if `file` exists and is a file
        if not os.path.isfile(path + file):
            # TODO: Maybe instead of raising an exception, just log it?
            raise Exception("File does not exist.")

        self.static_files[path] = file

    def get_static_files(self):
        """
        Get static files.
        :return:
        """
        return self.static_files

    def get_static_dirs(self):
        """
        Get static directory.
        :return:
        """
        return self.static_dir

