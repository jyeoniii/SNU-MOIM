import { TestBed, async, inject } from '@angular/core/testing';
import { MockBackend, MockConnection } from '@angular/http/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';

import { User } from './user';
import { College } from './college';
import { Subject } from './subject';
import { UserService } from './user.service';

import { collegeData, subjectData, interestData, userData } from './mock.data';

describe('UserService (mockBackend)', () => {
  beforeEach( async(() => {
    TestBed.configureTestingModule({
      imports: [HttpModule],
      providers: [
        UserService,
        {
          provide: XHRBackend,
          useClass: MockBackend
        }]
    }).compileComponents();
  }));

  it('should be created', inject([UserService], (service: UserService) => {
    expect(service).toBeTruthy();
  }));

  it('can initiate service when inject service',
    inject([UserService], (service: UserService) => {
      expect(service instanceof UserService).toBe(true);
    }));

  it('can initiate service with "new"',
    inject([Http], (http: Http) => {
      expect(http).not.toBeNull('http should be provided');
      const service = new UserService(http);
      expect(service instanceof UserService).toBe(true, 'new service should be ok');
    }));

  describe('when signIn', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = userData;
    }));

    it('should get user data when user info is right',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: userData[0]}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.signIn('hello', 'hellohello').then(user => expect(user).not.toBeNull());
      })));

    it('should get null when user info is not right',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 401, body: null}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.signIn('hello', 'hello').then(user => expect(user).toBeNull());
      })));
  });

  describe('when signUp', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = userData;
    }));

    it('should get signed up',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 201, body: {}}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.signUp(fakeUsers[0]).then(response => expect(response).toBeNull());
      })));
  });

  describe('when signOut', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = userData;
    }));

    it('should get signed out',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: {}}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.signOut().then(response => expect(response).toBeNull());
      })));
  });

  describe('when calling user/:id', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = userData;
    }));

    it('should get user info',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeUsers[1]}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        let fakeUser = fakeUsers.find(user => user.id === 2);
        service.getUserInfo(2).then(response => expect(response).toBe(fakeUser));
      })));

    it('should be able to edit user info',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeUsers[1]}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        let fakeUser = fakeUsers.find(user => user.id === 2);
        fakeUser.name = 'swpplove';
        service.editUserInfo(fakeUser).then(response => expect(response).toBeNull);
      })));
  });

  describe('when getting lists of data', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeColleges: College[];
    let fakeSubjects: Subject[];
    let fakeInterests: string[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeColleges = collegeData;
      fakeSubjects = subjectData;
      fakeInterests = interestData;
    }));

    it('should get college data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeColleges}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getCollegeList().then(colleges => expect(colleges.length).toBe(4));
      })));

    it('should get subject data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeSubjects}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getSubjectList().then(subjects => expect(subjects.length).toBe(5));
      })));

    it('should get interest data',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeInterests}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getInterestList().then(interests => expect(interests.length).toBe(3));
      })));
  });
});
/*
    it('should be ok returning no comments', async(inject([UserService], (service: UserService) => {
        service.getCommentsOnMeeting(4)
          .then(comments => {
            console.log(comments);
            expect(comments).not.toBeUndefined('returned comments should not be null');
            expect(comments.length).toBe(0);
          });
      }))
    );
  });

  describe('when getComment', () => {
    it('should have expected fake meeting', async(inject([UserService], (service: UserService) => {
      service.getComment(2)
        .then(comment => {
          console.log(comment);
          expect(comment).not.toBeUndefined('returned comments should not be null');
          expect(comment.content).toBe('Hello');
          expect(comment.author.name).toBe('name');
          expect(comment.meeting_id).toBe(2);
        });
    })));

    it('Should invoke handleError() when an error occured',
      async(inject([UserService], (service: UserService) => {
        // Invalid article id -> should raise an error
        service.getComment(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));
  });

  describe('when ediComment', () => {
    it('should successfully update backend data', async(inject([UserService], (service: UserService) => {
      service.getComment(3)
        .then(comment => {
          comment.content = 'New content';
          service.editComment(comment).then(modifiedComment => {
            console.log(modifiedComment);
            expect(modifiedComment.content).toBe('New content');
          });
        });
    })));

  });

  describe('when deleteComment', () => {
    it('should successfully delete selected comment on backend', async(inject([UserService], (service: UserService) => {
      service.deleteComment(2)
        .then(deletedMeeting => {
          expect(deletedMeeting).toBeNull();
          service.getComment(2).catch(reason => expect(reason).not.toBeUndefined());
        });
    })));
  });
});
*/
