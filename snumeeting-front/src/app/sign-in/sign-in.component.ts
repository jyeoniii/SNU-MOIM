import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../user.service';

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
      if (user.id > 0) {
        this.userService.loginedUser = user;
        this.router.navigate(['/user/', user.id]);
      } else {
        alert('Please check your ID or password.');
      }
    });
  }

  signUp() {
    this.router.navigate(['/sign_up']);
  }

}
