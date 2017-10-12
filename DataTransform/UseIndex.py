__author__ = "Haoxiang Ma"

import json
import sys

class QueryHandler:

    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.dataPath = self.dataPath+"/" if not self.dataPath.endswith("/") else self.dataPath

    def getTermID(self, term):
        with open(self.dataPath+"TermIDFile.txt", "r") as termIDFile:
            termDict = json.loads(termIDFile.read())
            for termID in termDict.keys():
                if(termDict[termID]["term"] == term):
                    return termID
        return -1

    def getInvertedList(self, termID):
        termID = str(termID)
        with open(self.dataPath+"InvertedIndex.txt", "r") as invertedIndexFile:
            invertedIndexDict = json.loads(invertedIndexFile.read())
            return invertedIndexDict[termID]

    def getIDNInvertedList(self, term):
        termID = self.getTermID(term)
        if(termID == -1):
            return "Can not find this term!"
        invertedList = self.getInvertedList(termID)
        documentIDs = []
        for each in invertedList:
            documentIDs.append(each["docID"])
        return documentIDs

    def getDocumentName(self, documentID):
        documentID = str(documentID)
        with open(self.dataPath+"DocumentIDFile.txt", "r") as documentIDFile:
            documentDict = json.loads(documentIDFile.read())
            return documentDict[documentID]["docName"]


if __name__ == "__main__":

    queryType = sys.argv[1] # the first argument from command line is query type
    queryTerm = sys.argv[2] # the second argument from command line is query term

    # set work dir to be current dir
    queryHandler = QueryHandler("./")

    # deal with different query type
    if(queryType == "--getTermID"):
        print(queryHandler.getTermID(queryTerm))
    elif(queryType == "--getInvertedList"):
        print(queryHandler.getInvertedList(queryTerm))
    elif(queryType == "--getDocumentIDs"):
        print(queryHandler.getIDNInvertedList(queryTerm))
    elif(queryType == "--getDocumentName"):
        print(queryHandler.getDocumentName(queryTerm))
