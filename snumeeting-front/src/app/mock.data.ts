import { User } from './user';
import { College } from './college';
import { Subject } from './subject';

export const collegeData = [
  {
    id: 4,
    name: 'Agriculture & Life Sciences'
  },
  {
    id: 5,
    name: 'Business Administration'
  },
  {
    id: 6,
    name: 'Education'
  },
  {
    id: 7,
    name: 'Engineering'
  }
] as College[];

export const interestData = [
  'Study',
  'Performance',
  'Volunteering'
] as string[];

export const subjectData = [
  {
    id: 1,
    interest: 'Study',
    name: 'Study_English'
  },
  {
    id: 2,
    interest: 'Study',
    name: 'Study_Computer'
  },
  {
    id: 3,
    interest: 'Performance',
    name: 'Perform_Band'
  },
  {
    id: 4,
    interest: 'Performance',
    name: 'Perform_Play'
  },
  {
    id: 5,
    interest: 'Volunteering',
    name: 'Volun_Teaching'
  }
] as Subject[];

export const userData = [
  {
    id: 1,
    username: 'hello',
    password: 'hellohello',
    name: 'jiyun',
    college: collegeData[2],
    subjects: [subjectData[0], subjectData[2], subjectData[4]]
  },
  {
    id: 2,
    username: 'swpp1234',
    password: 'password',
    name: 'swpp',
    college: collegeData[3],
    subjects: [subjectData[1]]
  }
] as User[];
