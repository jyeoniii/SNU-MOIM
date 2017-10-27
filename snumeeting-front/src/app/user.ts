import { Subject } from './subject';
import { College } from './college';

export class User {
  mySNU_id: string;
  password: string;
  name: string;
  college: College;
  interest: Subject[];
}
