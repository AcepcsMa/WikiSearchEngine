__author__ = "Haoxiang Ma"

from VectorGenerator import *
from VectorUtil import *

# class of rank model
class RankModel:

    def __init__(self, documents, numDoc, docFreqDict, topK):
        self.documents = documents
        self.numDoc = numDoc
        self.docFreqDict = docFreqDict
        self.topK = topK
        self.vectorGenerator = VectorGenerator(docFreqDict, numDoc)
        self.vectorUtil = VectorUtil()
        self.logWriter = None

    def setFileFolder(self, fileFolderName):
        fileFolderName = fileFolderName+"/" if not fileFolderName.endswith("/") else fileFolderName
        self.fileFolder = fileFolderName

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

    # deal with a query
    def dealWithQuery(self, query):

        rankResult = dict()
        contributionDict = dict()
        cleanQuery, cleanQueryTerms = self.clean(query) # transform query

        # calculate similarity between current query and each doc in documentPath
        for documentID in self.documents.keys():
            contributions = dict()
            documentName = self.documents[documentID]["docName"]
            docContent = open(self.fileFolder+documentName).read()  # read content of document
            cleanContent, cleanTerms = self.clean(docContent)   # transform the content

            # build a bag of words for current query & current document
            bagOfWords = list()
            bagOfWords.extend(cleanTerms)
            bagOfWords.extend(cleanQueryTerms)

            # generate tf-idf vector for current query and current document
            vecQuery = self.vectorGenerator.genTFIDFVector("QUERY", query, bagOfWords)
            vecDocument = self.vectorGenerator.genTFIDFVector("DOCUMENT", cleanContent, bagOfWords)

            # calculate the cosine similarity
            cosSimilarity, contributionVec = self.vectorUtil.cosineSimilarity(vecQuery, vecDocument)
            rankResult[documentID] = cosSimilarity
            for word, contribution in zip(bagOfWords, contributionVec):
                contributions[word] = contribution
            contributionDict[documentID] = contributions

        # sort the ranking result (DESC)
        rankResult = sorted(rankResult.items(), key=lambda pair:pair[1], reverse=True)

        # write log
        if(self.logWriter is None):
            raise Exception("Please set your log writer!")
        self.logWriter.write(query, cleanQueryTerms, rankResult, contributionDict)

        return cleanQueryTerms, rankResult[:self.topK]
