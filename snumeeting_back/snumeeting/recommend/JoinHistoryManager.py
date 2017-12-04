import json
from snumeeting.models import Subject

class JoinHistoryManager(object):
  # Count # of joined meetings for each category (use subject_id)

  def increaseCnt(self, joinHistory, subject_id):
    cnts = json.loads(joinHistory)
    if str(subject_id) in cnts.keys():
      prev = cnts.pop(str(subject_id))
    else:
      prev = 0;
    cnts[subject_id] = prev+1;
    return json.dumps(cnts)

  def decreaseCnt(self, joinHistory, subject_id):
    cnts = json.loads(joinHistory)
    if str(subject_id) in cnts.keys():
      prev = cnts.pop(str(subject_id))
    else:
      """ TODO: Error handling """
    cnts[subject_id] = prev-1;
    return json.dumps(cnts)

  def getCounts(self, joinHistory):
    return json.loads(joinHistory)

  def getCount(self, joinHistory, subject_id):
    cnts = json.loads(joinHistory)
    if str(subject_id) in cnts.keys():
      return cnts[str(subject_id)]
    else:
      return 0;

  def convertToList(self, joinHistory):
    result = []
    counts_dict = json.loads(joinHistory)
    subjects = Subject.objects.all()

    for subject in subjects:
      subject_id = subject.id
      if str(subject_id) in counts_dict.keys():
        result.append(counts_dict[str(subject_id)])
      else:
        result.append(0)

    return result


