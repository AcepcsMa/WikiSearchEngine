__author__ = "Haoxiang Ma"

class ScoreTool(object):

    def __init__(self):
        self.query = None   # query string
        self.poolSize = None    # pool size
        self.poolSizeWithoutDup = None  # pool size without duplicates
        self.pool = list()  # result pool
        self.relevantUrls = list()
        self.irrelevantUrls = list()
        self.relevantUrlsFromGoogle = list()
        self.relevantUrlsFromBing = list()
        self.relevanceDict = dict()
        self.relevanceDictGoogle = dict()
        self.relevanceDictBing = dict()

    # get the count of relevant results from different engines
    def getRelevantCount(self, engineName):
        if engineName == "Google":
            return len(self.relevantUrlsFromGoogle)
        elif engineName == "Bing":
            return len(self.relevantUrlsFromBing)
        else:
            return -1

    # get query
    def getQuery(self):
        return self.query

    # get pool size after duplicate removal
    def getPoolSizeWithouDup(self):
        return self.poolSizeWithoutDup

    # get the count of duplicates
    def getDupCount(self):
        return self.poolSize - self.poolSizeWithoutDup

    # load url pool from .txt file,
    # which is generated by ExtractURLs.py
    def loadPool(self, fileName):
        with open(fileName, "r") as poolFile:
            lines = poolFile.readlines()
            self.query = lines[2][lines[2].index(":")+1:].strip()
            for i in range(len(lines)):
                if i == 0:
                    self.poolSize = int(lines[i][lines[i].index(":")+1:].strip())
                if i == 1:
                    self.poolSizeWithoutDup = int(lines[i][lines[i].index(":")+1:].strip())
                if i >= 4:  # skip headers of stats
                    self.pool.append(lines[i].strip())

    # load relevance records from .txt file,
    # which is generated by ExtractURLs.py
    def loadRelevanceRecord(self, fileName):
        with open(fileName, "r") as relevanceFile:
            lines = relevanceFile.readlines()
            for index, line in zip(range(1, len(lines)+1), lines):
                data = line.split(",")
                url = data[0]
                isRelevant = True if data[1] == "YES" else False
                reason = data[2]
                if isRelevant:
                    self.relevantUrls.append(url)
                else:
                    self.irrelevantUrls.append(url)
                # keep track of a relevance dictionary
                self.relevanceDict[url] = {
                                             "isRelevant": data[1],
                                             "reason":reason
                                             }

    # score the 20 results returned from a engine
    def scoreEngine(self, engineResultFileName):
        relevantCount = 0
        meanPrecisionAt10 = 0.0
        precisions = list()

        # iterate the results, calculate the precision
        with open(engineResultFileName, "r") as engineResultFile:
            lines = engineResultFile.readlines()
            meanPrecisionRecord = list()

            for lineCount,line in zip(range(1, len(lines)+1), lines):
                currentUrl = line.strip()

                # keep track of relevant urls
                if currentUrl in self.relevantUrls and "Google" in engineResultFileName:
                    self.relevantUrlsFromGoogle.append(currentUrl)
                if currentUrl in self.relevantUrls and "Bing" in engineResultFileName:
                    self.relevantUrlsFromBing.append(currentUrl)

                # update relevance dictionary
                if currentUrl in self.relevanceDict.keys() and "Google" in engineResultFileName:
                    self.relevanceDictGoogle[currentUrl] = {
                        "isRelevant": self.relevanceDict[currentUrl]["isRelevant"],
                        "reason": self.relevanceDict[currentUrl]["reason"]
                    }
                if currentUrl in self.relevanceDict.keys() and "Bing" in engineResultFileName:
                    self.relevanceDictBing[currentUrl] = {
                        "isRelevant": self.relevanceDict[currentUrl]["isRelevant"],
                        "reason": self.relevanceDict[currentUrl]["reason"]
                    }

                # calculate precision at each index
                if currentUrl in self.relevantUrls or self.pool.count(currentUrl) > 1:
                    relevantCount += 1
                    meanPrecisionRecord.append(relevantCount / float(lineCount))
                precisions.append(relevantCount / float(lineCount))

                if(lineCount == 10):    # calculate the mean precision at 10
                    meanPrecisionAt10 = sum(meanPrecisionRecord) / float(len(meanPrecisionRecord))

        precisionAt5 = precisions[4]
        precisionAt10 = precisions[9]
        precisionAt16 = precisions[15]

        # return a result list [preAt5, preAt10, preAt16, meanPreAt10]
        result = list()
        result.append(precisionAt5)
        result.append(precisionAt10)
        result.append(precisionAt16)
        result.append(meanPrecisionAt10)
        return result


if __name__ == "__main__":

    #####################################################################################
    ######################## Deal with the stats of Query 1 #############################
    #####################################################################################
    scoreTool1 = ScoreTool()
    scoreTool1.loadPool("Pool_Query1.txt")  # load result pool
    scoreTool1.loadRelevanceRecord("Relevance_Query1.txt")  # load relevance file

    scoreResultFromGoogle = scoreTool1.scoreEngine("Google_Results_Query1.txt") # score google results
    scoreResultFromBing = scoreTool1.scoreEngine("Bing_Results_Query1.txt") # score bing results

    # write output in particular format
    with open("Query1Metrics.txt", "a") as metricsFile1:
        metricsFile1.write("a.Query: " + scoreTool1.getQuery() + "\n")
        metricsFile1.write("b.Engine: Google\n")
        metricsFile1.write("c.Pool Size without Duplicates: " + str(scoreTool1.getPoolSizeWithouDup()) + "\n")
        metricsFile1.write("d.Number of Duplicates: " + str(scoreTool1.getDupCount()) + "\n")
        metricsFile1.write("e.Number of relevant results: " + str(scoreTool1.getRelevantCount("Google")) + "\n")
        metricsFile1.write("f.Relevance Table\nNumber\t\tResult URL\t\tRelevant\t\tReason\n")
        index = 1
        for url in scoreTool1.relevanceDictGoogle.keys():
            metricsFile1.write("{}\t{}\t{}\t{}".format(index,
                                                       url,
                                                       scoreTool1.relevanceDictGoogle[url]["isRelevant"],
                                                       scoreTool1.relevanceDictGoogle[url]["reason"]))
            index += 1
        metricsFile1.write("g.Metrics of Precision")
        metricsFile1.write("\t1.Precision at rank 5: " + str(scoreResultFromGoogle[0]) + "\n")
        metricsFile1.write("\t2.Precision at rank 10: " + str(scoreResultFromGoogle[1]) + "\n")
        metricsFile1.write("\t3.Precision at rank 16: " + str(scoreResultFromGoogle[2]) + "\n")
        metricsFile1.write("\t4.Avg Precision at rank 10: " + str(scoreResultFromGoogle[3]) + "\n")

    with open("Query1Metrics.txt", "a") as metricsFile1:
        metricsFile1.write("\n\n")
        metricsFile1.write("a.Query: " + scoreTool1.getQuery() + "\n")
        metricsFile1.write("b.Engine: Bing\n")
        metricsFile1.write("c.Pool Size without Duplicates: " + str(scoreTool1.getPoolSizeWithouDup()) + "\n")
        metricsFile1.write("d.Number of Duplicates: " + str(scoreTool1.getDupCount()) + "\n")
        metricsFile1.write("e.Number of relevant results: " + str(scoreTool1.getRelevantCount("Bing")) + "\n")
        metricsFile1.write("f.Relevance Table\nNumber\t\tResult URL\t\tRelevant\t\tReason\n")
        index = 1
        for url in scoreTool1.relevanceDictBing.keys():
            metricsFile1.write("{}\t{}\t{}\t{}".format(index,
                                                       url,
                                                       scoreTool1.relevanceDictBing[url]["isRelevant"],
                                                       scoreTool1.relevanceDictBing[url]["reason"]))
            index += 1
        metricsFile1.write("g.Metrics of Precision\n")
        metricsFile1.write("\t1.Precision at rank 5: " + str(scoreResultFromBing[0]) + "\n")
        metricsFile1.write("\t2.Precision at rank 10: " + str(scoreResultFromBing[1]) + "\n")
        metricsFile1.write("\t3.Precision at rank 16: " + str(scoreResultFromBing[2]) + "\n")
        metricsFile1.write("\t4.Avg Precision at rank 10: " + str(scoreResultFromBing[3]) + "\n")


    #####################################################################################
    ######################## Deal with the stats of Query 1 #############################
    #####################################################################################
    scoreTool2 = ScoreTool()
    scoreTool2.loadPool("Pool_Query2.txt")  # load result pool
    scoreTool2.loadRelevanceRecord("Relevance_Query2.txt")  # load relevance file

    scoreResultFromGoogle = scoreTool2.scoreEngine("Google_Results_Query2.txt")  # score google results
    scoreResultFromBing = scoreTool2.scoreEngine("Bing_Results_Query2.txt")  # score bing results

    # write output in particular format
    with open("Query2Metrics.txt", "a") as metricsFile1:
        metricsFile1.write("a.Query: " + scoreTool2.getQuery() + "\n")
        metricsFile1.write("b.Engine: Google\n")
        metricsFile1.write("c.Pool Size without Duplicates: " + str(scoreTool2.getPoolSizeWithouDup()) + "\n")
        metricsFile1.write("d.Number of Duplicates: " + str(scoreTool2.getDupCount()) + "\n")
        metricsFile1.write("e.Number of relevant results: " + str(scoreTool2.getRelevantCount("Google")) + "\n")
        metricsFile1.write("f.Relevance Table\nNumber\t\tResult URL\t\tRelevant\t\tReason\n")
        index = 1
        for url in scoreTool2.relevanceDictGoogle.keys():
            metricsFile1.write("{}\t{}\t{}\t{}".format(index,
                                                       url,
                                                       scoreTool2.relevanceDictGoogle[url]["isRelevant"],
                                                       scoreTool2.relevanceDictGoogle[url]["reason"]))
            index += 1
        metricsFile1.write("g.Metrics of Precision")
        metricsFile1.write("\t1.Precision at rank 5: " + str(scoreResultFromGoogle[0]) + "\n")
        metricsFile1.write("\t2.Precision at rank 10: " + str(scoreResultFromGoogle[1]) + "\n")
        metricsFile1.write("\t3.Precision at rank 16: " + str(scoreResultFromGoogle[2]) + "\n")
        metricsFile1.write("\t4.Avg Precision at rank 10: " + str(scoreResultFromGoogle[3]) + "\n")

    with open("Query2Metrics.txt", "a") as metricsFile1:
        metricsFile1.write("\n\n")
        metricsFile1.write("a.Query: " + scoreTool2.getQuery() + "\n")
        metricsFile1.write("b.Engine: Bing\n")
        metricsFile1.write("c.Pool Size without Duplicates: " + str(scoreTool2.getPoolSizeWithouDup()) + "\n")
        metricsFile1.write("d.Number of Duplicates: " + str(scoreTool2.getDupCount()) + "\n")
        metricsFile1.write("e.Number of relevant results: " + str(scoreTool2.getRelevantCount("Bing")) + "\n")
        metricsFile1.write("f.Relevance Table\nNumber\t\tResult URL\t\tRelevant\t\tReason\n")
        index = 1
        for url in scoreTool2.relevanceDictBing.keys():
            metricsFile1.write("{}\t{}\t{}\t{}".format(index,
                                                       url,
                                                       scoreTool2.relevanceDictBing[url]["isRelevant"],
                                                       scoreTool2.relevanceDictBing[url]["reason"]))
            index += 1
        metricsFile1.write("g.Metrics of Precision\n")
        metricsFile1.write("\t1.Precision at rank 5: " + str(scoreResultFromBing[0]) + "\n")
        metricsFile1.write("\t2.Precision at rank 10: " + str(scoreResultFromBing[1]) + "\n")
        metricsFile1.write("\t3.Precision at rank 16: " + str(scoreResultFromBing[2]) + "\n")
        metricsFile1.write("\t4.Avg Precision at rank 10: " + str(scoreResultFromBing[3]) + "\n")