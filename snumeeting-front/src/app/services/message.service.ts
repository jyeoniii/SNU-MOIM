import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import { Message } from '../models/message';
import { User } from '../models/user';

@Injectable()
export class MessageService {

  private usersUrl = 'api/user';
  private messagesUrl = 'api/message';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  private handleError(error: any): Promise<any> {
    console.error('An error occured', error);
    return Promise.reject(error.message || error);
  }

  /* Services for '/api/user/:id/message/receiver or sender'
  *  GET : Get all messages on specified receiver or sender
  */
  getReceivedMessage(id: number): Promise<Message[]> {
    const url = '/api/user/${id}/message/received';
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Message[])
      .catch(this.handleError);
  }

  getSentMessage(id: number): Promise<Message[]> {
    const url = '/api/user/${id}/message/sent';
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Message[])
      .catch(this.handleError);
  }

  /* Services for '/api/message'
  *  GET : Get all messages
  *  POST : Send message
  */
  getMessages(): Promise<Message[]> {
    const url = `${this.messagesUrl}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Message[])
      .catch(this.handleError);
  }

  sendMessage(sender: User, receiver: User, content: string): Promise<Message> {
    const url = `${this.messagesUrl}`;
    return this.http.post(url, JSON.stringify(
      {sender_id: sender.id, receiver_id: receiver.id, content: content}),
      { headers: this.headers })
      .toPromise()
      .then(response => response.json() as Message)
      .catch(this.handleError);
  }

  /* Services for '/api/message/:id'
  *  GET : Get specified message
  *  DELETE : Delete specified message
  */

  getMessage(id: number): Promise<Message> {
    const url = '${this.messagesUrl}/${id}';
    return this.http.get(url, {headers: this.headers})
      .toPromise()
      .then(response => response.json() as Message)
      .catch(this.handleError);
  }

  deleteMessage(id: number): Promise<Message> {
    const url = `${this.messagesUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }
}
