import { Component, OnInit } from '@angular/core';

import { User } from '../user';
import { College } from '../college';
import { Subject } from '../subject';

import { UserService } from '../user-service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  constructor(
    private userService: UserService
  ) { }

  ngOnInit() {
    this.userService.getCollegeList().then(colleges => this.colleges = colleges);
  }

  colleges: College[];
  subjects: Subject[];

  signUp() {
    console.log('sign up');
  }
}
