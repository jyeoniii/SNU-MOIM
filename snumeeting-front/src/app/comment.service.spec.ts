import { TestBed, async, inject } from '@angular/core/testing';
import { HttpModule, Http } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import {FormsModule} from '@angular/forms';

import { InMemoryDataService } from './in-memory-data.service';
import { InMemoryWebApiModule } from 'angular-in-memory-web-api';

import { CommentService } from './comment.service';

describe('CommentService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpModule,
        RouterTestingModule,
        FormsModule,
        InMemoryWebApiModule.forRoot(InMemoryDataService, { delay: 0 }),
      ],
      providers: [CommentService]
    });
  });

  it('should be created', inject([CommentService], (service: CommentService) => {
    expect(service).toBeTruthy();
  }));

  it('can initiate service when inject service',
    inject([CommentService], (service: CommentService) => {
      expect(service instanceof CommentService).toBe(true);
    }));

  it('can initiate service with "new"',
    inject([CommentService], (http: Http) => {
      expect(http).not.toBeNull('http should be provided');
      const service = new CommentService(http);
      expect(service instanceof CommentService).toBe(true, 'new service should be ok');
    }));

  it('Should invoke handleError() when an error occured while handling data',
    async(inject([CommentService], (service: CommentService) => {
      // Invalid article id -> This should raise an error
      service.getComment(-1).catch(reason => expect(reason).not.toBeUndefined());
    })));


  describe('when getCommentsOnMeeting', () => {
    it('should have expected fake comments', async(inject([CommentService], (service: CommentService) => {
        service.getCommentsOnMeeting(2)
          .then(comments => {
            console.log(comments);
            expect(comments).not.toBeUndefined('returned comments should not be null');
            expect(comments.length).toBe(2);
          });
      }))
    );

    it('should be ok returning no comments', async(inject([CommentService], (service: CommentService) => {
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
    it('should have expected fake meeting', async(inject([CommentService], (service: CommentService) => {
      service.getComment(2)
        .then(comment => {
          console.log(comment);
          expect(comment).not.toBeUndefined('returned comments should not be null');
          expect(comment.content).toBe('Hello');
          expect(comment.author.name).toBe('name');
          expect(comment.meeting.id).toBe(2);
        });
    })));

    it('Should invoke handleError() when an error occured',
      async(inject([CommentService], (service: CommentService) => {
        // Invalid article id -> should raise an error
        service.getComment(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));
  });

  describe('when ediComment', () => {
    it('should successfully update backend data', async(inject([CommentService], (service: CommentService) => {
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
    it('should successfully delete selected comment on backend', async(inject([CommentService], (service: CommentService) => {
      service.deleteComment(2)
        .then(deletedMeeting => {
          expect(deletedMeeting).toBeNull();
          service.getComment(2).catch(reason => expect(reason).not.toBeUndefined());
        });
    })));
  });

});
