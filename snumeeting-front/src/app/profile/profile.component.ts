import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { User } from '../models/user';
import { UserService } from '../services/user.service';
import { UserFB } from '../models/userFB';
import { Meeting } from '../models/meeting';
import {MeetingService} from "../services/meeting.service";

enum Status {
  Self = 0,
  Friend = 1,
  ShowMutual = 2,
  LoginUserNoFB = 3,
  ProfileUserNoFB = 4,
  NoOneLoggedIn = 5,
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private meetingService: MeetingService,
  ) { }

  user: User;
  loginedUser: User;
  mutualFriends: UserFB[] = [];
  status: Status;

  FBprofile: UserFB;
  joinedMeetings: Meeting[];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.userService.getUserInfo(+params['id']).then(user => {
          this.user = user;
          if(user == null) {
            this.router.navigate(['/404']);
          }
          this.setStatus();
          this.meetingService.getJoinedMeeting(this.user.id)
            .then(meetings => {
              this.joinedMeetings = meetings;
            });
        }
      );
    });

    this.userService.getLoginedUser()
      .then(user => {
        this.loginedUser = user;
        if (this.loginedUser) {
          this.setStatus();
        } else {
          this.router.navigate(['/signin_first']);
        }
      });
  }

  editProfile() {
    this.router.navigate(['/user', this.user.id, 'edit']);
  }

  connectToFacebook() {
    window.location.href = '/oauth/login/facebook/';
  }

  signOut() {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']));
  }

  canEdit(): boolean {
    if (this.loginedUser && this.user) {
      return this.loginedUser.id === this.user.id;
    } else {
      // No user logged in
      return false;
    }
  }

  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  setStatus(): void {
    if (this.loginedUser && this.user) {
      if (this.loginedUser.id === this.user.id) {   // Self
        this.status = Status.Self;
        if (this.loginedUser.fb_connected) {
          this.userService.getFBProfile(this.loginedUser.id)
            .then(profile => {
              this.FBprofile = profile;
            });
        }
      } else {
        if (!this.loginedUser.fb_connected) {
          this.status = Status.LoginUserNoFB;
          if (this.user.fb_connected) {
            this.userService.getFBProfile(this.user.id)
              .then(profile => {
                this.FBprofile = profile;
              });
          }
        } else if (!this.user.fb_connected) {
          this.status = Status.ProfileUserNoFB;
        } else {
          this.userService.getFBProfile(this.user.id)
            .then(profile => {
              this.FBprofile = profile;
            });
          this.status = Status.ShowMutual;
          for (const friend of this.loginedUser.fb_friends) {
            if (friend.id === this.user.id) {
              this.status = Status.Friend;
              break;
            }
          }

          if (this.status === Status.ShowMutual) {
            this.getMutualFriends();
          }
        }
      }
    } else {
      this.status = Status.NoOneLoggedIn;
    }

    console.log(this.status);
  }

  getMutualFriends(): void {
    // Doesn't work:
    // return this.loginedUser.fb_friends.filter(e => this.user.fb_friends.includes(e));

    for (const loginedUserFriend of this.loginedUser.fb_friends) {
      for (const profileUserFriend of this.user.fb_friends) {
        if (loginedUserFriend.id === profileUserFriend.id) {
          this.userService.getFBProfile(loginedUserFriend.id)
            .then(FBprofile => this.mutualFriends.push(FBprofile));
          break;
        }
      }
    }
  }

  sendMessage() {
    this.router.navigate(['/user', this.loginedUser.id, 'message']);
  }
}
