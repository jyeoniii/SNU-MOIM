"""
Source :
   euclidean_distance, jaccrd_similarity : http://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/
   sim_distance : https://github.com/python-recsys/django-recommends


Usage:
    measures = Similarity()
 
    print measures.euclidean_distance([0,3,4,5],[7,6,3,-1])
    print measures.jaccard_similarity([0,1,2,5,6],[0,2,3,5,7,9])

"""


from math import *
from decimal import Decimal
 
class Similarity():
 
    def euclidean_distance(self,x,y):
 
        """ return euclidean distance between two lists """
 
        return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
 

    def jaccard_similarity(self,x,y):
 
        """ returns the jaccard similarity between two lists """
 
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))

        return intersection_cardinality/float(union_cardinality)

 
 
    def sim_distance(self, p1, p2):
        """Returns a distance-based similarity score for p1 and p2"""
        # Get the list of shared_items
        si = [item for item in p1 if item in p2]

        if len(si) != 0:
            squares = [pow(p1[item] - p2[item], 2) for item in si]
            # Add up the squares of all the differences
            sum_of_squares = sum(squares)
            return 1 / (1 + sqrt(sum_of_squares))
        return 0

