1. The most difficult / easiest part
    The most difficult part is generating tf-idf vectors for each query & each document and recording the stats.
    Because we have to use data from some inverted index files in last assignment in order to get df efficiently and
    record some key intermediate results(like tf-idf contribution of each word) during the process.
    The easiest part would be calculating the cosine similarity and sorting. Because once we get the vectors, it's easy
    to perform the calculation. And we can use the dictionary to save similarity results, which can be sorted easily.

2. Nothing changes in the 3 index files, everything remains unchanged in Assignment2. I just reused them.

3. Additional information

    ############################# Important! #############################
    # You have to make sure documents folder is correct & indexFolder ####
    # is correct! This script can not run without crawled documents and ##
    # index files! #######################################################

    To run the RunRankRetrieval.py, the command should be like:
    python3 RunRankRetrieval.py [indexFolderPath] [documentFolderPath] [QueryFilePath] [topK]

    Examples:
    * python3 RunRankRetrieval.py ../indexFiles/ ../documentFiles/ Queries.txt 5
