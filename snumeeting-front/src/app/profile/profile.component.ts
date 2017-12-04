import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { User } from '../models/user';
import { UserService } from '../services/user.service';

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
  notConnectedtoFB: boolean;

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.userService.getUserInfo(+params['id']).then(user => this.user = user);
    });

    this.userService.getLoginedUser()
      .then(user => this.loginedUser = user);

    this.userService.checkFBaccount().then(connected => this.notConnectedtoFB = !connected);
  }

  editProfile() {
    this.router.navigate(['/user', this.user.id, 'edit']);
  }

  signOut() {
    this.userService.signOut();
    this.router.navigate(['/']);
  }

  canEdit(): boolean {
    if (this.loginedUser && this.user) {
      return this.loginedUser.id === this.user.id;
    } else {
      // No user logged in
      return false;
    }
  }

  sendMessage() {
    this.router.navigate(['/user', this.loginedUser.id, 'message']);
  }
}
