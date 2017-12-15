import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';

import { TagSearchComponent } from './tag-search.component';

import { MeetingService } from '../services/meeting.service';
import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';

describe('TagSearchComponent', () => {
  let component: TagSearchComponent;
  let fixture: ComponentFixture<TagSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpModule,
        FormsModule,
        NgxPaginationModule,
      ],
      declarations: [ TagSearchComponent ],
      providers: [
        MeetingService,
        UserService,
        MetaDataService,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TagSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
