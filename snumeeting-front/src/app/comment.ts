import { User } from './user';
import { Meeting } from './meeting';

export class Comment {
  author: User;
  meeting: Meeting;
  content: string;
  publicity = true;
}
