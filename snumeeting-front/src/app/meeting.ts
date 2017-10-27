import { Subject } from './subject';
import { User } from './user';

export class Meeting {
  author: User;
  subject: Subject;
  description: string;
  location: string;
  max_number: number;
  members: User[];
}
