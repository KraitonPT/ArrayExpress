class Link_Generator:

    def __init__(self,format,keywords = [],criteria = {}):
        self.keywords = keywords
        self.criteria = criteria
        self.choose_format(format)

    def choose_format(self,format):
        if format == "xml" or format == "json":
            self.base_exp = "https://www.ebi.ac.uk/arrayexpress/" + format + "/v3/experiments"
            self.base_prot = "https://www.ebi.ac.uk/arrayexpress/" + format + "/v3/protocols"
            self.base_file = "https://www.ebi.ac.uk/arrayexpress/" + format + "/v3/files"
        else:
            print("Selected file format isn't available")

    def insert_keywords(self,keywords):
        self.keywords = keywords

    def insert_criteria(self,dic):
        self.criteria = dic

    def url_generator(self,type):
        dic = {"experiments":self.base_exp,"protocols":self.base_prot,"files":self.base_file}

        if type not in dic:
            print("Type of file not available")
        else:
            file_type = dic[type]
            if self.keywords != [] and self.criteria !={}:
                string = file_type + "?keywords=" + ("+").join(self.keywords)
                for key in self.criteria.keys():
                    string += "&" + key + "=" + self.criteria[key]

            elif self.criteria != {}:
                criteria_list = []
                for key in self.criteria:
                    criteria_list.append(key)
                first = criteria_list[0]
                string = file_type + "?" + first + "=" + self.criteria[first]
                for i in range(1,len(criteria_list)):
                    string += "&" + criteria_list[i] + "=" + self.criteria[criteria_list[i]]
            else:
                string = file_type + "?keywords=" + ("+").join(self.keywords)

            self.url = string

    def get_url(self):
        return self.url




