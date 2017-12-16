import { User } from './user';
import { Datetime } from './datetime';


export class Comment {
  id: number;
  author: User;
  meeting_id: number;
  content: string;
  publicity = true;
  datetime: Datetime;
}
