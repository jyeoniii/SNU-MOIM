import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { User } from '../models/user';
import { College } from '../models/college';
import { Subject } from '../models/subject';
import { Interest } from '../models/interest';

import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';


@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent implements OnInit {

  constructor(
    private router: Router,
    private metaDataService: MetaDataService,
    private route: ActivatedRoute,
    private userService: UserService
  ) { }

  loginedUser: User;
  user: User;
  colleges: College[];
  subjects: Subject[];
  interests: Interest[];
  interestChecked = [];
  subjectChecked = [];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.userService.getUserInfo(+params['id']).then(user => {
        this.user = user;
        if(user == null) {
          this.router.navigate(['/404']);
        }
        for (const subject of user.subjects) {
          this.subjectChecked[subject.name] = true;
          this.interestChecked[subject.interest_id] = true;
        }
      });
    });
    this.userService.getLoginedUser().then(user => {
      this.loginedUser = user;
      if (!this.loginedUser) {
        this.router.navigate(['/signin_first']);
      }

      if (this.loginedUser.id !== this.user.id) {
        this.router.navigate(['/user', this.loginedUser.id, 'edit']);
      }
    });

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

  goBack(): void {
    this.router.navigate(['/user', this.user.id]);
  }


  editProfile(password: string, passwordCheck: string, name: string) {
    if (this.loginedUser.id !== this.user.id) {
      alert('Are you trying to edit the profile of another user?');
      this.router.navigate(['/user/' + this.loginedUser.id + '/edit']);
      return;
    }

    if (password === '') {
      alert('Please enter a new password!');
      return;
    }

    if (name === '') {
      alert('Please enter your new name!');
      return;
    }

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

    if (password === passwordCheck) {
      this.user.name = name;
      this.user.subjects = selectedSubjects;

      this.userService.editUserInfo(this.user, password).then(() => {
        alert('Edit Profile Success!')
        this.router.navigate(['/user', this.user.id]);
      });
    } else {
      alert('Password and Check doesn\'t match.');
    }
  }

  signOut() {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']));
  }
}
