import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppModule } from '../app.module';
import { MeetingCreateComponent } from './meeting-create.component';

describe('MeetingCreateComponent', () => {
  let component: MeetingCreateComponent;
  let fixture: ComponentFixture<MeetingCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [AppModule]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(MeetingCreateComponent);
        component = fixture.componentInstance;
      });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MeetingCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
