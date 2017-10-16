__author__ = "Haoxiang Ma"

import re
import os

class DataTransformer:

    def __init__(self, documentList, workDir):
        self.termMap = dict()
        self.documentList = documentList
        self.numDocuments = len(documentList)
        self.workDir = workDir

    # data transformation
    def transform(self):
        fileSizeSum = 0
        tokenSum = 0
        for each in self.documentList:
            docID = each[0]
            content = each[1]
            fileSize = os.path.getsize(self.workDir + each[2])
            fileSizeSum += fileSize

            # clean the content
            content = re.sub("<.+?>","",content)
            content = re.sub("'", "", content)
            content = re.sub("\.", "", content)
            content = re.sub("\n", "", content)
            terms = content.split(" ")
            uniqueTerms = list(set(terms))  # get unique terms
            uniqueTerms = [uniqueTerm for uniqueTerm in uniqueTerms if len(uniqueTerm) > 0]
            tokenSum += len(terms)
            for term in uniqueTerms:
                try:
                    self.termMap[term].append({"docID":docID,"frequency":content.count(term)/float(len(terms))})
                except:
                    self.termMap[term] = list()
                    self.termMap[term].append({"docID":docID,"frequency":content.count(term)/float(len(terms))})

        uniqueTokenSum = len(self.termMap.keys())
        with open("stats.txt", "w") as statFile:
            statFile.write("Total size of all input files:" + str(fileSizeSum))
            statFile.write("\nTotal number of tokens:" + str(tokenSum))
            statFile.write("\nTotal number of unique tokens:" + str(uniqueTokenSum))

    # get all the terms
    def getTerms(self):
        return list(self.termMap.keys())

    # get documents which contain the specific term
    def getDocumentsWithTerm(self, term):
        if(term in self.termMap.keys()):
            return list(self.termMap[term])
        else:
            return []

    # get number of documents
    def getNumDocuments(self):
        return self.numDocuments

    # get documents
    def getDocumentList(self):
        return self.documentList
