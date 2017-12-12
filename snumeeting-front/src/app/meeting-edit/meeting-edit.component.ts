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
  selector: 'app-meeting-edit',
  templateUrl: './meeting-edit.component.html',
  styleUrls: ['./meeting-edit.component.css']
})
export class MeetingEditComponent implements OnInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private meetingService: MeetingService,
    private metaDataService: MetaDataService
  ) { }

  subjects: Subject[];
  interests: Interest[];
  selectedMeeting: Meeting;
  selectedSubject: Subject;
  selectedInterest: Interest;
  currentUser: User;
  interestChecked = [];
  subjectChecked = [];
  author: User;

  allTags: string[];
  tagInputs = [];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.meetingService.getMeeting(+params['id']).then(meeting => {
        this.selectedMeeting = meeting;
        this.selectedSubject = meeting.subject;
        for (const tag of meeting.tags){
          this.tagInputs.push(tag.name);
        }
      });
    })
    this.userService.getLoginedUser().then(user => this.currentUser = user);
    this.metaDataService.getSubjectList().then(subjects => this.subjects = subjects);
    this.metaDataService.getInterestList().then(interests => this.interests=interests);
  }

  signOut(): void {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']))
  }

  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  interestCheck(interest: string) {
    if (this.interestChecked[interest]) {
      this.interestChecked[interest] = false;
    } else {
      this.interestChecked[interest] = true;
    }
  }

  subjectCheck(subject: Subject) {
    if (this.subjectChecked[subject.name]) {
      this.subjectChecked[subject.name] = false;
    } else {
      this.subjectChecked[subject.name] = true;
      this.selectedSubject.name = subject.name;
      this.selectedSubject.id = subject.id;
    }
  }

  toEdit(): void {
    // console.log(this.selectedMeeting.title);
    // console.log(this.selectedMeeting.location);
    // console.log(this.selectedMeeting.description);
    // console.log(this.selectedMeeting.max_member);
    // console.log(this.selectedMeeting.subject.name);
    // console.log(this.selectedMeeting.subject.id);

    const tag_names = this.convertTagInputs();
    console.log(tag_names);

    this.meetingService.editMeeting(this.selectedMeeting, tag_names)
     .then(() => {
     alert('Successfully edited the MO-IM!')
       this.router.navigate(['/meeting', this.selectedMeeting.id]);
     });
  }

  convertTagInputs(): string[] {
    const res = [];

    for (const tag of this.tagInputs){
      if (tag.hasOwnProperty('value')) {
        res.push(tag.value);
      } else {
        res.push(tag);
      }

    }

    return res;
  }


}
