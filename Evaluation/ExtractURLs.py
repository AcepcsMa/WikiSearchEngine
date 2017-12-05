__author__ = "Haoxiang Ma"

import requests
from bs4 import BeautifulSoup
import re

class SearchEngineCrawler(object):

    def __init__(self):
        self.headers = {
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        self.resultPerPageGoogle = 10
        self.resultPerPageBing = 10
        self.googleUrl = "https://www.google.com/search?q={}&start={}"
        self.bingUrl = "https://www.bing.com/search?q={}&first={}"

    def crawlGoogle(self, query, pageCount):

        urls = list()
        terms = query.split(" ")
        realQuery = "+".join(terms)
        for i in range(pageCount):
            page = i * self.resultPerPageGoogle
            searchUrl = self.googleUrl.format(realQuery, page)
            response = requests.get(searchUrl, headers=self.headers)
            pageHtml = response.content.decode()

            # use BeautifulSoup to extract urls
            soup = BeautifulSoup(pageHtml, "lxml")
            results = soup.find_all(name="h3", attrs={"class":"r"})

            # data cleaning
            currentPageUrls = [result.find(name="a")["href"].replace("/url?q=", "") for result in results]
            currentPageUrls = [re.sub("(&sa=.+)", "", url) for url in currentPageUrls]
            urls.extend(currentPageUrls)
        return urls

    def crawlBing(self, query, pageCount):

        urls = list()
        terms = query.split(" ")
        realQuery = "+".join(terms)
        for i in range(pageCount):
            startIndex = i * self.resultPerPageBing + 1
            searchUrl = self.bingUrl.format(realQuery, startIndex)
            response = requests.get(searchUrl, headers=self.headers)
            pageHtml = response.content.decode()

            # use BeautifulSoup to extract urls
            soup = BeautifulSoup(pageHtml, "lxml")
            results = soup.find_all(name="li", attrs={"class": "b_algo"})

            # data cleaning
            currentPageUrls = [result.find(name="h2").find(name="a")["href"] for result in results]
            urls.extend(currentPageUrls)
        return urls


if __name__ == "__main__":

    # initialize the crawler
    myCrawler = SearchEngineCrawler()

    ######################################################################
    ############# For Query1 recent climate change in Seattle ############
    ######################################################################
    # crawl google and bing
    googleResults = myCrawler.crawlGoogle(query="recent climate change in Seattle",
                                          pageCount=2)
    bingResults = myCrawler.crawlBing(query="recent climate change in Seattle",
                                      pageCount=2)

    # get the top 15 results from each engine
    topGoogleResults = googleResults[:15]
    topBingResults = bingResults[:15]
    resultPool = list()
    resultPool.extend(topGoogleResults)
    resultPool.extend(topBingResults)

    # remove duplicates
    uniqueResultPool = list(set(resultPool))

    with open("Pool_Query1.txt", "w") as urlStatFile:
        urlStatFile.write("Total Pool Size:{}\n".format(len(resultPool)))
        urlStatFile.write("Pool Size without Duplicates:{}\n".format(len(uniqueResultPool)))
        urlStatFile.write("\n")
        for url in resultPool:
            urlStatFile.write(url + "\n")

    with open("Google_Results_Query1.txt", "w") as googleFile:
        for url in googleResults:
            googleFile.write(url + "\n")

    with open("Bing_Results_Query1.txt", "w") as bingFile:
        for url in bingResults:
            bingFile.write(url + "\n")


    ######################################################################
    ########### For Query2 American president election process ###########
    ######################################################################
    # crawl google and bing
    googleResults = myCrawler.crawlGoogle(query="American president election process",
                                          pageCount=2)
    bingResults = myCrawler.crawlBing(query="American president election process",
                                      pageCount=2)

    # get the top 15 results from each engine
    topGoogleResults = googleResults[:15]
    topBingResults = bingResults[:15]
    resultPool = list()
    resultPool.extend(topGoogleResults)
    resultPool.extend(topBingResults)

    # remove duplicates
    uniqueResultPool = list(set(resultPool))

    with open("Pool_Query2.txt", "w") as urlStatFile:
        urlStatFile.write("Total Pool Size:{}\n".format(len(resultPool)))
        urlStatFile.write("Pool Size without Duplicates:{}\n".format(len(uniqueResultPool)))
        urlStatFile.write("\n")
        for url in resultPool:
            urlStatFile.write(url + "\n")

    with open("Google_Results_Query2.txt", "w") as googleFile:
        for url in googleResults:
            googleFile.write(url + "\n")

    with open("Bing_Results_Query2.txt", "w") as bingFile:
        for url in bingResults:
            bingFile.write(url + "\n")