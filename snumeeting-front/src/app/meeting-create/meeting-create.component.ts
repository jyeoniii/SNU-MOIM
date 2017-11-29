import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { UserService } from "../services/user.service";
import { MeetingService } from "../services/meeting.service";

import { User } from '../models/user';
import { Meeting } from '../models/meeting';
import { Subject } from '../models/subject';
import { Interest } from '../models/interest';

import { MetaDataService } from "../services/meta-data-service";

@Component({
  selector: 'app-meeting-create',
  templateUrl: './meeting-create.component.html',
  styleUrls: ['./meeting-create.component.css']
})
export class MeetingCreateComponent implements OnInit {
  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private meetingService: MeetingService,
    private metaDataService: MetaDataService
  ) { }

  subjects: Subject[];
  interests: Interest[];
  meeting: Meeting = new Meeting();
  selectedSubject: Subject;
  selectedInterest: Interest;
  currentUser: User;
  interestChecked = [];
  subjectChecked = [];



  ngOnInit() {
    this.userService.getLoginedUser().then(user => this.currentUser = user);
    this.metaDataService.getSubjectList().then(subjects => this.subjects = subjects);
    this.metaDataService.getInterestList().then(interests => this.interests = interests);
    // this.metaDataService.getMemberList().then(members => this.members = members);
  }

  signOut(): void {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']))
  }

  goBack(): void {
    this.router.navigate(['/meeting'])
  }


  interestCheck(interest: string) {
    if (this.interestChecked[interest]) {
      this.interestChecked[interest] = false;
    } else {
      this.interestChecked[interest] = true;
      // this.selectedInterest = interest;
    }
  }

  subjectCheck(subject: Subject) {
    if (this.subjectChecked[subject.name]) {
      this.subjectChecked[subject.name] = false;
    } else {
      this.subjectChecked[subject.name] = true;
      this.selectedSubject = subject;
    }
  }

  create(): void {

    this.meeting.subject = this.selectedSubject;
    // console.log(this.meeting.subject);

    // console.log(this.meeting.description);

    this.meetingService.createMeeting(
      this.currentUser,
      this.meeting.title,
      this.meeting.subject,
      this.meeting.description,
      this.meeting.location,
      this.meeting.max_member
    )
      .then(() => {
        alert('Successfully Created a meeting!');
        this.router.navigate(['/meeting']);
      });
  }
}
