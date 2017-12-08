import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Meeting } from '../models/meeting';
import { User } from '../models/user';

import { headerWithCSRF } from './header';

@Injectable()
export class RecommendService {

  private recommendUrl = '/api/recommend';

  constructor(private http: Http) { }

  getRecMeetings(user_id: number, N: number): Promise<Meeting[]> {
    const url = `${this.recommendUrl}/meeting/${user_id}/${N}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Meeting[])
      .catch(this.handleError);
  }

  getRecUsersForMeeting(user_id: number, meeting_id: number, N: number): Promise<User[]> {
    const url = `${this.recommendUrl}/user/meeting/${user_id}/${meeting_id}/${N}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as User[])
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }

}
