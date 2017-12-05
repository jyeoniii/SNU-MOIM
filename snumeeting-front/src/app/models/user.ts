import { Subject } from './subject';
import { College } from './college';

export class User {
  id: number;
  username: string;
  password: string;
  name: string;
  college: College;
  subjects: Subject[];
  fb_friends: User[];
  fb_connected: boolean;
  token_expired = false;
}
