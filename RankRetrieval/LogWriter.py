__author__ = "Haoxiang Ma"

import json
import re

# log writer
class LogWriter:

    def __init__(self, logPath, fileFolder, indexFolder):
        logPath = logPath + "/" if not logPath.endswith("/") else logPath
        fileFolder = fileFolder + "/" if not fileFolder.endswith("/") else fileFolder
        indexFolder = indexFolder + "/" if not indexFolder.endswith("/") else indexFolder
        self.logPath = logPath
        self.fileFolder = fileFolder
        self.indexFolder = indexFolder
        self.documentDict = self.loadDocumentIDFile()

    def loadDocumentIDFile(self):
        documentIDFile = open(self.indexFolder + "DocumentIDFile.txt")
        documents = json.loads(documentIDFile.read())
        documentIDFile.close()
        return documents

    # write stats to log
    def write(self, rawQuery, transformedQuery, rankResult, contributionDict):
        with open(self.logPath + "Output.txt", "a") as outputFile:

            # line1 raw query
            outputFile.write(rawQuery + "\n")

            # line2 transformed query
            outputFile.write(str(transformedQuery) + "\n")

            for result in rankResult:
                docID = result[0]
                similarity = result[1]
                contributions = contributionDict[docID]
                docName = self.documentDict[docID]["docName"]

                # line r1 documentID & documentName
                outputFile.write(str(docID) + "\t" + docName + "\n")

                # line r2 snippet
                documentFile = open(self.fileFolder + docName)
                content = documentFile.read()
                documentFile.close()
                content = re.sub("<.+?>", "", content)
                content = re.sub("\n", "", content)
                outputFile.write(content[:200] + "\n") # first 200 bytes

                # line r3 cosine similarity
                outputFile.write("Cosine Similarity:" + str(similarity) + "\n")

                # contributions of each word
                for word in contributions:
                    outputFile.write(word + ":" + str(contributions[word]) + "; ")

                # line r4 blank line
                outputFile.write("\n")

                # another two blank lines
                outputFile.write("\n")
                outputFile.write("\n")