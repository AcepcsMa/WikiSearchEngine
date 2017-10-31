__author__ = "Haoxiang Ma"

from RankModel import *
from LogWriter import *
import sys

if __name__ == "__main__":

    # read args from command line
    indexFolderName = sys.argv[1]
    indexFolderName = indexFolderName + "/" if not indexFolderName.endswith("/") else indexFolderName
    fileFolderName = sys.argv[2]
    fileFolderName = fileFolderName + "/" if not fileFolderName.endswith("/") else fileFolderName
    queryFileName = sys.argv[3]
    topK = int(sys.argv[4])

    # load TermIDFile
    TermIDFile = open(indexFolderName + "TermIDFile.txt", "r")
    termDict = json.loads(TermIDFile.read())
    TermIDFile.close()

    # load DocumentIDFile
    DocumentIDFile = open(indexFolderName + "DocumentIDFile.txt", "r")
    documentDict = json.loads(DocumentIDFile.read())
    DocumentIDFile.close()
    numDoc = len(documentDict.keys())

    # load document frequency from index file
    terms = list()
    docFreq = dict()
    for key in termDict.keys():
        terms.append(termDict[key]["term"])
        docFreq[termDict[key]["term"]] = termDict[key]["docFreq"]

    # initialize log writer
    logWriter = LogWriter("./", fileFolderName, indexFolderName)

    # set rank model
    myModel = RankModel(documentDict, numDoc, docFreq, topK)
    myModel.setFileFolder(fileFolderName)
    myModel.setLogWriter(logWriter)

    # start to deal with queries
    queryFile = open(queryFileName, "r")
    for query in queryFile.readlines():
        query = query.strip("\n")
        print ("Dealing with query: \"" + query + "\". Please wait.")
        cleanQueryTerms, rankResult = myModel.dealWithQuery(query)
