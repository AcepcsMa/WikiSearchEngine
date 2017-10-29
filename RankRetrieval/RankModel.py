__author__ = "Haoxiang Ma"

from VectorGenerator import *
from VectorUtil import *

class RankModel:

    def __init__(self, documents, numDoc, docFreqDict):
        self.documents = documents
        self.numDoc = numDoc
        self.docFreqDict = docFreqDict
        self.vectorGenerator = VectorGenerator(docFreqDict, numDoc)
        self.vectorUtil = VectorUtil()

    def setIndexFolder(self, indexFolderName):

        indexFolderName = indexFolderName+"/" if not indexFolderName.endswith("/") else indexFolderName
        self.indexFolder = indexFolderName

    # clean the original data
    def clean(self, content):
        content = re.sub("<.+?>", "", content)
        content = re.sub("'", "", content)
        content = re.sub("\.", "", content)
        content = re.sub("\n", "", content)
        content = re.sub("\t", "", content)
        terms = content.split(" ")
        return content, terms

    def receiveQuery(self, query):

        rankResult = dict()
        cleanQuery, cleanQueryTerms = self.clean(query)

        for documentID in self.documents.keys():
            documentName = self.documents[documentID]["docName"]
            docContent = open(self.indexFolder+documentName).read()
            cleanContent, cleanTerms = self.clean(docContent)
            bagOfWords = list()
            bagOfWords.extend(cleanTerms)
            bagOfWords.extend(cleanQueryTerms)

            vecQuery = self.vectorGenerator.genTFIDFVector("QUERY", query, bagOfWords)
            vecDocument = self.vectorGenerator.genTFIDFVector("DOCUMENT", cleanContent, bagOfWords)
            cosSimilarity = self.vectorUtil.cosineSimilarity(vecQuery, vecDocument)
            rankResult[documentID] = cosSimilarity

        print (rankResult)

