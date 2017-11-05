import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { User } from './user';
import { College } from './college';
import { Subject } from './subject';

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
      .then(response => response.json() as User)
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

  getCollegeList(): Promise<College[]> {
    return this.http.get('/api/college')
      .toPromise()
      .then(response => response.json() as College[])
      .catch(this.handleError);
  }

  getInterestList(): Promise<string[]> {
    return this.http.get('/api/interest')
      .toPromise()
      .then(response => response.json() as string[])
      .catch(this.handleError);
  }

  getSubjectList(): Promise<Subject[]> {
    return this.http.get('/api/subject')
      .toPromise()
      .then(response => response.json() as Subject[])
      .catch(this.handleError);
  }


  /*
  signOut() {
    this.loginedUser.signed_in = false;

    this.http.put(`${this.userUrl}/${this.loginedUser.id}`, JSON.stringify(this.loginedUser))
      .toPromise()
      .then(() => null)
      .catch(this.handleError);

    this.loginedUser = new User();
  }

  getUserInfo(): Promise<User[]> {
    return this.http.get(this.articleUrl)
      .toPromise()
      .then(response => response.json().data as Article[])
      .catch(this.handleError);
  }

  getArticle(id: number): Promise<Article> {
    return this.http.get(`${this.articleUrl}/${id}`)
      .toPromise()
      .then(response => response.json().data as Article)
      .catch(this.handleError);
  }

  signUp(user: User): Promise<User> {
    return this.http.post(this.articleUrl, JSON.stringify({
      title: article.title,
      content: article.content,
      author_id: article.author_id}), {headers: this.headers})
      .toPromise()
      .then(response => response.json().data as Article)
      .catch(this.handleError);
  }

  editArticle(article: Article): Promise<Article> {
    return this.http.put(`${this.articleUrl}/${article.id}`,
      JSON.stringify(article), {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  deleteArticle(id: number): Promise<void> {
    return this.http.delete(`${this.articleUrl}/${id}`, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  getComments(): Promise<Comment[]> {
    return this.http.get(this.commentUrl)
      .toPromise()
      .then(response => response.json().data as Comment[])
      .catch(this.handleError);
  }

  getComment(id: number): Promise<Comment> {
    return this.http.get(`${this.commentUrl}/${id}`)
      .toPromise()
      .then(response => response.json().data as Comment)
      .catch(this.handleError);
  }

  createComment(comment: Comment): Promise<Comment> {
    return this.http.post(this.commentUrl, JSON.stringify({
      content: comment.content,
      article_id: comment.article_id,
      author_id: comment.author_id}), {headers: this.headers})
      .toPromise()
      .then(response => response.json().data as Comment)
      .catch(this.handleError);
  }

  editComment(comment: Comment): Promise<Comment> {
    return this.http.put(`${this.commentUrl}/${comment.id}`,
      JSON.stringify(comment), {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  deleteComment(id: number): Promise<void> {
    return this.http.delete(`${this.commentUrl}/${id}`, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  getUsers() {
    this.http.get(this.userUrl)
      .toPromise()
      .then(response => this.users = response.json().data as User[])
      .catch(this.handleError);
  }
*/



  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
