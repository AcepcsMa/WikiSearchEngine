__author__ = "Haoxiang Ma"

import math

class VectorUtil:

    def cosineSimilarity(self, vectorA, vectorB):
        # check if two vectors are of the same length
        if(len(vectorA) != len(vectorB)):
            raise Exception("Size of vectorA does not equal to size of vectorB")

        # calculate cosine similarity and record contributions
        similarity = 0.0
        contributions = list()
        for valueA, valueB in zip(vectorA, vectorB):
            similarity += valueA*valueB
            contributions.append(valueA*valueB)
        return similarity, contributions
