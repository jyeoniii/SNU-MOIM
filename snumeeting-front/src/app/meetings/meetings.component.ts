import { NgModule, Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecommendService } from '../services/recommend.service';

import { NgxPaginationModule } from 'ngx-pagination';
import { Meeting } from '../models/meeting';
import { User } from '../models/user';
import { Interest } from '../models/interest';
import { Subject } from '../models/subject';
import { MeetingFB } from '../models/meetingFB';

import { UserService } from '../services/user.service';
import { MeetingService } from '../services/meeting.service';
import { MetaDataService } from '../services/meta-data-service';

@Component({
  selector: 'app-meetings',
  templateUrl: './meetings.component.html',
  styleUrls: ['./meetings.component.css',]
})
@NgModule({
  imports: [
    NgxPaginationModule,
  ],
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
  private currentUser: User;

  private sub;
  private availableOnly = false;

  private loginedUser: User = null;

  private meetings: Meeting[];
  private allMeetings: Meeting[];
  private allMeetingsWithoutFiltering: Meeting[] = null;

  private meetingsFBfriends: MeetingFB[];

  // Recommendation
  private meetingsRecommended: Meeting[] = null;
  private meetingsShown: Meeting[] = null;
  private K = 10; // Num of meetings to be recommended;
  private N = 3; // Num of recommended meetings to be shown
  private idx = 0;  // Start index to be shown from recommended meetings

  // Searching
  readonly OPTION_DEFAULT = 'options';
  private searchOptions = ['title', 'author', 'category', 'tag']
  private selectedOption = this.OPTION_DEFAULT;
  private query = '';
  private interestList: Interest[];
  @Input() private selectedInterest: Interest = null;
  @Input() private selectedSubject: Subject = null;

  // Pagination
  private currentPage = 1;
  private totalItems = -1; // total number of items
  private maxSize = 10; // max page size = meetingsPerPage

  // FB recommendation
  private FBname = null;
  private FB_N = 6;
  private meetingsShownFB: MeetingFB[];

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
                this.allMeetings = meetings.reverse();
                this.totalItems = this.allMeetings.length;
                this.pageChanged();
              });
            break;
          case this.searchOptions[0]:   // title
            this.meetingService.searchMeetingsOfTitle(query).then(res => {
              this.allMeetings = res.reverse();
              this.totalItems = this.allMeetings.length;
              this.pageChanged();
            });
            break;
          case this.searchOptions[1]:   // author
            this.meetingService.searchMeetingsOfAuthor(query).then(res => {
              this.allMeetings = res.reverse();
              this.totalItems = this.allMeetings.length;
              this.pageChanged();
            });
            break;
          case this.searchOptions[2]:   // category
            this.meetingService.searchMeetingsOfSubject(query).then(res => {
              this.allMeetings = res.reverse();
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
      if (this.loginedUser) {
        this.recommendService.getRecMeetings(this.loginedUser.id, 5)
          .then(res => {
            this.meetingsRecommended = res;
            this.meetingsShown = this.meetingsRecommended.slice(this.idx, this.idx + this.N);
            console.log(this.meetingsShown);
          });
      } else {
        this.router.navigate(['/signin_first']);
      }

      if (this.loginedUser.fb_connected) {
        this.meetingService.getMeetingsFromFBfriends(this.loginedUser.id)
          .then(meetings => {
            this.meetingsFBfriends = meetings;
            this.meetingsShownFB = this.meetingsFBfriends.slice(0, 0 + this.FB_N);
        });
      }
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
    if ((this.selectedOption !== 'category') && this.query === '') {
      alert('Please enter a query!')
      return;
    }
    if (this.selectedOption === 'category') {  // subject
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
    if (this.selectedOption === 'tag') { // tag
      this.router.navigate(['/meeting/tag'], { queryParams: { tag: searchQuery }});
      return;
    }
    this.router.navigate(['meeting'],
      { queryParams: { option: this.selectedOption, query: searchQuery }});
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

  signOut(): void {
    this.userService.signOut()
    .then(() => this.router.navigate(['/signin']));
  }

  showOtherRecommendation(next: boolean): void {
    if (next) {
      const increasedIdx = this.idx + 1;
      if (increasedIdx + this.N <= this.meetingsRecommended.length) this.idx = increasedIdx;
    } else {
      if (this.idx !== 0) this.idx -= 1;
    }
    this.meetingsShown = this.meetingsRecommended.slice(this.idx, this.idx + this.N);
  }

  changeFBNameShown(name: string) {
    console.log(this.FBname);
    this.FBname = name;
  }

}

