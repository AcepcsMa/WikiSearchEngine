__author__ = "Haoxiang Ma"
from WikiCrawler import WikiCrawler
import sys
import os


if __name__ == "__main__":
    seedUrl = sys.argv[1]
    numPages = int(sys.argv[2])
    maxDepth = 5
    pauseTime = 3

    if(os.path.exists("./files") is False):
        os.mkdir("./files")

    crawler = WikiCrawler(numPages,maxDepth,seedUrl,pauseTime)
    crawler.start()