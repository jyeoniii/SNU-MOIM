import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';


import { AppModule } from '../app.module';
import { SignInComponent } from './sign-in.component';

describe('SignInComponent', () => {
  let component: SignInComponent;
  let fixture: ComponentFixture<SignInComponent>;

  let routerStub;

  beforeEach(async(() => {
    routerStub = {
      navigate: jasmine.createSpy('navigate')
    };

    TestBed.configureTestingModule({
      imports: [AppModule],
      providers: [
        {
          provide: Router,
          useValue: routerStub
        }
      ]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(SignInComponent);
        component = fixture.componentInstance;
      });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SignInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
