import { User } from './user';
import { Meeting } from './meeting';

export class Comment {
  id: number;
  author: User;
  meeting_id: number;
  content: string;
  publicity = true;
}
