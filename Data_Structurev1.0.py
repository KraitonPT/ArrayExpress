from Link_Generator import Link_Generator
from File_Requester import File_Requester
from MetaData import MetaData
from Experiments import Experiments

class DataStructure:

    def __init__(self,json):
        self.json = json
        self.__n_exps = len(self.json["experiments"]["experiment"])


    def create_experiments(self,n=None):
        n = self.__n_exps if n is None else n
        self.experiments = []
        for i in range(n):
            dic = self.json["experiments"]["experiment"][i]
            x = Experiments(dic)
            self.experiments.append(x)

    def get_experiments(self):
        return self.experiments


