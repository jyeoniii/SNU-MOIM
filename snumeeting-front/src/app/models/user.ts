import { Subject } from './subject';
import { College } from './college';

export class User {
  id: number;
  username: string;
  password: string;
  name: string;
  college: College;
  subjects: Subject[];
  token_expired = false;
}
