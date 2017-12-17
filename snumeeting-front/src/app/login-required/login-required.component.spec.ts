import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { AppModule } from '../app.module';
import { LoginRequiredComponent } from './login-required.component';

describe('LoginRequiredComponent', () => {
  let component: LoginRequiredComponent;
  let fixture: ComponentFixture<LoginRequiredComponent>;

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
    }).compileComponents().then(() => {
      fixture = TestBed.createComponent(LoginRequiredComponent);
      component = fixture.componentInstance;
    });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginRequiredComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should navigate to sign in page', () => {
    component.signIn();
    expect(routerStub.navigate).toHaveBeenCalledWith(['/sign_in']);
  });
});
