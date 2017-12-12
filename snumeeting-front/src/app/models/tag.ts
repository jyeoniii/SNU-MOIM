import { Meeting } from './meeting';

export class Tag {
  id: number;
  name: string;
  meetings_on_tag: Meeting[];
}
