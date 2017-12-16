import { Subject } from './subject';
import { User } from './user';
import { Tag } from './tag';

export class Meeting {
  id: number;
  author: User;
  title: string;
  subject: Subject;
  description: string;
  location: string;
  max_member: number;
  members: User[];
  is_closed: boolean;
  tags: Tag[];
}
