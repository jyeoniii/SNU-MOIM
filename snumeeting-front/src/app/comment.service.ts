import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import { Comment } from './comment';
import { User } from './user';
import { Meeting } from './meeting';

@Injectable()
export class CommentService {

  private meetingsUrl = 'api/meeting';
  private commentsUrl = 'api/comment'; // URL to web api
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  private handleError(error: any): Promise<any> {
    console.error('An error occured', error);
    return Promise.reject(error.message || error);
  }

  /* Services for '/api/:id/comment'
  *  GET : Get all comments on specified meeting
  *  POST : Create new comment on specified meeting
  */
  getCommentsOnMeeting(meetingId: number): Promise<Comment[]> {
    const url = `${this.meetingsUrl}/${meetingId}/comment`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Comment[])
      .catch(this.handleError);
  }

  createComment(meetingId: number, author: User, content: string, publicity: boolean): Promise<Comment> {
    const url = `${this.meetingsUrl}/${meetingId}/comment`;

    return this.http.post(url, JSON.stringify(
      {author_id: author.id, content: content, publicity: publicity}),
      { headers: this.headers })
      .toPromise()
      .then(response => response.json().data as Comment)
      .catch(this.handleError);
  }

  /* Services for '/api/comment/:id'
  *  GET : Get specified comment
  *  PUT : Edit specified comment
  *  DELETE : Delete specified comment
  */
  getComment(id: number): Promise<Comment> {
    const url = `${this.commentsUrl}/${id}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json().data as Comment[])
      .catch(this.handleError);
  }

  editComment(editedComment: Comment): Promise<Comment> {
    const url = `${this.commentsUrl}/${editedComment.id}`;
    return this.http.put(url, JSON.stringify(editedComment), { headers: this.headers })
      .toPromise()
      .then(() => editedComment)
      .catch(this.handleError);
  }

  deleteComment(id: number): Promise<Comment> {
    const url = `${this.commentsUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }
}
