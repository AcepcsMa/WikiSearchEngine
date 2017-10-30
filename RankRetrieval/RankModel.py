__author__ = "Haoxiang Ma"

from VectorGenerator import *
from VectorUtil import *

class RankModel:

    def __init__(self, documents, numDoc, docFreqDict, topK):
        self.documents = documents
        self.numDoc = numDoc
        self.docFreqDict = docFreqDict
        self.topK = topK
        self.vectorGenerator = VectorGenerator(docFreqDict, numDoc)
        self.vectorUtil = VectorUtil()
        self.logWriter = None

    def setIndexFolder(self, indexFolderName):
        indexFolderName = indexFolderName+"/" if not indexFolderName.endswith("/") else indexFolderName
        self.indexFolder = indexFolderName

    def setLogWriter(self, logWriter):
        self.logWriter = logWriter

    # clean the original data
    def clean(self, content):
        content = re.sub("<.+?>", "", content)
        content = re.sub("'", "", content)
        content = re.sub("\.", "", content)
        content = re.sub("\n", "", content)
        content = re.sub("\t", "", content)
        terms = content.split(" ")
        return content, terms

    def dealWithQuery(self, query):

        rankResult = dict()
        contributionDict = dict()
        cleanQuery, cleanQueryTerms = self.clean(query)

        for documentID in self.documents.keys():
            contributions = dict()
            documentName = self.documents[documentID]["docName"]
            docContent = open(self.indexFolder+documentName).read()
            cleanContent, cleanTerms = self.clean(docContent)
            bagOfWords = list()
            bagOfWords.extend(cleanTerms)
            bagOfWords.extend(cleanQueryTerms)

            vecQuery = self.vectorGenerator.genTFIDFVector("QUERY", query, bagOfWords)
            vecDocument = self.vectorGenerator.genTFIDFVector("DOCUMENT", cleanContent, bagOfWords)
            cosSimilarity, contributionVec = self.vectorUtil.cosineSimilarity(vecQuery, vecDocument)
            rankResult[documentID] = cosSimilarity
            for word, contribution in zip(bagOfWords, contributionVec):
                contributions[word] = contribution
            contributionDict[documentID] = contributions

        rankResult = sorted(rankResult.items(), key=lambda pair:pair[1], reverse=True)
        print (rankResult)

        if(self.logWriter is None):
            raise Exception("Please set your log writer!")
        self.logWriter.write(query, cleanQueryTerms, rankResult, contributionDict)

        return cleanQueryTerms, rankResult[:self.topK]
