import { async, ComponentFixture, inject, TestBed } from '@angular/core/testing';

import { MeetingEditComponent } from './meeting-edit.component';

import { RouterTestingModule } from '@angular/router/testing';

import { FormsModule } from "@angular/forms";
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from "@angular/http";
import { Observable } from 'rxjs/Rx';
import { ActivatedRoute } from "@angular/router";

import { MeetingService } from "../services/meeting.service";
import { UserService } from "../services/user.service";

import { Meeting } from "../models/meeting";

import { MockBackend, MockConnection } from "@angular/http/testing";
import { makeMeetingData } from "../models/mock-data";
import { MetaDataService } from '../services/meta-data-service';

import { TagInputModule } from 'ngx-chips';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('MeetingEditComponent', () => {
  let component: MeetingEditComponent;
  let fixture: ComponentFixture<MeetingEditComponent>;

  let backEnd: MockBackend;
  let fakeMeeting: Meeting[];
  let meetingService: MeetingService;
  let response: Response;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpModule,
        FormsModule,
        TagInputModule,
        BrowserAnimationsModule,
      ],
      declarations: [MeetingEditComponent],
      providers: [
        MeetingService, UserService, MetaDataService,
        { provide: XHRBackend, useClass: MockBackend },
        { provide: ActivatedRoute, useValue: {'params': Observable.from([{id: 1}])}},
      ]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(MeetingEditComponent);
        component = fixture.componentInstance;
      });
  }));

  beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
    fixture = TestBed.createComponent(MeetingEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    backEnd = be;
    meetingService = new MeetingService(http);
    fakeMeeting = makeMeetingData();

    response = new Response(new ResponseOptions({status: 200, body: fakeMeeting[1]}));
    backEnd.connections.subscribe((c: MockConnection) => c.mockRespond(response));
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
