import { Component, OnInit, Input } from '@angular/core';
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
  styleUrls: ['./meeting-create.component.css'],
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

  allTags: string[];
  tagInputs = [];
  notice = '';


  ngOnInit() {
    this.userService.getLoginedUser().then(user => {
      this.currentUser = user;
      if (!this.currentUser) {
        this.router.navigate(['/signin_first']);
      }
    });
    this.metaDataService.getSubjectList().then(subjects => this.subjects = subjects);
    this.metaDataService.getInterestList().then(interests => this.interests = interests);
    this.metaDataService.getTagNameList().then(tags => this.allTags = tags);
  }

  signOut(): void {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']));
  }

  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  checkInput(): void {
    if (this.meeting.title==null) {
      this.notice = 'Did you forget a title?';
      console.log('no title');
      return;
    } else if (this.meeting.subject==null) {
      this.notice = 'What about interest?';
      console.log('no interest');
      return;
    } else if (this.meeting.description==null) {
      this.notice = 'Let us know your MO-IM detail';
      console.log('no description');
      return;
    } else if (this.meeting.location==null) {
      this.notice = 'Where shall the MO-IM take place?';
      console.log('no location');
      return;
    } else if (this.meeting.max_member==null) {
      this.notice = 'How many members you want? (of course not 1 right?)';
      console.log('no members');
      return;
    } else if (this.meeting.max_member>50) {
      this.notice = 'Well, that seems like a huge conference...';
      console.log('max member exceeded');
      return;
    } else if (this.meeting.max_member===0) {
      this.notice = 'No member? You must be kidding!';
      console.log('no members');
      return;
    } else if (this.meeting.max_member===1) {
      this.notice = 'How many members you want? (of course not 1 right?)';
      console.log('no members');
      return;
    }

    console.log('input checked');
  }


  create(): void {
    const tagNames = this.convertTagInputs();
    this.meeting.subject = this.selectedSubject;
    this.checkInput();

    if (this.notice=='') {
      this.meetingService.createMeeting(
        this.currentUser,
        this.meeting.title,
        this.meeting.subject,
        this.meeting.description,
        this.meeting.location,
        this.meeting.max_member,
        tagNames
      )
        .then(new_meeting => {
          alert('Successfully Created a meeting!');
          this.router.navigate(['/meeting', new_meeting.id]);
        });
    } else {
      alert(this.notice);
      this.notice = '';
      return;
    }
  }

  convertTagInputs(): string[] {
    const res = [];

    for (const tag of this.tagInputs){
      res.push(tag.value);
    }

    return res;
  }

}
