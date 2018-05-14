from Link_Generator import Link_Generator
from File_Requester import File_Requester

class Experiments:


    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v













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