import { TestBed, async, inject } from '@angular/core/testing';
import { MockBackend, MockConnection } from '@angular/http/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';

import { User } from '../models/user';

import { UserService } from './user.service';

import { makeUserData } from '../models/mock-data';

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

  describe('when check user', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = makeUserData();

    }));

    it('should check if user doesn\'t exist',
      async(inject([], () => {
        let response = new Response(new ResponseOptions({status: 200}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.checkUser('no').then(result => expect(result).toBe(true));
      })));
  });

  describe('when signIn', () => {
    let backend: MockBackend;
    let service: UserService;
    let fakeUsers: User[];
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new UserService(http);
      fakeUsers = makeUserData();
    }));

    it('should get user data when user info is right',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 200, body: fakeUsers[0]}));
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
      fakeUsers = makeUserData();
    }));

    it('should get signed up',
      async(inject([], () => {
        response = new Response(new ResponseOptions({status: 201, body: {}}));
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.signUp(fakeUsers[0], '1234').then(response => expect(response).toBeNull());
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
      fakeUsers = makeUserData();
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
      fakeUsers = makeUserData();
      response = new Response(new ResponseOptions({status: 200, body: fakeUsers[1]}));

    }));

    it('should get user info',
      async(inject([], () => {
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        let fakeUser = fakeUsers.find(user => user.id === 2);
        service.getUserInfo(1).then(response => expect(response).toBe(fakeUser));
      })));

    it('should raise an error if user doesn\'t exist',
      async(inject([], () => {
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getUserInfo(-1).then(reason => expect(reason).not.toBeUndefined());
      })));

    it('should be able to edit user info',
      async(inject([], () => {
        backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        let fakeUser = fakeUsers.find(user => user.id === 2);
        fakeUser.name = 'swpp';
        service.editUserInfo(fakeUser, '1234').then(response => {
          expect(response).toBeNull;
          expect(fakeUser.name).toBe('swpp');
        });
      })));
  });


});

