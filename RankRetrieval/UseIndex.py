__author__ = "Haoxiang Ma"

import json
import sys

# class of query handler
class QueryHandler:

    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.dataPath = self.dataPath+"/" if not self.dataPath.endswith("/") else self.dataPath

    # get termID by term
    def getTermID(self, term):
        with open(self.dataPath+"TermIDFile.txt", "r") as termIDFile:
            termDict = json.loads(termIDFile.read())
            for termID in termDict.keys():
                if(termDict[termID]["term"] == term):
                    return termID
        return -1

    # get inverted list by termID
    def getInvertedList(self, termID):
        termID = str(termID)
        with open(self.dataPath+"InvertedIndex.txt", "r") as invertedIndexFile:
            invertedIndexDict = json.loads(invertedIndexFile.read())
            return invertedIndexDict[termID]

    # get documentID by term
    def getIDNInvertedList(self, term):
        termID = self.getTermID(term)
        if(termID == -1):
            return "Can not find this term!"
        invertedList = self.getInvertedList(termID)
        documentIDs = []
        for each in invertedList:
            documentIDs.append(each["docID"])
        return documentIDs

    # get document name by documentID
    def getDocumentName(self, documentID):
        documentID = str(documentID)
        with open(self.dataPath+"DocumentIDFile.txt", "r") as documentIDFile:
            documentDict = json.loads(documentIDFile.read())
            return documentDict[documentID]["docName"]

    # search by a complete query
    def search(self, query):
        terms = query.split(" ")
        docIDs = set()
        for term in terms:
            invertedList = set(self.getIDNInvertedList(term))
            docIDs = docIDs.union(invertedList)
        result = [self.getDocumentName(docID) for docID in docIDs]
        return result

if __name__ == "__main__":

    queryType = sys.argv[1] # the first argument from command line is query type
    queryTerm = sys.argv[2] # the second argument from command line is query term

    # set work dir to be current dir
    queryHandler = QueryHandler("./")

    # get termID by term
    if(queryType == "--getTermID"):
        print(queryHandler.getTermID(queryTerm))

    # get inverted list by termID
    elif(queryType == "--getInvertedList"):
        print(queryHandler.getInvertedList(queryTerm))

    # get documentID by term
    elif(queryType == "--getDocumentIDs"):
        print(queryHandler.getIDNInvertedList(queryTerm))

    # get document name by documentID
    elif(queryType == "--getDocumentName"):
        print(queryHandler.getDocumentName(queryTerm))

    # search by a complete query
    elif(queryType == "--search"):
        query = " ".join(sys.argv[2:])
        print ("\nSearch Result:")
        print (queryHandler.search(query),"\n")