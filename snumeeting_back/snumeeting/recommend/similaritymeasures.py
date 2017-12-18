"""
Source :
   http://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/

Usage:
    measures = Similarity()
    print measures.euclidean_distance([0,3,4,5],[7,6,3,-1])

"""


from math import *
from decimal import Decimal
 
def euclidean_distance(x,y):
  """ return euclidean distance between two lists """
  return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

