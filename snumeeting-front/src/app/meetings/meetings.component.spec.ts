import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { PaginationDirective } from '../../../node_modules/angular2-bootstrap-pagination/directives/pagination.directive';

import { MeetingsComponent } from './meetings.component';
import {MeetingService} from '../meeting.service';
import {MetaDataService} from '../meta-data-service';
import {UserService} from '../user.service';

describe('MeetingsComponent', () => {
  let component: MeetingsComponent;
  let fixture: ComponentFixture<MeetingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpModule,
        FormsModule,
      ],
      declarations: [
        MeetingsComponent,
        PaginationDirective,
      ],
      providers: [
        MeetingService,
        MetaDataService,
        UserService,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MeetingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
