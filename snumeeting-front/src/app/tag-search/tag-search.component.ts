import { NgModule, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { MeetingService } from '../services/meeting.service';
import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';

import { Meeting } from '../models/meeting';
import { User } from '../models/user';

import { NgxPaginationModule } from 'ngx-pagination';

@Component({
  selector: 'app-tag-search',
  templateUrl: './tag-search.component.html',
  styleUrls: ['./tag-search.component.css']
})
@NgModule({
  imports: [
    NgxPaginationModule,
  ],
})
export class TagSearchComponent implements OnInit {

  private tagName;
  private sub;

  private currentUser: User;

  private availableOnly = false;

  private meetings: Meeting[];
  private allMeetings: Meeting[];
  private allMeetingsWithoutFiltering: Meeting[];

  // Pagination
  private currentPage = 1;
  private totalItems = -1; // total number of items
  private maxSize = 10; // max page size = meetingsPerPage

  constructor(
    private meetingService: MeetingService,
    private metaDataService: MetaDataService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute,
    private location: Location,
  ) { }

  ngOnInit() {
    this.sub = this.route
      .queryParams
      .subscribe(params => {
        this.tagName = params['tag'] || null;
        if (this.tagName == null) {
          alert('A Tag should be specified!');
          this.goBack();
        } else {
          this.meetingService.getMeetingsOnTag(this.tagName).then(res => {
            this.allMeetings = res;
            this.totalItems = this.allMeetings.length;
            this.pageChanged();
          });
          this.userService.getLoginedUser()
            .then(user => this.currentUser = user);
        }
      });
  }

  pageChanged(): void {
    this.meetings = this.allMeetings.slice(
      (this.currentPage - 1) * this.maxSize,
      this.currentPage * this.maxSize);
  }

  available(): void {
    this.availableOnly = !this.availableOnly;
    if (this.availableOnly) {
      this.allMeetingsWithoutFiltering = this.allMeetings;
      this.allMeetings = this.allMeetings.filter(
        meeting => (meeting.members.length < meeting.max_member) && (!meeting.is_closed));
      this.pageChanged();
    } else {
      this.allMeetings = this.allMeetingsWithoutFiltering;
      this.pageChanged();
    }
  }

  goBack(): void {
    this.location.back();
  }

}
