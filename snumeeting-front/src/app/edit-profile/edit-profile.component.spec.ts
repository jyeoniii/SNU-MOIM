import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';
import { HttpModule, Http, XHRBackend, Response, ResponseOptions } from '@angular/http';
import { MockBackend, MockConnection } from '@angular/http/testing';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs/Rx';

import { AppModule } from '../app.module';
import { EditProfileComponent } from './edit-profile.component';

import { User } from '../models/user';
import { UserService } from '../services/user.service';
import { makeUserData, makeCollegeData, makeSubjectData, makeInterestData } from '../models/mock-data';

describe('EditProfileComponent', () => {
  let component: EditProfileComponent;
  let fixture: ComponentFixture<EditProfileComponent>;

  let backend: MockBackend;
  let fakeUsers: User[];
  let userService: UserService;
  let response: Response;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppModule,
        HttpModule
      ],
      providers: [
        UserService,
        {
          provide: XHRBackend,
          useClass: MockBackend
        },
        { provide: ActivatedRoute,
          useValue: {'params': Observable.from([{id: 1}])}
        }
      ]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(EditProfileComponent);
        component = fixture.componentInstance;
      });
  }));

  beforeEach(inject([Http, XHRBackend], (http: Http, be: MockBackend) => {
    fixture = TestBed.createComponent(EditProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    backend = be;
    userService = new UserService(http);
    fakeUsers = makeUserData();

    response = new Response(new ResponseOptions({status: 200, body: fakeUsers[1]}));
    backend.connections.subscribe((c: MockConnection) => c.mockRespond(response));
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
