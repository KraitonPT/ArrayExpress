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


if __name__=="__main__":
    x = Link_Generator("xml")
    cenas = ["fibroblasts", "cancer"]
    x.insert_keywords(cenas)
    dic = {"species": "mus%20musculus", "sa": "fibroblasts"}
    x.insert_criteria(dic)
    x.url_generator("experiments")
    request = File_Requester(x.get_url())
    print(request.get_url())
    request.do_request()
    print(request.get_request())
