import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { User } from '../user';
import { UserService } from '../user.service';

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
    this.route.params.subscribe(params => {
      this.userService.getUserInfo(+params['id']).then(user => this.user = user);
    });

    this.loginedUser = this.userService.loginedUser;
  }

  editProfile() {
    this.router.navigate(['/user', this.user.id, 'edit']);
  }

}
