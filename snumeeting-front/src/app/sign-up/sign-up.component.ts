import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { User } from '../models/user';
import { College } from '../models/college';
import { Subject } from '../models/subject';
import { Interest } from '../models/interest';

import { UserService } from '../services/user.service';
import {MetaDataService} from '../services/meta-data-service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})

export class SignUpComponent implements OnInit {

  constructor(
    private metaDataService: MetaDataService,
    private userService: UserService,
    private router: Router
  ) { }

  selectedCollege: College;
  colleges: College[];
  subjects: Subject[];
  interests: Interest[];
  interestChecked = [];
  subjectChecked = [];

  userNotExist = false;

  ngOnInit() {
    this.metaDataService.getCollegeList().then(colleges => this.colleges = colleges);
    this.metaDataService.getSubjectList().then(subjects => this.subjects = subjects);
    this.metaDataService.getInterestList().then(interests => this.interests = interests);
  }

  interestCheck(interest: string) {
    if (this.interestChecked[interest]) {
      this.interestChecked[interest] = false;
    } else {
      this.interestChecked[interest] = true;
    }
  }

  subjectCheck(subjectName: string) {
    if (this.subjectChecked[subjectName]) {
      this.subjectChecked[subjectName] = false;
    } else {
      this.subjectChecked[subjectName] = true;
    }
  }

  checkUser(username: string) {
    if (username === '') {
      alert('Please enter your mySNU ID.');
    } else {
      this.userService.checkUser(username).then(userNotExist => {
        if (userNotExist) {
          alert('You can use this ID.');
          this.userNotExist = true;
        } else {
          alert('This ID is already taken.\n(Maybe you already signed up with our service?)');
          this.userNotExist = false;
        }
      });
    }
  }

  signUp(username: string, password: string, passwordCheck: string, name: string) {
    var selectedSubjects: Subject[] = [];

    for (let subject of this.subjects) {
      if (this.subjectChecked[subject.name]) {
        selectedSubjects.push(subject);
      }
    }

    if (selectedSubjects.length === 0) {
      alert('Please select interests.');
      return;
    }

    if (!this.userNotExist) {
      alert('Please check if your ID exists.');
      return;
    }

    if (username === '' || password === '') {
      alert('Please enter your ID or password.');
      return;
    }

    if (name === '') {
      alert('Please enter your name.');
      return;
    }

    if (!this.selectedCollege) {
      alert('Please select your college.');
      return;
    }

    if (password === passwordCheck) {
      var newUser = new User();
      newUser.username = username;
      newUser.name = name;
      newUser.college = this.selectedCollege;
      newUser.subjects = selectedSubjects;

      this.userService.signUp(newUser, password).then(() => {
        alert('Authentication mail was sent! Please check your mailbox.')
        this.router.navigate(['/sign_in']);
      });
    } else {
      alert('Password and Check doesn\'t match.');
    }
  }

  goBack(): void {
    this.router.navigate(['/sign_in'])
  }

}
