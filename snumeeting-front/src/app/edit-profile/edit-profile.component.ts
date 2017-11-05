import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { User } from '../user';
import { College } from '../college';
import { Subject } from '../subject';

import { UserService } from '../user-service';


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

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) => this.userService.getUserInfo(+params.get('id')))
      .subscribe(user => this.user = user);

    this.userService.getCollegeList().then(colleges => this.colleges = colleges);
  }

  editProfile() {
    console.log('edit profile');
  }
}
