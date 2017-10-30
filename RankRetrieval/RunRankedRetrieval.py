__author__ = "Haoxiang Ma"

from RankModel import *
from LogWriter import *
import sys

if __name__ == "__main__":

    # read args from command line
    indexfolderName = sys.argv[1]
    folderName = sys.argv[2]
    queryFileName = sys.argv[3]
    topK = sys.argv[4]

    # load TermIDFile
    TermIDFile = open("TermIDFile.txt", "r")
    termDict = json.loads(TermIDFile.read())
    TermIDFile.close()

    # load DocumentIDFile
    DocumentIDFile = open("DocumentIDFile.txt", "r")
    documentDict = json.loads(DocumentIDFile.read())
    DocumentIDFile.close()
    numDoc = len(documentDict.keys())

    terms = list()
    docFreq = dict()
    for key in termDict.keys():
        terms.append(termDict[key]["term"])
        docFreq[termDict[key]["term"]] = termDict[key]["docFreq"]

    # initialize log writer
    logWriter = LogWriter("./", "../InfoCrawler/files", "./")

    # set rank model
    myModel = RankModel(documentDict, numDoc, docFreq, topK)
    myModel.setIndexFolder("../InfoCrawler/files")
    myModel.setLogWriter(logWriter)

    # start to deal with queries
    queryFile = open(queryFileName, "r")
    for query in queryFile.readline():
        cleanQueryTerms, rankResult = myModel.dealWithQuery(query)
