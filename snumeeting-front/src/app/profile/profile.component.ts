import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { User } from '../user';
import { UserService } from '../user.service';

import 'rxjs/add/operator/switchMap';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService
  ) { }

  user: User;
  loginedUser: User;

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) => this.userService.getUserInfo(+params.get('id')))
      .subscribe(user => this.user = user);

    this.loginedUser = this.userService.loginedUser;
  }

  editProfile() {
    this.router.navigate(['/user', this.user.id, 'edit']);
  }

}
