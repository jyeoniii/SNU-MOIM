import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { User } from '../user';
import { College } from '../college';
import { Subject } from '../subject';

import { UserService } from '../user.service';


@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent implements OnInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService
  ) { }

  user: User;
  colleges: College[];
  subjects: Subject[];
  interests: string[];
  interestChecked = [];
  subjectChecked = [];

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) => this.userService.getUserInfo(+params.get('id')))
      .subscribe(user => this.user = user);

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

  editProfile(password: string, passwordCheck: string, name: string) {
    if (password === passwordCheck) {
      var selectedSubjects: Subject[] = [];

      for (let subject of this.subjects) {
        if (this.subjectChecked[subject.name]) {
          selectedSubjects.push(subject);
        }
      }

      this.user.password = password;
      this.user.name = name;
      this.user.subjects = selectedSubjects;

      this.userService.editUserInfo(this.user).then(() => {
        alert('Edit Profile Success!')
        this.router.navigate(['/user', this.user.id]);
      });
    } else {
      alert('Password and Check doesn\'t match.');
    }
  }
}
