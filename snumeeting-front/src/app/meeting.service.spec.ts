import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule, Http } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import {FormsModule} from '@angular/forms';

import { MeetingService } from './meeting.service';

/*
describe('MeetingService', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpModule,
        RouterTestingModule,
        FormsModule
      ],
      providers: [MeetingService]
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

  it('Should invoke handleError() when an error occured while handling data',
    async(inject([MeetingService], (service: MeetingService) => {
      // Invalid article id -> This should raise an error
      service.getMeeting(-1).catch(reason => expect(reason).not.toBeUndefined());
    })));


  describe('when getMeetings', () => {
    it('should have expected fake meetings', async(inject([MeetingService], (service: MeetingService) => {
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
  });

  describe('when editMeeting', () => {
    it('should successfully update backend data', async(inject([MeetingService], (service: MeetingService) => {
      service.getMeeting(3)
        .then(meeting => {
          meeting.title = 'New title';
          service.editMeeting(meeting).then(modifiedMeeting => {
            console.log(modifiedMeeting);
            expect(modifiedMeeting.title).toBe('New title');
          });
        });
    })));

  });

  describe('when deleteMeeting', () => {
    it('should successfully delete selected meeting on backend', async(inject([MeetingService], (service: MeetingService) => {
      service.deleteMeeting(2)
        .then(deletedMeeting => {
          expect(deletedMeeting).toBeNull();
          service.getMeeting(2).catch(reason => expect(reason).not.toBeUndefined());
        });
    })));

  });
});
*/
