__author__ = "Haoxiang Ma"

import math

class VectorUtil:

    def cosineSimilarity(self, vectorA, vectorB):
        # check if two vectors are of the same length
        if(len(vectorA) != len(vectorB)):
            raise Exception("Size of vectorA does not equal to size of vectorB")

        numerator = 0.0
        for valueA, valueB in zip(vectorA, vectorB):
            numerator += valueA*valueB
        denominator = math.sqrt(self.vectorSize(vectorA) * self.vectorSize(vectorB))
        return numerator / denominator


    def vectorSize(self, vector):
        size = 0.0
        for value in vector:
            size += value*value
        return size