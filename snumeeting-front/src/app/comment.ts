import { User } from './user';
import { Meeting } from './meeting';

export class Comment {
  id: number;
  author: User;
  meeting: Meeting;
  content: string;
  publicity = true;
}
