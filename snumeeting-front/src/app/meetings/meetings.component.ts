import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Meeting } from '../models/meeting';
import { User } from '../models/user';
import { Interest } from '../models/interest';
import { Subject } from '../models/subject';

import { MeetingService } from '../services/meeting.service';
import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';
import { RecommendService } from '../services/recommend.service';


@Component({
  selector: 'app-meetings',
  templateUrl: './meetings.component.html',
  styleUrls: ['./meetings.component.css', './dashboard.css']
})
export class MeetingsComponent implements OnInit {

  constructor(
    private meetingService: MeetingService,
    private metaDataService: MetaDataService,
    private recommendService: RecommendService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  private sub;
  private availableOnly = false;

  private loginedUser: User = null;

  private meetings: Meeting[];
  private allMeetings: Meeting[];
  private allMeetingsWithoutFiltering: Meeting[] = null;

  private meetingsRecommended: Meeting[] = null;
  private K = 10; // Num of meetings to be recommended;
  private N = 3; // Num of recommended meetings to be shown
  private idx = 0;  // Start index to be shown from recommended meetings

  // Searching
  readonly OPTION_DEFAULT = 'options';
  private searchOptions = ['title', 'author', 'category']
  private selectedOption = this.OPTION_DEFAULT;
  private query = '';
  private interestList: Interest[];
  @Input() private selectedInterest: Interest = null;
  @Input() private selectedSubject: Subject = null;

  // Pagination
  private currentPage = 1;
  private totalItems = -1; // total number of items
  private maxSize = 10; // max page size = meetingsPerPage

  ngOnInit() {
    this.sub = this.route
      .queryParams
      .subscribe(params => {
        // Defaults to null if no query param provided.
        const option = params['option'] || null;
        const query = params['query'] || null;

        switch (option) {
          case null:
            this.meetingService.getMeetings()
              .then(meetings => {
                this.allMeetings = meetings;
                this.totalItems = this.allMeetings.length;
                this.pageChanged();
              });
            break;
          case this.searchOptions[0]:   // title
            this.meetingService.searchMeetingsOfTitle(query).then(res => {
              this.allMeetings = res;
              this.totalItems = this.allMeetings.length;
              this.pageChanged();
            });
            break;
          case this.searchOptions[1]:   // author
            this.meetingService.searchMeetingsOfAuthor(query).then(res => {
              this.allMeetings = res;
              this.totalItems = this.allMeetings.length;
              this.pageChanged();
            });
            break;
          case this.searchOptions[2]:   // category
            this.meetingService.searchMeetingsOfSubject(query).then(res => {
              this.allMeetings = res;
              this.totalItems = this.allMeetings.length;
              this.pageChanged();
            });
            break;
          default:
            console.error('Invalid option');
        }
      });
    this.metaDataService.getInterestList()
      .then(interestList => this.interestList = interestList);
    this.userService.getLoginedUser().then(user => {
      this.loginedUser = user;
      this.recommendService.getRecMeetings(this.loginedUser.id, 5)
        .then(res => this.meetingsRecommended = res);
    });
  }

  // ngOnDestroy {
  //   this.sub.unsubscribe();
  // }

  goToCreatePage(): void {
    this.router.navigate(['meeting/create']);
  }

  pageChanged(): void {
    this.meetings = this.allMeetings.slice(
      (this.currentPage - 1) * this.maxSize,
      this.currentPage * this.maxSize);
  }

  search(): void {
    let searchQuery = this.query;
    if ((this.selectedOption !== this.searchOptions[2]) && this.query === '') {
      alert('Please enter a query!')
      return;
    }
    if (this.selectedOption === this.searchOptions[2]) {
      if (this.selectedInterest === null) {
        alert('Please choose an interest and a subject!');
        return;
      }
      if (this.selectedSubject === null) {
        alert('Please choose a subject!');
        return;
      }
      searchQuery = `${this.selectedSubject.id}`;
      if (this.query !== '') {
        searchQuery = `${searchQuery}_${this.query}`;
      }
    }
    this.router.navigate(['meeting'],
      { queryParams: { option: this.selectedOption, query: searchQuery }});
  }

  available(): void {
    this.availableOnly = !this.availableOnly;
    if (this.availableOnly) {
      this.allMeetingsWithoutFiltering = this.allMeetings;
      this.allMeetings = this.allMeetings.filter(meeting => meeting.members.length < meeting.max_member);
      this.pageChanged();
    } else {
      this.allMeetings = this.allMeetingsWithoutFiltering;
      this.pageChanged();
    }
  }

  signOut(): void {
    this.userService.signOut();
    this.router.navigate(['/']);
  }

  showOtherRecommendation(next: boolean): void {
    if (next) {
      this.idx += 1;
    } else {
      this.idx -= 1;
    }
  }

}

