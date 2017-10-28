__author__ = "Haoxiang Ma"

import re
import math

class VectorGenerator:

    QUERY = "QUERY"
    DOCUMENT = "DOCUMENT"

    def __init__(self, docFreq, numDoc):
        self.docFreq = docFreq
        self.numDoc = numDoc

    def genTFIDFVector(self, dataType, data, bagOfWords):
        cleanData, cleanTerms = self.clean(data)
        vector = list()

        if(dataType == self.QUERY):

            for word in bagOfWords:
                tfRaw = cleanData.count(word)
                try:
                    tfWeighted = 1 + math.log10(tfRaw)
                except:
                    tfWeighted = 0

                df = self.docFreq[word]
                try:
                    idf = math.log10(self.numDoc/df)
                except:
                    idf = 0
                valTFIDF = tfWeighted * idf
                vector.append(valTFIDF)

        elif(dataType == self.DOCUMENT):
            pass
        
        return self.normalized(vector)

    def clean(self, content):
        content = re.sub("<.+?>", "", content)
        content = re.sub("'", "", content)
        content = re.sub("\.", "", content)
        content = re.sub("\n", "", content)
        content = re.sub("\t", "", content)
        terms = content.split(" ")
        return content, terms

    def normalized(self, vector):
        l2Norm = 0
        for val in vector:
            l2Norm += val*val
        l2Norm = math.sqrt(l2Norm)
        normalizedVector = [val/l2Norm for val in vector]
        return normalizedVector