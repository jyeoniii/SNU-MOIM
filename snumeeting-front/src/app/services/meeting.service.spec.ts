import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import {FormsModule} from '@angular/forms';

import { MockBackend, MockConnection } from '@angular/http/testing';

import { MeetingService } from './meeting.service';
import { Meeting } from '../models/meeting';
import { User } from '../models/user';
import { Tag } from '../models/tag';

import { makeMeetingData, makeUserData, makeTagData } from '../models/mock-data';

describe('MeetingService', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpModule,
        RouterTestingModule,
        FormsModule,
      ],
      providers: [MeetingService,
        { provide: XHRBackend, useClass: MockBackend }
      ]
    }).compileComponents();
  }));

  it('should be created', inject([MeetingService], (service: MeetingService) => {
    expect(service).toBeTruthy();
  }));

  it('can initiate service when inject service',
    inject([MeetingService], (service: MeetingService) => {
      expect(service instanceof MeetingService).toBe(true);
    }));

  it('can initiate service with "new"',
    inject([MeetingService], (http: Http) => {
      expect(http).not.toBeNull('http should be provided');
      const service = new MeetingService(http);
      expect(service instanceof MeetingService).toBe(true, 'new service should be ok');
    }));

  it('can provide the mockBackend as XHRBackend', inject([XHRBackend], (backend: MockBackend) => {
    expect(backend).not.toBeNull('backend should be provided');
  }));


  describe('when getMeetings', () => {
    let backend: MockBackend;
    let fakeMeeting: Meeting[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeMeeting = makeMeetingData();
      const options = new ResponseOptions({status: 200, body: fakeMeeting});
      response = new Response(options);
    }));

    it('should have expected fake meetings', async(inject([], () => {
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
      service.getMeetings()
        .then(meetings => {
          console.log(meetings);
          expect(meetings).not.toBeUndefined('returned meetings should not be null');
          expect(meetings.length).toBe(4);
        });
      }))
    );
  });

  describe('when getMeeting', () => {
    it('should have expected fake meeting', async(inject([MeetingService], (service: MeetingService) => {
        service.getMeeting(2)
          .then(meeting => {
            console.log(meeting);
            expect(meeting).not.toBeUndefined('returned meetings should not be null');
            expect(meeting.title).toBe('Mock-title2');
            expect(meeting.author.name).toBe('name2');
            expect(meeting.members.length).toBe(1);
          });
      })));

    it('Should invoke handleError() when an error occured',
      async(inject([MeetingService], (service: MeetingService) => {
        // Invalid article id -> should raise an error
        service.getMeeting(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));

    it('Should invoke handleError() when an error occured while handling data',
      async(inject([MeetingService], (service: MeetingService) => {
        // Invalid article id -> This should raise an error
        service.getMeeting(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));
  });

  describe('when editMeeting / delete meeting', () => {
    let backend: MockBackend;
    let fakeMeeting: Meeting[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeMeeting = makeMeetingData();
      const options = new ResponseOptions({status: 200, body: fakeMeeting});
      response = new Response(options);
    }));

    it('should successfully update backend data', async(inject([MeetingService], (service: MeetingService) => {
      service.getMeeting(3)
        .then(meeting => {
          meeting.title = 'New title';
          service.editMeeting(meeting, []).then(modifiedMeeting => {
            console.log(modifiedMeeting);
            expect(modifiedMeeting.title).toBe('New title');
          });
        });
    })));

    it('should successfully delete selected meeting on backend', async(inject([MeetingService], (service: MeetingService) => {
      service.deleteMeeting(2)
        .then(deletedMeeting => {
          expect(deletedMeeting).toBeNull();
          service.getMeeting(2).catch(reason => expect(reason).not.toBeUndefined());
        });
    })));

  });

  describe('when joinMeeting / leaveMeeting / closeMeeting', () => {
    let backend: MockBackend;
    let fakeMeeting: Meeting[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeMeeting = makeMeetingData();
      const options = new ResponseOptions({status: 200, body: fakeMeeting});
      response = new Response(options);
    }));

    it('joinMeeting should successfully update members of the meeting', async(inject([MeetingService], (service: MeetingService) => {
      const target_meeting = fakeMeeting[0];
      service.joinMeeting(target_meeting.id, 2)
        .then(() => {
          service.getMeeting(target_meeting.id).then(updated => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(updated.members.length).toBe(target_meeting.members.length + 1);
          });
        });
    })));

    it('leaveMeeting should successfully update members of the meeting', async(inject([MeetingService], (service: MeetingService) => {
      const target_meeting = fakeMeeting[0];
      service.leaveMeeting(target_meeting.id, 2)
        .then(() => {
          service.getMeeting(target_meeting.id).then(updated => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(updated.members.length).toBe(target_meeting.members.length - 1);
          });
        });
    })));

    it('closeMeeting should successfully update is_closed', async(inject([MeetingService], (service: MeetingService) => {
      const target_meeting = fakeMeeting[0];
      service.closeMeeting(target_meeting.id)
        .then(() => {
          service.getMeeting(target_meeting.id).then(updated => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(updated.is_closed).toBe(true);
          });
        });
    })));

  });

  describe('when getJoinedMeeting', () => {
    let backend: MockBackend;
    let fakeUser: User[];
    let fakeMeeting: Meeting[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeUser = makeUserData();
      fakeMeeting = makeMeetingData();
      const options = new ResponseOptions({status: 200, body: fakeMeeting});
      response = new Response(options);
    }));

    it('should return expected meetings', async(inject([MeetingService], (service: MeetingService) => {
      service.getJoinedMeeting(2)
        .then(meetings => {
          backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
          expect(meetings.length).toBe(2);
        });
    })));

  });

  describe('when getMeetingsOnTag', () => {
    let backend: MockBackend;
    let fakeTag: Tag[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeTag = makeTagData();
    }));

    it('should get meetings related to the tag', async(inject([MeetingService], (service: MeetingService) => {
      const options = new ResponseOptions({status: 200, body: fakeTag});
      response = new Response(options);
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
      service.getMeetingsOnTag('study')
        .then(meetings => {
          expect(meetings.length).toBe(2);
        });
    })));

    // it('should return empty array when the tag does not exists', async(inject([MeetingService], (service: MeetingService) => {
    //   const options = new ResponseOptions({status: 404, body: fakeTag});
    //   response = new Response(options);
    //   backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
    //   service.getMeetingsOnTag('nonexisting')
    //     .then(response => {
    //       expect(response).toBe(0);
    //     });
    // })));

  });

  describe('when test searching', () => {
    let backend: MockBackend;
    let fakeUser: User[];
    let fakeMeeting: Meeting[];
    let service: MeetingService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MeetingService(http);
      fakeUser = makeUserData();
      fakeMeeting = makeMeetingData();
      const options = new ResponseOptions({status: 200, body: fakeMeeting});
      response = new Response(options);
    }));

    it('searchMeetingsOfTitle should return expected meetings', async(inject([MeetingService],
      (service: MeetingService) => {
        service.searchMeetingsOfTitle('1')
          .then(meetings => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(meetings.length).toBe(1);
          });
      })));

    it('searchMeetingsOfAuthor should return expected meetings', async(inject([MeetingService],
      (service: MeetingService) => {
        service.searchMeetingsOfAuthor('2')
          .then(meetings => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(meetings.length).toBe(1);
          });
      })));

    it('searchMeetingsOfSubject should return expected meetings(subject id only)', async(inject([MeetingService],
      (service: MeetingService) => {
        service.searchMeetingsOfSubject('3')
          .then(meetings => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(meetings.length).toBe(2);
          });
      })));

    it('searchMeetingsOfSubject should return expected meetings(subject id and title)', async(inject([MeetingService],
      (service: MeetingService) => {
        service.searchMeetingsOfSubject('3_an')
          .then(meetings => {
            backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
            expect(meetings.length).toBe(1);
          });
      })));
  });


});


