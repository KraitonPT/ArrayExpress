from Link_Generator import Link_Generator
from File_Requester import File_Requester
from File import File
from MetaData import MetaData
import zipfile
import pandas as pd
import os
from os.path import isfile, join
from io import StringIO

class Experiment:

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.df = {}


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

    def create_files(self):
        self.files = []
        self.do_files_url()
        self.json_files_requester()
        self.json_files_decoder()
        for file in self.decoded_json_files["files"]["experiment"]["file"]:
            self.files.append(File(file))

    def download_all_files(self,path):
        if self.files:
            for file in self.files:
                file.download_file(path)

    def do_idf_file(self,path):
        for file in self.files:
            if file.extension != "zip" and file.kind == "idf":
                file.download_file(path)
                fpath = os.path.join(*[path,file.location])
                with open(fpath, 'r') as f:
                    strio = StringIO(f.read())
                df = pd.read_csv(filepath_or_buffer=strio, encoding='utf-8', sep="\t")
                self.df[file.kind] = df

    def do_sdrf_file(self, path):
        for file in self.files:
            if file.extension != "zip" and file.kind == "sdrf":
                file.download_file(path)
                fpath = os.path.join(*[path, file.location])
                with open(fpath, 'r') as f:
                    strio = StringIO(f.read())
                df = pd.read_csv(filepath_or_buffer=strio, encoding='utf-8', sep="\t")
                self.df[file.kind] = df

    def do_processed_file(self,path):
        self.df["processed"] = []
        for file in self.files:
            if file.extension == "zip" and "processed" in file.location:
                file.download_file(path)
                fpath = os.path.join(*[path,file.location])
                zpath = os.path.join(*[path, "processed"])
                zip_ref = zipfile.ZipFile(fpath, 'r')
                zip_ref.extractall(zpath)
                zip_ref.close()
                onlyfiles = [f for f in os.listdir(zpath) if isfile(join(zpath, f))]
                for file in onlyfiles:
                    tpath = os.path.join(*[zpath, file])
                    with open(tpath, 'r') as f:
                        strio = StringIO(f.read())
                    df = pd.read_csv(filepath_or_buffer=strio, encoding='utf-8', sep="\t")
                    self.df["processed"].append(df)


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
    exp = Experiment(decoder.get_decoded()["experiments"]["experiment"][1])
    print(exp.__dict__)
    print(exp.accession)
    #exp.do_files_url()
    #print(exp.get_files_url())
    #exp.json_files_requester()
    #print(exp.get_json_files_request())
    #exp.json_files_decoder()
    #print(exp.get_decoded_json_files())
    exp.create_files()
    print(exp.files)
    #exp.download_all_files("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.files_url)
    exp.do_idf_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.df["idf"])
    exp.do_sdrf_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.df["sdrf"])
    exp.do_processed_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.df["processed"][0])


