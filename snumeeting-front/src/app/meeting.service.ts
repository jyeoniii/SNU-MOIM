import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { Meeting } from './meeting';
import { User } from './user';
import { Subject } from './subject';

@Injectable()
export class MeetingService {

  private meetingsUrl = 'api/meeting'; // URL to web api
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  private handleError(error: any): Promise<any> {
    console.error('An error occured', error);
    return Promise.reject(error.message || error);
  }

  /* Services for '/api/meeting'
  *  GET : Get all meeting data
  *  POST : Create new meeting
  */
  getMeetings(): Promise<Meeting[]> {
    return this.http.get(this.meetingsUrl)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

  createMeeting(author: User,
                title: string,
                subject: Subject,
                description: string,
                location: string,
                max_number: number): Promise<Meeting> {
    return this.http.post(this.meetingsUrl, JSON.stringify(
      {author_id: author.id, title: title, subject_id: subject.id, description: description, location: location, max_number: max_number}),
      { headers: this.headers })
      .toPromise()
      .then(response => response.json() as Meeting)
      .catch(this.handleError);
  }

  /* Services for '/api/meeting/:id'
  *  GET : Get specified meeting
  *  PUT : Edit specified meeting
  *  DELETE : Delete specified meeting
  */
  getMeeting(id: number): Promise<Meeting> {
    const url = `${this.meetingsUrl}/${id}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting)
      .catch(this.handleError);
  }

  editMeeting(editedMeeting: Meeting): Promise<Meeting> {
    const url = `${this.meetingsUrl}/${editedMeeting.id}`;
    return this.http.put(url, {title: editedMeeting.title,
                                     description: editedMeeting.description,
                                     location: editedMeeting.location,
                                     max_member: editedMeeting.max_member,
                                     subject_id: editedMeeting.subject.id }, { headers: this.headers })
      .toPromise()
      .then(() => editedMeeting)
      .catch(this.handleError);
  }

  deleteMeeting(id: number): Promise<Meeting> {
    const url = `${this.meetingsUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }
}
