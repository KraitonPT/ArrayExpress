from Link_Generator import Link_Generator
from File_Requester import File_Requester
from MetaData import MetaData
import requests
import os


class File:

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def download_file(self,path):
        req = requests.get(self.url)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(os.path.join(path,self.location),"wb") as f:
            f.write(req.content)



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
    file = File(exp.get_decoded_json_files()["files"]["experiment"]["file"][1])
    print(file.__dict__)
    file.download_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
