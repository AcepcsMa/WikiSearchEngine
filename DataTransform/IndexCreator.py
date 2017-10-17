__author__ = "Haoxiang Ma"

import json
import os
import re

# class of index creator
class IndexCreator:

    def __init__(self, dataTransformer):
        self.dataTransformer = dataTransformer
        self.terms = dataTransformer.getTerms()
        self.numTerms = len(self.terms)
        self.numDocuments = dataTransformer.getNumDocuments()
        self.indexFileSizeSum = 0

    # create TermIDFile.txt
    def createTermIDFile(self):
        termIDDict = dict()
        for termID, term in zip(range(1,self.numTerms+1), self.terms):
            documents = self.dataTransformer.getDocumentsWithTerm(term)
            item = {"term":term, "docFreq":len(documents)}
            termIDDict[termID] = item

        with open("TermIDFile.txt", "w") as termIDFile:
            termIDFile.write(json.dumps(termIDDict))

        self.indexFileSizeSum += os.path.getsize("TermIDFile.txt")

    # create DocumentIDFile.txt
    def createDocumentIDFile(self):
        documentIDDict = dict()
        documentList = self.dataTransformer.getDocumentList()
        for each in documentList:
            docID = each[0]
            docContent = each[1]
            docName = each[2]
            documentIDDict[docID] = dict()
            documentIDDict[docID]["docName"] = docName
            #documentIDDict[docID]["docLength"] = len(docContent)
            documentIDDict[docID]["docLength"] = self.dataTransformer.getNumTokensOfDoc(docID)

        with open("DocumentIDFile.txt", "w") as documentIDFile:
            documentIDFile.write(json.dumps(documentIDDict))

        self.indexFileSizeSum += os.path.getsize("DocumentIDFile.txt")

    # create InvertedIndex.txt
    def createInvertedIndex(self):
        invertedIndexDict = {}
        for termID, term in zip(range(1, self.numTerms + 1), self.terms):
            invertedIndexDict[termID] = list()
            documents = self.dataTransformer.getDocumentsWithTerm(term)
            for each in documents:
                invertedIndexDict[termID].append(each)

        with open("InvertedIndex.txt", "w") as invertedIndexFile:
            invertedIndexFile.write(json.dumps(invertedIndexDict))

        self.indexFileSizeSum += os.path.getsize("InvertedIndex.txt")

        fileSizeSum = 0
        with open("stats.txt", "r") as statFile:
            fileSizeSum = re.findall("Total size of all input files\:(.+?)\n", statFile.read())[0]

        with open("stats.txt", "a+") as statFile:
            statFile.write("\nTotal size of three index files:" + str(self.indexFileSizeSum))
            ratio = float(self.indexFileSizeSum) / float(fileSizeSum)
            statFile.write("\nRatio of the index size to the total file size:" + "%.2f"%ratio)

