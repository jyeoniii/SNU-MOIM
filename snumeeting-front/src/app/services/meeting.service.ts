import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Meeting } from '../models/meeting';
import { User } from '../models/user';
import { Subject } from '../models/subject';
import { MeetingFB } from '../models/meetingFB';

import { headerWithCSRF } from './header';

@Injectable()
export class MeetingService {

  private meetingsUrl = 'api/meeting'; // URL to web api

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

  searchMeetingsOfTitle(query: string) {
    const url = `${this.meetingsUrl}/search/title/${query}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

  searchMeetingsOfAuthor(query: string) {
    const url = `${this.meetingsUrl}/search/author/${query}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

  searchMeetingsOfSubject(query: string) {
    const url = `${this.meetingsUrl}/search/subject/${query}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

  // createMeeting(meeting: Meeting): Promise<Meeting> {
  //
  //   return this.http.post(this.meetingsUrl, JSON.stringify({
  //       author_id: meeting.author.id,
  //       title: meeting.title,
  //       description: meeting.description,
  //       location: meeting.location,
  //       max_number: meeting.max_member,
  //       member: meeting.members,
  //       subject_id: meeting.subject.id,
  //     }),
  //     { headers: headerWithCSRF() })
  //     .toPromise()
  //     .then(response => response.json() as Meeting)
  //     .catch(this.handleError);
  // }


  createMeeting(author: User,
                title: string,
                subject: Subject,
                description: string,
                location: string,
                max_number: number,
                tag_names: string[]): Promise<void> {
    return this.http.post(this.meetingsUrl,
      JSON.stringify({
        author_id: author.id,
        title: title,
        subject_id: subject.id,
        description: description,
        location: location,
        max_member: max_number,
        tag_names: tag_names
      }),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
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
      .catch(response => {
        if (response.status === 404) return null;
        else this.handleError(response)
      });
  }

  editMeeting(editedMeeting: Meeting, tag_names: string[]): Promise<Meeting> {
    const url = `${this.meetingsUrl}/${editedMeeting.id}`;
    return this.http.put(url,
      JSON.stringify({
        title: editedMeeting.title,
        description: editedMeeting.description,
        location: editedMeeting.location,
        max_member: editedMeeting.max_member,
        subject_id: editedMeeting.subject.id,
        tag_names: tag_names
      }),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(() => editedMeeting)
      .catch(this.handleError);
  }

  deleteMeeting(id: number): Promise<Meeting> {
    const url = `${this.meetingsUrl}/${id}`;
    return this.http.delete(url, {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  joinMeeting(meeting_id: number, user_id: number) {
    const url = `api/joinMeeting/${meeting_id}`;
    return this.http.put(url,
      JSON.stringify({user_id: user_id}), {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  leaveMeeting(meeting_id: number, user_id: number) {
    const url = `api/leaveMeeting/${meeting_id}`;
    return this.http.put(url,
      JSON.stringify({user_id: user_id}), {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  closeMeeting(meeting_id: number): Promise<void> {
    const url = `api/closeMeeting/${meeting_id}`;
    return this.http.get(url)
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  getMeetingsOnTag(tagName: string): Promise<Meeting[]> {
    const url = `${this.meetingsUrl}/tag/${tagName}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(response => {
        if (response.status === 404) return [];
        else this.handleError(response);
      });
  }

  getMeetingsFromFBfriends(user_id: number): Promise<MeetingFB[]> {
    const url = `${this.meetingsUrl}/fb_friends/${user_id}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as MeetingFB[])
      .catch(this.handleError);
  }

  getJoinedMeeting(user_id: number): Promise<Meeting[]> {
    const url = `api/user/${user_id}/meeting`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

}
