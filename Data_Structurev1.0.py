from Link_Generator import Link_Generator
from File_Requester import File_Requester
from MetaData import MetaData
from Experiments import Experiments

class DataStructure:

    def __init__(self,json):
        self.json = json


    def create_experiments(self,n):
        self.experiments = []
        for i in range(n):
            dic = self.json["experiments"]["experiment"][i]
            x = Experiments(dic)
            self.experiments.append(x)

    def get_experiments(self):
        return self.experiments










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
    data = DataStructure(decoder.get_decoded())
    data.create_experiments(4)
    print(data.get_experiments())
    print(data.get_experiments()[3].__dict__)

