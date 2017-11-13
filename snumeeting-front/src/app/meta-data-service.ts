import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { College } from './college';
import { Subject } from './subject';
import { Interest } from './interest';

@Injectable()
export class MetaDataService {

  private collegeUrl = '/api/college';
  private interestUrl = '/api/interest';
  private subjectUrl = '/api/subject';

  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) {
  }

  getCollegeList(): Promise<College[]> {
    return this.http.get(this.collegeUrl)
      .toPromise()
      .then(response => response.json() as College[])
      .catch(this.handleError);
  }

  getInterestList(): Promise<Interest[]> {
    return this.http.get(this.interestUrl)
      .toPromise()
      .then(response => response.json() as Interest[])
      .catch(this.handleError);
  }

  getSubjectList(): Promise<Subject[]> {
    return this.http.get(this.subjectUrl)
      .toPromise()
      .then(response => response.json() as Subject[])
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }

}
