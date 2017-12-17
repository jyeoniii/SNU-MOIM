import { User } from './user';
import { Datetime } from './datetime';

export class Message {
	id: number;
	sender: User;
	receiver: User;
	content: string;
	datetime: Datetime;
}

