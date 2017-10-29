__author__ = "Haoxiang Ma"
import json

from VectorGenerator import *
from VectorUtil import *
from RankModel import *

if __name__ == "__main__":
    TermIDFile = open("TermIDFile.txt", "r")
    termDict = json.loads(TermIDFile.read())
    TermIDFile.close()

    DocumentIDFile = open("DocumentIDFile.txt", "r")
    documentDict = json.loads(DocumentIDFile.read())
    DocumentIDFile.close()
    numDoc = len(documentDict.keys())

    terms = list()
    docFreq = dict()
    for key in termDict.keys():
        terms.append(termDict[key]["term"])
        docFreq[termDict[key]["term"]] = termDict[key]["docFreq"]

    '''vectorGenerator = VectorGenerator(docFreq, numDoc)
    vectorUtil = VectorUtil()

    query = "Who is Gerard"
    queryWords = query.split(" ")
    bagOfWords = list()
    bagOfWords.extend(queryWords)

    docFile = open("../InfoCrawler/files/1.txt")
    content = docFile.read()
    content = re.sub("<.+?>", "", content)
    content = re.sub("'", "", content)
    content = re.sub("\.", "", content)
    content = re.sub("\n", "", content)
    content = re.sub("\t", "", content)
    terms = content.split(" ")
    bagOfWords.extend(terms)

    vecQuery = vectorGenerator.genTFIDFVector(VectorGenerator.QUERY, query, bagOfWords)
    vecDocument = vectorGenerator.genTFIDFVector(VectorGenerator.DOCUMENT, content, bagOfWords)
    print (len(vecQuery) == len(vecDocument))

    print (vectorUtil.cosineSimilarity(vecQuery, vecDocument))

    #print (vectorGenerator.genTFIDFVector("QUERY", "hello world"))'''

    myModel = RankModel(documentDict, numDoc, docFreq)
    myModel.setIndexFolder("../InfoCrawler/files")
    myModel.receiveQuery("Who is Gerard")

