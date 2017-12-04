import { User } from './user';

export class Message {
	id: number;
	sender: User;
	receiver: User;
	content: string;
	sended_at: string;
}

