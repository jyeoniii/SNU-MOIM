import { Subject } from './subject';
import { User } from './user';
import { Comment } from './comment';

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
