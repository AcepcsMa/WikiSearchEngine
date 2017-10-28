__author__ = "Haoxiang Ma"

import DataTransformer
import sys
import os

if __name__ == "__main__":

    # set parameters
    folderName = str(sys.argv[1])
    folderName = folderName + "/" if not folderName.endswith("/") else folderName
    numFilesToProcess = int(sys.argv[2])
    fileNames = os.listdir(folderName)

    # read documents from local, record documentID, content, and documentName
    documentList = list()
    for i, fileName in zip(range(1, numFilesToProcess + 1), fileNames):
        with open(folderName + fileName) as document:
            documentList.append((i, document.read(), fileName))

    # new a transformer, do the transformation
    d = DataTransformer.DataTransformer(documentList, folderName)
    d.transform()

    # print the result
    terms = d.getTerms()
    for i in range(1, len(terms)+1):
        print(i, terms[i - 1])
