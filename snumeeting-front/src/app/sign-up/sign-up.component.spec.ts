import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';
import { MockBackend, MockConnection } from '@angular/http/testing';
import { Http, XHRBackend, Response, ResponseOptions } from '@angular/http';

import { AppModule } from '../app.module';
import { UserService } from '../user.service';
import { SignUpComponent } from './sign-up.component';

describe('SignUpComponent', () => {
  let component: SignUpComponent;
  let fixture: ComponentFixture<SignUpComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [AppModule],
      providers: [
        UserService,
        {
          provide: XHRBackend,
          useClass: MockBackend
        }]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(SignUpComponent);
        component = fixture.componentInstance;
      });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SignUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
