__author__ = "Haoxiang Ma"

import json
import DataTransformer

class IndexCreator:

    def __init__(self, dataTransformer):
        self.dataTransformer = dataTransformer
        self.terms = dataTransformer.getTerms()
        self.numTerms = len(self.terms)
        self.numDocuments = dataTransformer.getNumDocuments()

    def createTermIDFile(self):
        termIDDict = dict()
        for termID, term in zip(range(1,self.numTerms+1), self.terms):
            #termIDDict[termID] = list()
            documents = self.dataTransformer.getDocumentsWithTerm(term)
            #for document in documents:
            item = {"term":term, "docFreq":len(documents)/float(self.numDocuments)}
            termIDDict[termID] = item

        with open("TermIDFile.txt", "w") as termIDFile:
            termIDFile.write(json.dumps(termIDDict))

    def createDocumentIDFile(self):
        documentIDDict = dict()
        documentList = self.dataTransformer.getDocumentList()
        for each in documentList:
            docID = each[0]
            docContent = each[1]
            docName = each[2]
            documentIDDict[docID] = dict()
            documentIDDict[docID]["docName"] = docName
            documentIDDict[docID]["docLength"] = len(docContent)

        with open("DocumentIDFile.txt", "w") as documentIDFile:
            documentIDFile.write(json.dumps(documentIDDict))

    def createInvertedIndex(self):
        invertedIndexDict = {}
        for termID, term in zip(range(1, self.numTerms + 1), self.terms):
            invertedIndexDict[termID] = list()
            documents = self.dataTransformer.getDocumentsWithTerm(term)
            for each in documents:
                invertedIndexDict[termID].append(each)

        with open("InvertedIndex.txt", "w") as invertedIndexFile:
            invertedIndexFile.write(json.dumps(invertedIndexDict))


if __name__ == "__main__":
    documentList = list()
    for i in range(1, 21):
        with open("/Users/marco/Code/Python_code/InfoCrawler/files/{}.txt".format(i)) as document:
            documentList.append((i, document.read(), "{}.txt".format(i)))

    d = DataTransformer.DataTransformer(documentList)
    d.transform()

    creator = IndexCreator(d)
    creator.createTermIDFile()
    creator.createDocumentIDFile()
    creator.createInvertedIndex()