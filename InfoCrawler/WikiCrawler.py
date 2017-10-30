__author__ = "Haoxiang Ma"

import queue
import requests
import re
import time
import sys

class WikiCrawler:

    def __init__(self, numPages, maxDepthLimit, seedUrl, pauseTime):
        self.taskQueue = queue.Queue()
        self.finishedUrls = set()
        self.seedUrl = seedUrl
        self.numPageLimit = numPages
        self.maxDepthLimit = maxDepthLimit
        self.pauseTime = pauseTime
        self.pageCount = 0

        self.maxPageSize = -1
        self.minPageSize = sys.maxsize
        self.sumPageSize = 0
        self.currentMaxDepth = 0

        self.wikiPrefix = "https://en.wikipedia.org"    # the urls in wiki pages lack prefix
        self.stopWords = ["Main_Page"]

    def crawl(self):
        # while the task queue is not empty, get task from the queue
        while(self.taskQueue.empty() is False):
            if(self.pageCount >= self.numPageLimit): # but if the page count goes over the limit, break
                break

            # get a task from task queue
            currentTask = self.taskQueue.get()
            currentUrl = currentTask["url"]
            if(currentUrl in self.finishedUrls): # check if current page has been crawled
                continue
            currentDepth = currentTask["depth"]
            if(currentDepth > self.maxDepthLimit):   # check if the depth of current page exceeds max depth
                continue

            try:
                # send http request to get page content
                response = requests.get(currentUrl)
                pageContent = response.content.decode()
                pageContent = re.findall("<div id=\"bodyContent\".+?<div id=\"mw-navigation\">", pageContent, re.S)[0]
            except:
                continue

            # try to get content length of this page, and update related stats
            try:
                currentPageSize = int(response.headers["Content-Length"])
                self.sumPageSize += currentPageSize
                if(currentPageSize > self.maxPageSize):
                    self.maxPageSize = currentPageSize
                elif(currentPageSize < self.minPageSize):
                    self.minPageSize = currentPageSize
            except:
                currentPageSize = len(response.content.decode())
            self.pageCount += 1

            # update the max depth reached if necessary
            if(currentDepth > self.currentMaxDepth):
                self.currentMaxDepth = currentDepth

            # extract urls from current page content, then put them into the task queue
            links = self.extractLinks(pageContent)
            for linkUrl in links:
                if(linkUrl not in self.finishedUrls):
                    for stopWord in self.stopWords:
                        if(stopWord not in linkUrl):    # ignore some useless pages
                            self.taskQueue.put({"url":linkUrl,"depth":currentDepth+1})

            # save current page content to local file, and put current url into finished set
            self.saveToLocalFile(self.pageCount, currentUrl, pageContent, self.pageCount)
            self.finishedUrls.add(currentUrl)
            print (str(self.pageCount)+ " Finshed crawling:" + currentUrl)

            # sleep for a while to be polite :)
            time.sleep(self.pauseTime)

    # use regular expression to extract urls from the page content
    def extractLinks(self, pageContent):
        links = re.findall("<a href=\"(.+?)\".+?>", pageContent)
        links = [self.wikiPrefix+link for link in links]
        return links

    # call this method to save page contents to local file
    def saveToLocalFile(self, pageCount, url, content, numPage):
        with open("./files/{}.txt".format(numPage), "w") as pageFile:
            pageFile.write(content)
        with open("./URLsCrawled.txt", "a") as urlFile:
            urlFile.write(str(pageCount) + " " + url + "\n")

    # call this method to write stats to local file
    def writeStat(self):
        with open("./stats.txt", "w") as statFile:
            statFile.write("Maximum size:" + str(self.maxPageSize) + " bytes\n")
            statFile.write("Minimum size:" + str(self.minPageSize) + " bytes\n")
            statFile.write("Average size:" + str(self.sumPageSize/self.pageCount) + " bytes\n")
            statFile.write("Maximum depth reach:" + str(self.currentMaxDepth))

    # call this method to start crawling
    def start(self):
        self.taskQueue.put({"url":self.seedUrl,"depth":1})
        self.crawl()
        self.writeStat()
