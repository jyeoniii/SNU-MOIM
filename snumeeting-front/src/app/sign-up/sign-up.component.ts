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

  signUp(username: string, password: string, passwordCheck: string, name: string) {
    if (password === passwordCheck) {
      var selectedSubjects: Subject[] = [];

      for (let subject of this.subjects) {
        if (this.subjectChecked[subject.name]) {
          selectedSubjects.push(subject);
        }
      }

      var newUser = new User();
      newUser.username = username;
      newUser.password = password;
      newUser.name = name;
      newUser.college = this.selectedCollege;
      newUser.subjects = selectedSubjects;

      this.userService.signUp(newUser).then(() => {
        alert('Sign Up Success!')
        this.router.navigate(['/sign_in']);
      });
  } else {
    alert('Password and Check doesn\'t match.');
    }
  }

}
