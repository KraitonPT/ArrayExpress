from json import JSONDecoder
from Link_Generator import Link_Generator
from File_Requester import File_Requester


class MetaData:

    def __init__(self, json,url):
        self.json = json
        self.url = url

    def decode_json(self):
        decoder = JSONDecoder()
        self.decoded = decoder.decode(self.json)

    def get_decoded(self):
        return self.decoded


















if __name__=="__main__":
    x = Link_Generator("json")
    cenas = ["fibroblasts", "cancer"]
    x.insert_keywords(cenas)
    dic = {"species": "mus%20musculus", "sa": "fibroblasts"}
    x.insert_criteria(dic)
    x.url_generator("experiments")
    request = File_Requester(x.get_url())
    print(request.get_url())
    request.do_request()
    request.get_request()
    request.do_content()
    print(request.get_content())
    decoder = MetaData(request.get_content(),request.get_url())
    decoder.decode_json()
    print(decoder.get_decoded())
