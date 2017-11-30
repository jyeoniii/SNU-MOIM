from snumeeting.models import Ex_User, College
from .similaritymeasures import Similarity 
from .JoinHistoryManager import JoinHistoryManager
import heapq
from operator import itemgetter

def getUserSimilarity(target):
  # Find the user having the most similar join history

  K = 5   # number of similar users to be recommended
  measure = Similarity()
  manager = JoinHistoryManager()
  users = Ex_User.objects.all()
  similarities = {}

  jh_target = manager.convertToList(target.joinHistory)

  d_colleges= getCollegeDistance(target.college)
  print(d_colleges)

  for user in users:
    if user.id == target.id:
      continue
    jh_user = manager.convertToList(user.joinHistory)
    jh_d = measure.euclidean_distance(jh_target, jh_user)  # Interest Distance 
    col_d = d_colleges[user.college_id]          # College Distance 

    # Convert distance to similarity
    # (Current weight) InterestDistance:CollegeDistance = 2:1
    print("id:"+str(user.id)+" interest distance: "+str(jh_d)+ " / college distance: " + str(col_d/2))
    similarities[user.id] = 1 / (1 + jh_d + col_d/2)  

  return heapq.nlargest(K, similarities.items(), key=itemgetter(1)) 

  
def getCollegeDistance(target):
  measure = Similarity()
  manager = JoinHistoryManager()
  colleges = College.objects.all()

  distances = {}
  sum = 0

  jh_target = manager.convertToList(target.joinHistory)

  for college in colleges:
    if college.id == target.id:
      distances[college.id] = 0 
      continue
    jh_college = manager.convertToList(college.joinHistory)
    d = measure.euclidean_distance(jh_target, jh_college)
    distances[college.id] = d
    sum += d

  #return {k: v / sum for k, v in distances.items()}  # Proportion (sum=1)
  return distances


