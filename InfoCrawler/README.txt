1. The urls in the HTML pages of wiki are lacked of prefix("https://en.wikipedia.org"), so I had to
deal with this problem, adding prefix to each of the original urls before pushing them into the task queue.
And I had to set the sleep interval longer than one second, because I was stopped by the server when I crawled
around 100 pages with a one-second sleep interval.

2. I am using python3, and a third-party package named requests. Just run the script 'RunCrawler.py' with the
following command:
    python3 RunCrawler.py "https://en.wikipedia.org/wiki/Gerard_Salton" 800