from Link_Generator import Link_Generator
from File_Requester import File_Requester
from File import File
from MetaData import MetaData
import zipfile
import pandas as pd
import random
import string
import shutil
import os
from os.path import isfile, join
from io import StringIO

class Experiment:

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.df = {}
        self.create_files()
        self.len_proccessed_one = False

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
                    lines = strio.readlines()
                    splt_lines = []
                    for line in lines:
                        nw_line = line.split("\t")
                        if len(nw_line) > 1:
                            splt_lines.append((nw_line[0].strip(),nw_line[1].strip()))
                self.df[file.kind] = {}
                for x,y in splt_lines:
                    self.df[file.kind][x] = y


    def get_idf_file(self):
        if "idf" in self.df:
            return self.df["idf"]
        else:
            return "There isn't any idf file stored"

    def do_sdrf_file(self, path):
        for file in self.files:
            if file.extension != "zip" and file.kind == "sdrf":
                file.download_file(path)
                fpath = os.path.join(*[path, file.location])
                with open(fpath, 'r') as f:
                    strio = StringIO(f.read())
                df = pd.read_csv(filepath_or_buffer=strio, encoding='utf-8', sep="\t")
                self.df[file.kind] = df

    def get_sdrf_file(self):
        if "sdrf" in self.df:
            return self.df["sdrf"]
        else:
            return "There isn't any sdrf file stored"

    def get_metada_sdrf(self,files):
        if "sdrf" in self.df and "concat_processed" in self.df:
            col_index = self.find_samples().tolist()[0]
            sdrf_df = self.df["sdrf"]
            metadata = sdrf_df.loc[sdrf_df[col_index].isin(files),:]
            return metadata
        else:
            return "sdrf or concatenated files don't exist"

    def find_samples(self):
        if "concat_processed" in self.df:
            sdrf = self.df["sdrf"]
            concat_columns = self.df["concat_processed"].columns
            counts = sdrf.apply(lambda x: sum(x.isin(concat_columns)))
            sample_col = counts[counts==max(counts)]
            return sample_col.index


    def do_processed_file(self,path):
        if "sdrf" not in self.df:
            self.do_sdrf_file(path)
        self.df["processed"] = []
        for file in self.files:
            if file.extension == "zip" and "processed.1" in file.location:
                file.download_file(path)
                fpath = os.path.join(*[path,file.location])
                random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                zpath = os.path.join(*[path,random_string])
                dir_path = zpath
                zip_ref = zipfile.ZipFile(fpath, 'r')
                zip_ref.extractall(zpath)
                zip_ref.close()
                onlyfiles = [f for f in os.listdir(zpath) if isfile(join(zpath, f))]
                if len(onlyfiles) <= 1:
                    self.len_proccessed_one = True
                for file in onlyfiles:
                    tpath = os.path.join(*[zpath, file])
                    # with open(tpath, 'r') as f:
                    #     strio = StringIO()
                    #     for line in f.readlines():
                    #         strio.write(line + "\n")
                    df = pd.read_csv(filepath_or_buffer=open(tpath,"r"), sep="\t")
                    self.df["processed"].append((file,df))
                shutil.rmtree(dir_path)

    def get_processed_file(self):
        if "processed" in self.df:
            return self.df["processed"]
        else:
            return "There isn't any processed file stored"

    def process_df(self,index_col,index_val):
        if "processed" in self.df:
            df_list = list(zip(*self.get_processed_file()))
            concat_processed_raw = [df.set_index(index_col, drop=True) for df in df_list[1]]         # alterado
            value_df = [df[index_val] for df in concat_processed_raw]     # alterado
            df_final = pd.concat(value_df, axis=1)
            df_final.columns = df_list[0]
            return df_final
        else:
            return "There isn't any processed files stored"

    def get_col_names(self):
        df_list = self.df["processed"]
        # ind = df_list[0][1].columns[:-1].tolist()
        # val = df_list[0][1].columns[-1]
        ind = df_list[0][1].columns[0]
        val_bol = df_list[0][1].columns == "VALUE"
        val = df_list[0][1].columns[val_bol]
        return ind,val

    def concat_processed(self):
        if self.len_proccessed_one:
            self.df["concat_processed"] = self.df["processed"][0][1]
            column = self.df["concat_processed"].columns[0]
            self.df["concat_processed"] = self.df["concat_processed"].set_index(column,drop = True)
        else:
            if self.df["processed"] != []:
                index_col,index_val= self.get_col_names()          #alterado
                df_final = self.process_df(index_col,index_val)           #alterado
                self.df["concat_processed"] = df_final


    def get_concat_processed(self):
        if "concat_processed" in self.df:
            return self.df["concat_processed"]
        else:
            self.concat_processed()
            if "concat_processed" in self.df:
                return self.df["concat_processed"]
            else:
                return "There isn't any processed files"

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

