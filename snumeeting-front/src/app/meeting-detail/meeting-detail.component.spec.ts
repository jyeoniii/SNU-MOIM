import { async, inject, ComponentFixture, TestBed } from '@angular/core/testing';

import { MeetingDetailComponent } from './meeting-detail.component';
import {RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';

import { MeetingService } from '../meeting.service';
import { CommentService } from '../comment.service';

import { Meeting } from '../meeting';

import { MockBackend } from '@angular/http/testing';

import { makeMeetingData } from '../mock-data';

describe('MeetingDetailComponent', () => {
  let component: MeetingDetailComponent;
  let fixture: ComponentFixture<MeetingDetailComponent>;

  let backend: MockBackend;
  let fakeMeeting: Meeting[];
  let service: MeetingService;
  let response: Response;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ RouterTestingModule,
                 HttpModule,
                 FormsModule,
      ],
      declarations: [ MeetingDetailComponent],
      providers: [MeetingService, CommentService,
        { provide: XHRBackend, useClass: MockBackend },
        { provide: ActivatedRoute, useValue: { 'params': Observable.from([{ id: 1 }]) } },
      ]
    })
    .compileComponents();
  }));

  beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
    fixture = TestBed.createComponent(MeetingDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    backend = be;
    service = new MeetingService(http);
    fakeMeeting = makeMeetingData();
    const options = new ResponseOptions({status: 200, body: fakeMeeting});
    response = new Response(options);
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });



});
