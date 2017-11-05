import { Subject } from './subject';
import { User } from './user';

export class Meeting {
  id: number;
  author: User;
  title: string;
  subject: Subject;
  description: string;
  location: string;
  max_member: number;
  members: User[];
}
