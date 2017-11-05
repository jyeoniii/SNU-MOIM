/*
This file is to create the meeting
The following parts will be added later
-User Service
-Meeting Service

 */
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from "@angular/common";

import { User } from "../user";
//import user service
import { Meeting } from "../meeting";
//import meeting service

@Component({
  selector: 'app-meeting-create',
  templateUrl: './meeting-create.component.html',
  styleUrls: ['./meeting-create.component.css']
})
export class MeetingCreateComponent implements OnInit {
  currentUser: User;
  meeting: Meeting;
  isWriting: boolean=false;

  constructor(
    private router: Router,
    private location: Location,

  //  private userService: UserService,
  //  private meetingService: MeetingService
  ) { }

  ngOnInit() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'))
    this.meeting = new Meeting
    this.isWriting = true
  }

  signOut(): void {
  //  this.userService.signOut().then(() => goToSignIn())

  }
  goToSignIn(): void {
    this.router.navigate(['/signin'])
  }
  goBack(): void {
    this.location.back()
  }
  showWritingTab(): void {
    this.isWriting = true
  }
  showPreviewTap(): void {
    this.isWriting = false
  }
  create(): void {
    this.meetingService.create(
      this.meeting.title,
      this.meeting.subject.interest,  //interest b4 subject?
      this.meeting.subject,
      this.meeting.description,
      this.meeting.location,
      this.meeting.members,
      this.meeting.max_member,
      )
      .then(meeting => {
        this.meeting = meeting
        this.goToDetail()
      })

  }
  goToDetail(): void {
    this.router.navigate(['/meeting', this.meeting.id])
  }
}
