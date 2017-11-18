import { TestBed, inject, async } from '@angular/core/testing';
import { MockBackend, MockConnection } from '@angular/http/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';

import { MetaDataService } from './meta-data-service';

import { College } from '../models/college';
import { Interest } from '../models/interest';
import { Subject } from '../models/subject';

import { makeCollegeData, makeSubjectData, makeInterestData, makeUserData } from '../models/mock-data';

describe('MetaDataServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpModule],
      providers: [MetaDataService,
        {
          provide: XHRBackend,
          useClass: MockBackend
        }]
    });
  });

  it('should be created', inject([MetaDataService], (service: MetaDataService) => {
    expect(service).toBeTruthy();
  }));


  describe('when getting lists of data', () => {
    let backend: MockBackend;
    let service: MetaDataService;
    let fakeColleges: College[];
    let fakeSubjects: Subject[];
    let fakeInterests: Interest[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MetaDataService(http);
      fakeColleges = makeCollegeData();
      fakeSubjects = makeSubjectData();
      fakeInterests = makeInterestData();
    }));

    it('should get college data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeColleges}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getCollegeList().then(colleges => expect(colleges.length).toBe(2));
      })));

    it('should get subject data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeSubjects}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getSubjectList().then(subjects => expect(subjects.length).toBe(3));
      })));

    it('should get interest data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeInterests}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getInterestList().then(interests => expect(interests.length).toBe(2));
      })));
  });
});
