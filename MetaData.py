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



