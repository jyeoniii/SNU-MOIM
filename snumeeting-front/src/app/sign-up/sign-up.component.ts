import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

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
    private userService: UserService,
    private router: Router
  ) { }

  selectedCollege: College;
  colleges: College[];
  subjects: Subject[];
  interests: string[];
  interestChecked = [];
  subjectChecked = [];

  ngOnInit() {
    this.userService.getCollegeList().then(colleges => this.colleges = colleges);
    this.userService.getSubjectList().then(subjects => this.subjects = subjects);
    this.userService.getInterestList().then(interests => this.interests = interests);
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
