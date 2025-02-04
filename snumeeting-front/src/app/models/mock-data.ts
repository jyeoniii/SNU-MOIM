
import { User } from './user';
import { College } from './college';
import { Subject } from './subject';
import { Meeting } from './meeting';
import { Comment } from './comment';
import { Interest } from './interest';
import { Message } from './message';
import { Tag } from './tag';

const college = [
  {id: 1, name: 'Engineering'},
  {id: 2, name: 'Business'},
];

const subject = [
  {id: 1, name: 'English', interest_id: 1},
  {id: 2, name: 'Chinese', interest_id: 1},
  {id: 3, name: 'Band', interest_id: 2},
];

const interest = [
  { id: 1, name: 'Study', subjects: [subject[0], subject[1]]},
  { id: 2, name: 'Performance', subjects: [subject[2]]}
];

const user = [
  {id: 1, username: 'fake', name: 'name', college: college[0], subjects: [subject[0]]},
  {id: 2, username: 'fake2', name: 'name2', college: college[1], subjects: [subject[1], subject[2]]},
  {id: 3, username: 'fake3', name: 'name3', college: college[1], subjects: [subject[2]]},
];

const meeting = [
  {id: 1, author: user[0], title: 'Mock-title1', subject: subject[0],
    description: 'Description1', location: 'SNUstation', max_member: 4, members: [ user[0] ], is_closed: false },
  {id: 2, author: user[1], title: 'Mock-title2', subject: subject[1],
    description: 'Description2', location: 'SNU', max_member: 5, members: [ user[0] ], is_closed: false  },
  {id: 3, author: user[2], title: 'Mock-title3', subject: subject[2],
    description: 'Description3', location: 'Nokdu', max_member: 6, members: [ user[0], user[1] ], is_closed: false  },
  {id: 4, author: user[2], title: 'Mock-title4', subject: subject[0],
    description: 'Description4', location: 'SNU', max_member: 3, members: [ user[0], user[1] ], is_closed: false  },
];

const comment = [
  {id: 1, author: user[0], meeting_id: 3, content: 'Hi', publicity: true},
  {id: 2, author: user[0], meeting_id: 2, content: 'Hello', publicity: true},
  {id: 3, author: user[1], meeting_id: 1, content: 'Hiiiiiii', publicity: true},
  {id: 4, author: user[1], meeting_id: 2, content: 'Nooooooooo', publicity: true},
  {id: 5, author: user[2], meeting_id: 3, content: 'What?', publicity: true},
];

const message = [
  {id: 1, sender: user[0], receiver: user[1], content: 'Bye'},
  {id: 2, sender: user[1], receiver: user[0], content: 'Ok, bye'},
  {id: 3, sender: user[1], receiver: user[2], content: 'You want to join us?'},
  {id: 4, sender: user[2], receiver: user[0], content: 'Get it on'},
  {id: 5, sender: user[0], receiver: user[2], content: 'Ok'},
  {id: 6, sender: user[2], receiver: user[1], content: 'Right'},
];

const tag = [
  {id: 1, name: 'study', meetings_on_tag:[meeting[0], meeting[1]]},
  {id: 2, name: 'english', meetings_on_tag:[meeting[2], meeting[3]]},
]

export const makeCollegeData = () => college as College[];
export const makeUserData = () => user as User[];
export const makeInterestData = () => interest as Interest[];
export const makeMeetingData = () => meeting as Meeting[];
export const makeCommentData = () => comment as Comment[];
export const makeSubjectData = () => subject as Subject[];
export const makeMessageData = () => message as Message[];
export const makeTagData = () => tag as Tag[];
