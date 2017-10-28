__author__ = "Haoxiang Ma"
import json

from VectorGenerator import *

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

    vectorGenerator = VectorGenerator(terms, docFreq, numDoc)
    print (vectorGenerator.genTFIDFVector("QUERY", "hello world"))

