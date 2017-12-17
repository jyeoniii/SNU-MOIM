import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent implements OnInit {

  constructor(
    private userService: UserService,
    private metaDataService: MetaDataService,
    private router: Router
  ) {}

  ngOnInit() {
    this.showMessageAlert();

    this.userService.getLoginedUser()
      .then(user => {
        if (user) {
          this.router.navigate(['/meeting']);
        }
      });
  }

  showMessageAlert() {
    this.metaDataService.getMessage().then(response => {
      if (response.status === 200) {
        alert(response.json()['message']);
      }
    });
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
