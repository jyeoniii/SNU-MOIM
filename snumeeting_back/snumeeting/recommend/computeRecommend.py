from snumeeting.models import Ex_User, College
from .similaritymeasures import Similarity 
from .JoinHistoryManager import JoinHistoryManager
import heapq
import random
from operator import itemgetter

def getRecMeetingsUserBased(target, N):
  # Get meetings that similar users is joined
  # N : maximum number of meetings to be recommended

  K = 3     # number of similar users to be recommended
  similar_users = dict(getUserSimilarity(target,K))
  result = []

  sim_user_ids = list(similar_users.keys())
  for uid in sim_user_ids:
    user = Ex_User.objects.get(id=uid)
    meetings_joined = list(user.meetings_joined.all())
    result += meetings_joined

  if len(result) > N:
    result = result[:N]

  result = list(filter(
      (lambda m: not (m.is_closed or (target in m.members.all()))),
       result))

  return result

def getUserSimilarity(target, K):
  # Find the user having the most similar join history
  # target : target user to calculte similarity
  # K : number of similar users to be recommended
  # return: List of tuples - [ top K (Ex_User's id, similarity score) ]

  measure = Similarity()
  manager = JoinHistoryManager()
  users = Ex_User.objects.all()
  similarities = {}

  jh_target = manager.convertToList(target.joinHistory)

  d_colleges= getCollegeDistance(target.college)

  for user in users:
    if user.id == target.id:
      continue
    jh_user = manager.convertToList(user.joinHistory)
    jh_d = measure.euclidean_distance(jh_target, jh_user)  # Interest Distance 
    col_d = d_colleges[user.college_id]          # College Distance 

    # Convert distance to similarity
    # (Current weight) InterestDistance:CollegeDistance = 2:1
    # print("id:"+str(user.id)+" interest distance: "+str(jh_d)+ " / college distance: " + str(col_d/2))
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


