1. The most difficult / easiest part
    The most difficult part would be handling the flow of data. Because in the partI of this assignment, I do the
transformation of text data, then I have to design how to 'flow' the data into partII. The final solution is keeping
all necessary data inside an instance of transformer, and then use it to construct an index creator.
    The easiest part is developing some methods in UseIndex for users to do the search. Because all of the data have
been kept properly during the transformation & index creation, so it's easy to find them and display.

2. The format of index files
    I use JSON to encapsulate all the indexes.
    For the TermIDFile, the structure is like:
    {
        "1":{
                "term":"Gerard",
                "docFreq":18        // the number of documents that this term occurs in
            }

        "2":{
                "term":"Wikipedia",
                "docFreq":8
            }
    }

    For the DocumentIDFile, the structure is like:
    {
        "1":{
                "docName":"doc1.txt",
                "docLength":150         // the number of tokens in this document
            }

        "2":{
                "docName":"doc2.txt",
                "docLength":450
            }
    }

    For the InvertedIndex.txt, the structure is like:
    {
        "1":[{"docID":1, "frequency":10}, {"docID":2, "frequency":7}]

        "2":[{"docID":5, "frequency":16}, {"docID":7, "frequency":18}]
    }

3. Query and result
    I run a query "Who Is Gerard" (python3 UseIndex --search Who Is Gerard),
    and the result is:
    ['1.txt', '13.txt', '101.txt', '103.txt', '104.txt', '107.txt', '108.txt', '139.txt', '14.txt', '112.txt', '119.txt', '124.txt']

4. Additional information

    ######################### Important! #########################
    # You have to run CreateIndex.py before doing the search! ####
    # Otherwise, there would not be index files, nothing you #####
    # can get from the search. But you don't have to run RunData #
    # Transformer.py, because I do the transformation in Create ##
    # Index.py before creating indexes. ##########################

    The command should be like:
    python3 CreateIndex.py [the folder path] [num of file processed]

    Then if you want to run UseIndex.py, you have 5 options:
    * python3 UseIndex --getTermID [term]

    * python3 UseIndex --getInvertedList [termID]

    * python3 UseIndex --getDocumentIDs [term]

    * python3 UseIndex --getDocumentName [documentID]

    * python3 UseIndex --search [a complete query]
