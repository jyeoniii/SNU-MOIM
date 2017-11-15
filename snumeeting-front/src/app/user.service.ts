import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { User } from './user';

@Injectable()
export class UserService {
  private userUrl = '/api/user';

  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) {
  }

  user: User = new User();
  loginedUser: User = new User();

  signIn(username: string, password: string): Promise<User> {
    return this.http.post('/api/signin', JSON.stringify({username: username, password: password}),
      {headers: this.headers})
      .toPromise()
      .then(response => response.json() as User, () => null)
      .catch(this.handleError);
  }

  signUp(user: User): Promise<void> {
    var subjectIDList: number[] = [];
    for (let subject of user.subjects) {
      subjectIDList.push(subject.id);
    }

    return this.http.post('/api/signup', JSON.stringify({
        username: user.username,
        password: user.password,
        name: user.name,
        college_id: user.college.id,
        subject_ids: subjectIDList
      }),
      {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  signOut(): Promise<void> {
    // call this.loginedUser = new User() with then of this function
    return this.http.get('/api/signout', {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  getUserInfo(id: number): Promise<User> {
    return this.http.get(`${this.userUrl}/${id}`)
      .toPromise()
      .then(response => response.json() as User)
      .catch(this.handleError);
  }

  editUserInfo(user: User): Promise<void> {
    var subjectIDList: number[] = [];
    for (let subject of user.subjects) {
      subjectIDList.push(subject.id);
    }

    return this.http.put(`${this.userUrl}/${user.id}`, JSON.stringify({
        password: user.password,
        name: user.name,
        college_id: user.college.id,
        subject_ids: subjectIDList
      }),
      {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
