import { User } from './user';
import { College } from './college';
import { Subject } from './subject';
import { Meeting } from './meeting';
import { Comment } from './comment';

const college = [
  {id: 1, name: 'Engineering'},
  {id: 2, name: 'Business'},
];

const subject = [
  {id: 1, name: 'English', interest: 'study'},
  {id: 2, name: 'Chinese', interest: 'study'},
  {id: 3, name: 'Band', interest: 'performance'},
];

const user = [
  {id: 1, username: 'fake', password: '1234', name: 'name', college: college[0], subjects: [subject[0]]},
  {id: 2, username: 'fake2', password: '1234', name: 'name2', college: college[1], subjects: [subject[1], subject[2]]},
  {id: 3, username: 'fake3', password: '1234', name: 'name3', college: college[1], subjects: [subject[2]]},
];

const meeting = [
  {id: 1, author: user[0], title: 'Mock-title1', subject: subject[0],
    description: 'Description1', location: 'SNUstation', max_member: 4, members: [ user[0] ] },
  {id: 2, author: user[1], title: 'Mock-title2', subject: subject[1],
    description: 'Description2', location: 'SNU', max_member: 5, members: [ user[0] ] },
  {id: 3, author: user[2], title: 'Mock-title3', subject: subject[2],
    description: 'Description3', location: 'Nokdu', max_member: 6, members: [ user[0], user[1] ] },
  {id: 4, author: user[2], title: 'Mock-title4', subject: subject[0],
    description: 'Description4', location: 'SNU', max_member: 3, members: [ user[0], user[1] ] },
];

const comment = [
  {id: 1, author: user[0], meeting_id: 3, content: 'Hi', publicity: true},
  {id: 2, author: user[0], meeting_id: 2, content: 'Hello', publicity: true},
  {id: 3, author: user[1], meeting_id: 1, content: 'Hiiiiiii', publicity: true},
  {id: 4, author: user[1], meeting_id: 2, content: 'Nooooooooo', publicity: true},
  {id: 5, author: user[2], meeting_id: 3, content: 'What?', publicity: true},
];

const interest = ['study', 'performance'];

export const makeCollegeData = () => college as College[];
export const makeUserData = () => user as User[];
export const makeInterestData = () => interest as string[];
export const makeMeetingData = () => meeting as Meeting[];
export const makeCommentData = () => comment as Comment[];
export const makeSubjectData = () => subject as Subject[];

