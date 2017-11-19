import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../services/user.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent implements OnInit {

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
  }

  signIn(username: string, password: string) {
    this.userService.signIn(username, password).then(user => {
      if (user !== null) {
        this.userService.setLoginedUser(user);
        this.router.navigate(['/meeting']);
      } else {
        alert('Please check your ID or password.');
      }
    });
  }

  signUp() {
    this.router.navigate(['/sign_up']);
  }

}
