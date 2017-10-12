__author__ = "Haoxiang Ma"

import DataTransformer
import IndexCreator
import sys
import os

if __name__ == "__main__":

    folderName = str(sys.argv[1])
    folderName = folderName+"/" if not folderName.endswith("/") else folderName
    numFilesToProcess = int(sys.argv[2])

    fileNames = os.listdir(folderName)

    documentList = list()
    for i, fileName in zip(range(1, numFilesToProcess+1), fileNames):
        with open(folderName + fileName) as document:
            documentList.append((i, document.read(), fileName))

    d = DataTransformer.DataTransformer(documentList)
    d.transform()

    creator = IndexCreator.IndexCreator(d)
    creator.createTermIDFile()
    creator.createDocumentIDFile()
    creator.createInvertedIndex()
