from json import JSONDecoder

class MetaData:

    def __init__(self, json,url):
        self.json = json
        self.url = url

    def decode_json(self):          # Decodes an encoded JSON
        decoder = JSONDecoder()
        self.decoded = decoder.decode(self.json)

    def get_decoded(self):         # Returns a decoded JSON
        return self.decoded



