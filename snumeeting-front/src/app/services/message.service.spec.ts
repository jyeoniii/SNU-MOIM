import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import {FormsModule} from '@angular/forms';

import { MockBackend, MockConnection } from '@angular/http/testing';

import { MessageService } from './message.service';
import { Message } from '../models/message';

import { makeMessageData } from '../models/mock-data';

describe('MessageService', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpModule,
        RouterTestingModule,
        FormsModule,
      ],
      providers: [MessageService,
        { provide: XHRBackend, useClass: MockBackend }
      ]
    }).compileComponents();
  }));

  it('should be created', inject([MessageService], (service: MessageService) => {
    expect(service).toBeTruthy();
  }));

  it('can initiate service when inject service',
    inject([MessageService], (service: MessageService) => {
      expect(service instanceof MessageService).toBe(true);
    }));

  it('can initiate service with "new"',
    inject([MessageService], (http: Http) => {
      expect(http).not.toBeNull('http should be provided');
      const service = new MessageService(http);
      expect(service instanceof MessageService).toBe(true, 'new service should be ok');
    }));

  it('can provide the mockBackend as XHRBackend', inject([XHRBackend], (backend: MockBackend) => {
    expect(backend).not.toBeNull('backend should be provided');
  }));

  describe('when getMessages', () => {
    let backend: MockBackend;
    let fakeMessage: Message[];
    let service: MessageService;
    let response: Response;

    beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
      backend = be;
      service = new MessageService(http);
      fakeMessage = makeMessageData();
      const options = new ResponseOptions({status: 200, body: fakeMessage});
      response = new Response(options);
    }));

    it('should have expected fake messages', async(inject([], () => {
      backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
      service.getMessages()
        .then(messages => {
          console.log(messages);
          expect(messages).not.toBeUndefined('returned messages should not be null');
          expect(messages.length).toBe(6);
        });
      }))
    );
  });

  /*
  describe('when getMessage', () => {
    it('should have expected fake message', async(inject([MessageService], (service: MessageService) => {
        service.getMessage(2)
          .then(message => {
            console.log(message);
            expect(message).not.toBeUndefined('returned meetings should not be null');
            expect(message.sender.name).toBe('name2');
            expect(message.receiver.name).toBe('name1');
            expect(message.content).toBe('Ok, bye');
            expect(message.sended_at).toBe('2017-11-15T01:35:06Z');
          });
      })));

    it('Should invoke handleError() when an error occured',
      async(inject([MessageService], (service: MessageService) => {
        // Invalid message id -> should raise an error
        service.getMessage(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));

    it('Should invoke handleError() when an error occured while handling data',
      async(inject([MessageService], (service: MessageService) => {
        // Invalid message id -> This should raise an error
        service.getMessage(-1).catch(reason => expect(reason).not.toBeUndefined());
      })));
  });
  */
});


