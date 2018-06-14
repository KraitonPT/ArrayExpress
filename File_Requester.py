import requests
from Link_Generator import Link_Generator

class File_Requester:

    def __init__(self,url):
        self.url = url

    def get_url(self):               # Returns the stores URL
        return self.url

    def change_url(self,new_url):       # Sets a new URL
        self.url = new_url

    def do_request(self):              # Does the request using the stored URL
        self.request = requests.get(self.url)

    def get_request(self):                   # Returns the request
        if self.request:
            return self.request
        else:
            print("There isn't any request done")

    def do_content(self):          # Stores the content of the request
        self.content = self.request.text

    def get_content(self):            # Returns the content of the request
        return self.content

