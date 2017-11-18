import { TestBed, async, inject } from '@angular/core/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import {FormsModule} from '@angular/forms';
import { MockBackend, MockConnection } from '@angular/http/testing';

import { CommentService } from './comment.service';
import { makeCommentData } from '../models/mock-data';

import { Comment } from '../models/comment';

describe('CommentService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpModule,
        RouterTestingModule,
        FormsModule,
      ],
      providers: [CommentService,
        { provide: XHRBackend, useClass: MockBackend }
      ]
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

  it('can provide the mockBackend as XHRBackend', inject([XHRBackend], (backend: MockBackend) => {
    expect(backend).not.toBeNull('backend should be provided');
  }));

  describe('when getCommentsOnMeeting', () => {
    let backend: MockBackend;
    let fakeComment: Comment[];
    let response: Response;

    beforeEach(inject([XHRBackend], (be: MockBackend) => {
      backend = be;
      fakeComment = makeCommentData();
    }));

    it('should have expected fake comments', async(inject([CommentService], (service: CommentService) => {
      fakeComment = fakeComment.filter(comment => comment.meeting_id === 2);
      const options = new ResponseOptions({status: 200, body: fakeComment});
      response = new Response(options);
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
        service.getCommentsOnMeeting(2)
          .then(comments => {
            console.log(comments);
            expect(comments).not.toBeUndefined('returned comments should not be null');
            expect(comments.length).toBe(2);
          });
      }))
    );

    it('should be ok returning no comments', async(inject([CommentService], (service: CommentService) => {
      fakeComment = fakeComment.filter(comment => comment.meeting_id === 4);
      const options = new ResponseOptions({status: 200, body: fakeComment});
      response = new Response(options);
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
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
    let backend: MockBackend;
    let fakeComment: Comment[];
    let response: Response;

    beforeEach(inject([XHRBackend], (be: MockBackend) => {
      backend = be;
      fakeComment = makeCommentData();
      const options = new ResponseOptions({status: 200, body: fakeComment[1]});
      response = new Response(options);
    }));

    it('should have expected fake meeting', async(inject([CommentService], (service: CommentService) => {
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
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
      async(inject([CommentService], (service: CommentService) => {
        // Invalid article id -> should raise an error
        service.getComment(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));
  });

  describe('when editComment', () => {
    let backend: MockBackend;
    let fakeComment: Comment[];
    let response: Response;

    beforeEach(inject([XHRBackend], (be: MockBackend) => {
      backend = be;
      fakeComment = makeCommentData();
      const options = new ResponseOptions({status: 200, body: fakeComment});
      response = new Response(options);
    }));

    it('should successfully update backend data', async(inject([CommentService], (service: CommentService) => {
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
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
    let backend: MockBackend;
    let fakeComment: Comment[];
    let response: Response;

    beforeEach(inject([XHRBackend], (be: MockBackend) => {
      backend = be;
      fakeComment = makeCommentData();
      const options = new ResponseOptions({status: 200, body: fakeComment});
      response = new Response(options);
    }));

    it('should successfully delete selected comment on backend', async(inject([CommentService], (service: CommentService) => {
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
      service.deleteComment(2)
        .then(deletedMeeting => {
          expect(deletedMeeting).toBeNull();
          service.getComment(2).catch(reason => expect(reason).not.toBeUndefined());
        });
    })));
  });

});
