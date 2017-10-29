__author__ = "Haoxiang Ma"

import re
import math

class VectorGenerator:

    QUERY = "QUERY"
    DOCUMENT = "DOCUMENT"

    def __init__(self, docFreq, numDoc):
        self.docFreq = docFreq
        self.numDoc = numDoc

    # generate tf-idf vector for query/document
    def genTFIDFVector(self, dataType, data, bagOfWords):
        cleanData, cleanTerms = self.clean(data)
        vector = list()

        for word in bagOfWords:
            tfRaw = cleanData.count(word)
            try:
                tfWeighted = 1 + math.log10(tfRaw)
            except:
                tfWeighted = 0

            # for a query, we use the actual df and idf
            if(dataType == self.QUERY):
                try:
                    df = self.docFreq[word]
                    idf = math.log10(self.numDoc/df)
                except:
                    idf = 0
                valTFIDF = tfWeighted * idf

            # for a document, we use 1 or 0 for df(idf)
            elif(dataType == self.DOCUMENT):
                try:
                    tfWeighted = 1 + math.log10(tfRaw)
                except:
                    tfWeighted = 0
                df = 1 if word in cleanData else 0
                valTFIDF = tfWeighted * df
            else:
                valTFIDF = 0

            vector.append(valTFIDF)

        # return the normalized vector
        return self.normalized(vector)

    # clean the original data
    def clean(self, content):
        content = re.sub("<.+?>", "", content)
        content = re.sub("'", "", content)
        content = re.sub("\.", "", content)
        content = re.sub("\n", "", content)
        content = re.sub("\t", "", content)
        terms = content.split(" ")
        return content, terms

    # L2 normalize
    def normalized(self, vector):
        l2Norm = 0
        for val in vector:
            l2Norm += val*val
        l2Norm = math.sqrt(l2Norm)
        normalizedVector = [val/l2Norm for val in vector]
        return normalizedVector