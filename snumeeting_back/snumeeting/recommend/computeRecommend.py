from django.forms.models import model_to_dict
from snumeeting.models import Ex_User, College
from .similaritymeasures import Similarity 
from .JoinHistoryManager import JoinHistoryManager
import heapq
import random
from operator import itemgetter

def getRecMeetings(target, N):
  # Get meetings that similar users is joined
  # N : maximum number of meetings to be recommended

  K = 3     # number of similar users to be recommended
  target_interests = target.subjects.all()
  scores = {} 

  similar_users = dict(getUserSimilarity(target,K))
  print(similar_users)

  # Score based on similar users
  sim_user_ids = list(similar_users.keys())
  for uid in sim_user_ids:
    user = Ex_User.objects.get(id=uid)
    meetings_joined = list(user.meetings_joined.all())

    for m in meetings_joined:
      if not (m.is_closed or (target in m.members.all())):  # exclude closed meeting or one that target user is already joined
        scores[m] = similar_users[uid]

  # Score based on target user's interest
  for subject in target_interests:
    for m in subject.meetings.all():
      if not (m.is_closed or (target in m.members.all())):  # exclude closed meeting or one that target user is already joined
        if m in scores.keys():
          scores[m] += 0.15    # Give 15% advantage for meetings in categories that user is interested
        else:
          scores[m] = 0.15

  topN = heapq.nlargest(N, scores.items(), key=itemgetter(1)) 

  # Helper function: remove Queryset type 'members' which is not serializable
  def removeQuerySets(meeting):
    del meeting['members']
    del meeting['tags']
    return meeting

  return list(map(lambda x: removeQuerySets(x), [model_to_dict(t[0]) for t in topN])) 



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
    if target.joinHistory != "{}":
      jh_user = manager.convertToList(user.joinHistory)
      jh_d = measure.euclidean_distance(jh_target, jh_user)  # Interest Distance 
    else:  # Cold start -> computing join history similarity is meaningless
      jh_d = 0
    col_d = d_colleges[user.college_id]          # College Distance 

    # Convert distance to similarity
    # (Current weight) InterestDistance:CollegeDistance = 3:1
    # print("id:"+str(user.id)+" interest distance: "+str(jh_d)+ " / college distance: " + str(col_d/2))
    similarities[user.id] = 1 / (1 + jh_d + col_d/3)  

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

  return distances


