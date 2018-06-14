from Experiments import Experiments

class DataStructure:

    def __init__(self,json):
        self.json = json
        self.__n_exps = len(self.json["experiments"]["experiment"])


    def create_experiments(self,n=None):                 # Creates a list with given number of Experiment instances from requested content
        n = self.__n_exps if n is None else n
        self.experiments = []
        for i in range(n):
            dic = self.json["experiments"]["experiment"][i]
            x = Experiments(dic)
            self.experiments.append(x)

    def get_experiments(self):               # Returns the list of Experiment instances
        return self.experiments


