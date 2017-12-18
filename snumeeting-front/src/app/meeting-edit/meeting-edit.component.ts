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
  author: User;
  notice: string='';

  allTags: string[];
  tagInputs = [];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.meetingService.getMeeting(+params['id']).then(meeting => {
        this.selectedMeeting = meeting;
        if(meeting == null) {
          this.router.navigate(['/404']);
        }
        this.selectedSubject = meeting.subject;
        for (const tag of meeting.tags){
          this.tagInputs.push(tag.name);
        }
      });
    })
    this.userService.getLoginedUser().then(user => {
      this.currentUser = user;
      if (!this.currentUser) {
        this.router.navigate(['/signin_first']);
      }
    });
    this.metaDataService.getSubjectList().then(subjects => this.subjects = subjects);
    this.metaDataService.getInterestList().then(interests => this.interests = interests);
  }

  signOut(): void {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']))
  }

  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  checkInput(): void {
    if (this.selectedMeeting.title=='') {
      this.notice = 'Did you forget a title?';
      console.log('no title');
      return;
    } else if (this.selectedMeeting.subject==null) {
      this.notice = 'What about subject?';
      console.log('no subject');
      return;
    } else if (this.selectedMeeting.description=='') {
      this.notice = 'Let us know your MO-IM detail';
      console.log('no description');
      return;
    } else if (this.selectedMeeting.location=='') {
      this.notice = 'Where shall the MO-IM take place?';
      console.log('no location');
      return;
    } else if (this.selectedMeeting.max_member==1) {
      this.notice = 'How many members you want? (of course not 1 right?)';
      console.log('no members');
      return;
    } else if (this.selectedMeeting.max_member==0) {
      this.notice = 'No member? You must be kidding!';
      console.log('no members');
      return;
    } else if (this.selectedMeeting.max_member<0) {
      this.notice = 'Negative members? Hehe';
      console.log('negative member');
      return;
    } else if (this.selectedMeeting.max_member>50) {
      this.notice = 'Well, that seems like a huge conference...';
      console.log('max member exceeded');
      return;
    }


    console.log('input checked');
  }

  toEdit(): void {

    const tag_names = this.convertTagInputs();
    console.log(tag_names);
    this.selectedMeeting.subject = this.selectedSubject;
    this.checkInput();

    if (this.notice=='') {
      this.meetingService.editMeeting(this.selectedMeeting, tag_names)
        .then(() => {
          alert('Successfully edited (or no changed) the MO-IM!')
          this.router.navigate(['/meeting', this.selectedMeeting.id]);
        });
    } else {
      alert(this.notice);
      this.notice='';
      return;
    }


  }

  convertTagInputs(): string[] {
    const res = [];

    for (const tag of this.tagInputs) {
      if (tag.hasOwnProperty('value')) {
        res.push(tag.value);
      } else {
        res.push(tag);
      }

    }

    return res;
  }


}
