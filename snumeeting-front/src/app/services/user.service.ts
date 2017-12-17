import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { User } from '../models/user';
import { UserFB } from '../models/userFB';

import { headerWithCSRF } from './header';

@Injectable()
export class UserService {
  private static loginedUser = null;
  private userUrl = '/api/user';
  private tokenUrl = '/api/token';

  constructor(private http: Http) {
  }

  user: User = new User();

  getToken() {
    this.http.get(this.tokenUrl)
      .toPromise()
      .catch(this.handleError);
  }

  checkUser(username: string): Promise<boolean> {
    return this.http.post('/api/check_user',
      JSON.stringify({username: username}),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(() => true, () => false)
      .catch(this.handleError);
  }

  signIn(username: string, password: string): Promise<User> {
    return this.http.post('/api/signin',
      JSON.stringify({username: username, password: password}),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(response => response.json() as User, () => null)
      .catch(this.handleError);
  }

  signUp(user: User, password: string): Promise<void> {
    const subjectIDList: number[] = [];
    for (const subject of user.subjects) {
      subjectIDList.push(subject.id);
    }

    return this.http.post('/api/signup', JSON.stringify({
        username: user.username,
        name: user.name,
        password: password,
        college_id: user.college.id,
        subject_ids: subjectIDList
      }),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  signOut(): Promise<void> {
    // call this.loginedUser = new User() with then of this function
    return this.http.get('/api/signout', {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  getUsers(): Promise<User[]> {
    return this.http.get('/api/user')
      .toPromise()
      .then(response => response.json() as User[])
      .catch(this.handleError);
  }

  getUserInfo(id: number): Promise<User> {
    return this.http.get(`${this.userUrl}/${id}`)
      .toPromise()
      .then(response => response.json() as User)
      .catch(this.handleError);
  }

  editUserInfo(user: User, password: string): Promise<void> {
    const subjectIDList: number[] = [];
    for (const subject of user.subjects) {
      subjectIDList.push(subject.id);
    }

    return this.http.put(`${this.userUrl}/${user.id}`,
      JSON.stringify({
        password: password,
        name: user.name,
        college_id: user.college.id,
        subject_ids: subjectIDList
      }),
      {headers: headerWithCSRF()})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  setLoginedUser(user: User): void {
    UserService.loginedUser = user;
  }

  getLoginedUser(): Promise<User> {
    return this.http.request('/api/loginedUser')
      .toPromise()
      .then(response => response.json() as User)
      .catch(this.handleError);
  }

  getFBProfile(user_id: number): Promise<UserFB> {
    const url = `/api/fb_profile/${user_id}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as UserFB)
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
