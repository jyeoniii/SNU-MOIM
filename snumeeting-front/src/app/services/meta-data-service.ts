import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { College } from '../models/college';
import { Subject } from '../models/subject';
import { Interest } from '../models/interest';
import { Tag } from '../models/tag';

@Injectable()
export class MetaDataService {

  private collegeUrl = '/api/college';
  private interestUrl = '/api/interest';
  private subjectUrl = '/api/subject';
  private messageUrl = '/api/messages';
  private tagUrl = '/api/tags';

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

  getMessage(): Promise<Response> {
    return this.http.get(this.messageUrl)
      .toPromise()
      .then(response => response, () => null)
      .catch(this.handleError);
  }

  getTagNameList(): Promise<string[]> {
    return this.http.get(this.tagUrl)
      .toPromise()
      .then(response => response.json() as string[])
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
