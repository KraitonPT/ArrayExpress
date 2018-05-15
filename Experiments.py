from Link_Generator import Link_Generator
from File_Requester import File_Requester
from MetaData import MetaData

class Experiments:

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def do_files_url(self):
        dic = {"accession": self.accession}
        link_generator = Link_Generator("json",[],dic)
        link_generator.url_generator("files")
        self.files_url = link_generator.get_url()

    def get_files_url(self):
        return self.files_url

    def json_files_requester(self):
        requester = File_Requester(self.get_files_url())
        requester.do_request()
        requester.do_content()
        self.json_files = requester.get_content()

    def get_json_files_request(self):
        return self.json_files

    def json_files_decoder(self):
        meta = MetaData(self.get_json_files_request(),self.get_files_url())
        meta.decode_json()
        self.decoded_json_files = meta.get_decoded()

    def get_decoded_json_files(self):
        return self.decoded_json_files

    def do_protocols_url(self):
        dic = {"experiment": self.accession}
        link_generator = Link_Generator("json", [], dic)
        link_generator.url_generator("protocols")
        self.protocols_url = link_generator.get_url()


    def get_protocols_url(self):
        return self.protocols_url

    def json_protocols_requester(self):
        requester = File_Requester(self.get_files_url())
        requester.do_request()
        requester.do_content()
        self.json_protocols = requester.get_content()

    def json_files_requester(self):
        requester = File_Requester(self.get_files_url())
        requester.do_request()
        requester.do_content()
        self.json_files = requester.get_content()

    def get_json_protocols_request(self):
        return self.json_protocols

    def json_protocols_decoder(self):
        meta = MetaData(self.get_json_protocols_request(), self.get_protocols_url())
        meta.decode_json()
        self.decoded_json_protocols = meta.get_decoded()

    def get_decoded_json_protocols(self):
        return self.decoded_json_protocols()

if __name__ == "__main__":
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
    decoder = MetaData(request.get_content(), request.get_url())
    decoder.decode_json()
    print(decoder.get_decoded())
    exp = Experiments(decoder.get_decoded()["experiments"]["experiment"][0])
    print(exp.__dict__)
    print(exp.accession)
    exp.do_files_url()
    print(exp.get_files_url())
    exp.json_files_requester()
    print(exp.get_json_files_request())
    exp.json_files_decoder()
    print(exp.get_decoded_json_files())

