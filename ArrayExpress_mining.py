import requests

class ArrayExpress_mining:

    def __init__(self):
        self.keywords = []
        self.criteria = {}
        self.base_exp = "https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments"
        self.base_prot = "https://www.ebi.ac.uk/arrayexpress/xml/v3/protocols"
        self.base_file = "https://www.ebi.ac.uk/arrayexpress/xml/v3/files"
        self.metadata_exp_xml = None
        self.metadata_prot_xml = None
        self.metadata_file_xml = None

    def choose_type(self,type):
        if type == "xml":
            self.base_exp = "https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments"
            self.base_prot = "https://www.ebi.ac.uk/arrayexpress/xml/v3/protocols"
            self.base_file = "https://www.ebi.ac.uk/arrayexpress/xml/v3/files"
        elif type == "json":
            self.base_exp = "https://www.ebi.ac.uk/arrayexpress/json/v3/experiments"
            self.base_prot = "https://www.ebi.ac.uk/arrayexpress/json/v3/protocols"
            self.base_file = "https://www.ebi.ac.uk/arrayexpress/json/v3/files"
        else:
            print("Type of file not available")


    def insert_keywords(self,keywords):
        self.keywords = keywords

    def insert_criteria(self,dic):
        self.criteria = dic

    def metadata_exp(self):
        if self.keywords != [] and self.criteria !={} :
            string = self.base_exp + "?keywords=" + ("+").join(self.keywords)
            for key in self.criteria.keys():
                string += "&" + key + "=" + self.criteria[key]

        elif self.criteria != {}:
            criteria_list = []
            for key in self.criteria:
                criteria_list.append(key)
            first = criteria_list[0]
            string = self.base_exp + "?" + first + "=" + self.criteria[first]
            for i in range(1,len(criteria_list)):
                string += "&" + criteria_list[i] + "=" + self.criteria[criteria_list[i]]
        else:
            string = self.base_exp + "?keywords=" + ("+").join(self.keywords)

        print(string)
        self.metadata_exp_xml = requests.get(string)

    def get_metadata_exp_xml(self):
        if self.metadata_exp_xml != None:
            return self.metadata_exp_xml
        else:
            print("That xml file doesn't exist")

    def metadata_file(self):
        if self.keywords != [] and self.criteria !={} :
            string = self.base_file+ "?keywords=" + ("+").join(self.keywords)
            for key in self.criteria.keys():
                string += "&" + key + "=" + self.criteria[key]

        elif self.criteria != {}:
            criteria_list = []
            for key in self.criteria:
                criteria_list.append(key)
            first = criteria_list[0]
            string = self.base_file + "?" + first + "=" + self.criteria[first]
            for i in range(1,len(criteria_list)):
                string += "&" + criteria_list[i] + "=" + self.criteria[criteria_list[i]]
        else:
            string = self.base_file + "?keywords=" + ("+").join(self.keywords)

        print(string)
        self.metadata_file_xml = requests.get(string)

    def get_metadata_file_xml(self):
        if self.metadata_file_xml != None:
            return self.metadata_file_xml
        else:
            print("That xml file doesn't exist")

    def metadata_prot(self):
        if self.keywords != [] and self.criteria !={} :
            string = self.base_prot+ "?keywords=" + ("+").join(self.keywords)
            for key in self.criteria.keys():
                string += "&" + key + "=" + self.criteria[key]

        elif self.criteria != {}:
            criteria_list = []
            for key in self.criteria:
                criteria_list.append(key)
            first = criteria_list[0]
            string = self.base_prot + "?" + first + "=" + self.criteria[first]
            for i in range(1,len(criteria_list)):
                string += "&" + criteria_list[i] + "=" + self.criteria[criteria_list[i]]
        else:
            string = self.base_prot + "?keywords=" + ("+").join(self.keywords)

        print(string)
        self.metadata_prot_xml = requests.get(string)

    def get_metadata_prot_xml(self):
        if self.metadata_prot_xml != None:
            return self.metadata_prot_xml
        else:
            print("That xml file doesn't exist")




if __name__=="__main__":
    x = ArrayExpress_mining()
    cenas = ["fibroblasts","cancer"]
    x.insert_keywords(cenas)
    dic = {"species" : "mus%20musculus", "sa" : "fibroblasts"}
    x.insert_criteria(dic)
    x.choose_type("json")
    x.metadata_prot()
    print(x.get_metadata_prot_xml())


