import requests
import os
from os.path import isfile, join


class File:

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def download_file(self,path):             # Downloads the file for the given path
        files_dir = [f for f in os.listdir(path) if isfile(join(path, f))]
        if self.location in files_dir:
            return None
        req = requests.get(self.url)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(os.path.join(path,self.location),"wb") as f:
            f.write(req.content)
