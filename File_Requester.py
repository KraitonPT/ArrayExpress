import requests
from Link_Generator import Link_Generator

class File_Requester:

    def __init__(self,url):
        self.url = url

    def get_url(self):
        return self.url

    def change_url(self,new_url):
        self.url = new_url

    def do_request(self):
        self.request = requests.get(self.url)

    def get_request(self):
        if self.request:
            return self.request
        else:
            print("There isn't any request done")

    def do_content(self):
        self.content = self.request.text

    def get_content(self):
        return self.content

