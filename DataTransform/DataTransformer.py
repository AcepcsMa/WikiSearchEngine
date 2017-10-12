__author__ = "Haoxiang Ma"

import re

class DataTransformer:

    def __init__(self, documentList):
        self.termMap = dict()
        self.documentList = documentList
        self.numDocuments = len(documentList)

    def transform(self):
        for each in self.documentList:
            docID = each[0]
            content = each[1]
            content = re.sub("<.+?>","",content)
            content = re.sub("'", "", content)
            content = re.sub("\.", "", content)
            content = re.sub("\n", "", content)
            terms = list(set(content.split(" ")))
            #terms = [re.sub("'", "", term) for term in terms] # get rid of apostrophes
            #terms = [re.sub("\.", "", term) for term in terms] # get rid of dot
            #terms = [re.sub("\n", "", term) for term in terms]
            for term in terms:
                try:
                    self.termMap[term].append({"docID":docID,"frequency":content.count(term)/float(len(terms))})
                except:
                    self.termMap[term] = list()
                    self.termMap[term].append({"docID":docID,"frequency":content.count(term)/float(len(terms))})

    def getTerms(self):
        return list(self.termMap.keys())

    def getDocumentsWithTerm(self, term):
        if(term in self.termMap.keys()):
            return list(self.termMap[term])
        else:
            return []

    def getNumDocuments(self):
        return self.numDocuments

    def getDocumentList(self):
        return self.documentList

if __name__ == "__main__":

    documentList = list()
    for i in range(1,51):
        with open("/Users/marco/Code/Python_code/InfoCrawler/files/{}.txt".format(i)) as document:
            documentList.append((i,document.read()))

    d = DataTransformer(documentList)
    d.transform()