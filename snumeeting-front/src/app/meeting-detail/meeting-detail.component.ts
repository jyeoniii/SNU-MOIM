import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Meeting } from '../models/meeting';
import { Comment } from '../models/comment';
import { User } from '../models/user';
import { MeetingService } from '../services/meeting.service';
import {CommentService} from '../services/comment.service';
import {UserService} from '../services/user.service';

@Component({
  selector: 'app-meeting-detail',
  templateUrl: './meeting-detail.component.html',
  styleUrls: ['./meeting-detail.component.css']
})


export class MeetingDetailComponent implements OnInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private meetingService: MeetingService,
    private commentService: CommentService
  ) { }

  private selectedMeeting: Meeting;

  private comments: Comment[];
  private author: User;
  private currentUser: User;
  private alreadyJoined = false;

  private selectedComment: Comment = null;   // Comment to be edited

  @Input() private newComment: string = null;
  private isPrivate = false;
  private isPrivate_edit = false;

  private emptySeats = null;

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.userService.getLoginedUser()
        .then(user => this.currentUser = user);
      this.meetingService.getMeeting(+params['id'])
        .then(meeting => {
          this.selectedMeeting = meeting;
          this.author = meeting.author;
          this.emptySeats = new Array(this.selectedMeeting.max_member - this.selectedMeeting.members.length);
          if (this.selectedMeeting.members.find(member => member.id === this.currentUser.id)) {
            this.alreadyJoined = true;
            console.log(this.alreadyJoined);
          }
        });
      this.commentService.getCommentsOnMeeting(+params['id'])
        .then(comments => {
          this.comments = comments;
        });
    });
  }


  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  edit(): void {
    this.router.navigate(['/meeting', this.selectedMeeting.id, 'edit']);
  }

  delete(): void {
    this.meetingService.deleteMeeting(this.selectedMeeting.id);
    this.router.navigate(['/meeting']);
  }

  createComment(content: string): void {
    if (this.newComment !== null) {
      let comment;
      this.commentService.createComment(this.selectedMeeting.id, this.currentUser, content, !this.isPrivate)
        .then(res => {
          comment = res;
          this.comments.push(comment);
          this.newComment = null;
          this.isPrivate = false;
        });
    }
  }

  toEditMode(comment: Comment): void {
    this.selectedComment = comment;
  }

  cancleEditMode(comment: Comment): void{
    this.selectedComment = null;
  }

  editComment(comment: Comment): void {
    const targetIdx = this.comments.indexOf(comment);
    this.commentService.editComment(comment, !this.isPrivate_edit).then(modifiedComment => {
      this.comments[targetIdx] = modifiedComment;
      this.selectedComment = null;
    });

  }

  deleteComment(comment: Comment): void {
    console.log(comment);
    this.commentService.deleteComment(comment.id);
    this.comments.splice(this.comments.indexOf(comment), 1);
  }

  isOwner(): boolean {
    if (this.currentUser && this.selectedMeeting) {
      return this.currentUser.id === this.selectedMeeting.author.id;
    } else {
      // No user logged in
      return false;
    }
  }

  signOut(): void {
    this.userService.signOut();
    this.router.navigate(['/']);
  }

  changePrivateMode(create: boolean): void {
    if (create) {   // create mode
      this.isPrivate = !this.isPrivate;
    } else {        // edit mode
      this.isPrivate_edit = !this.isPrivate_edit;
    }
  }

  joinMeeting(): void {
    if (this.selectedMeeting.members.length === this.selectedMeeting.max_member) {
      alert('This meeting is already full! :(');
      return;
    }
    this.meetingService.joinMeeting(this.selectedMeeting.id, this.currentUser.id);
    this.selectedMeeting.members.push(this.currentUser);
    this.emptySeats = new Array(this.selectedMeeting.max_member - this.selectedMeeting.members.length);
    this.alreadyJoined = true;
    alert('Welcome!');
  }

  leaveMeeting(): void {
    if (confirm('Are you sure you leave this meeting?')) {
      this.meetingService.leaveMeeting(this.selectedMeeting.id, this.currentUser.id)
        .then(() => {
        alert('Bye!');
        this.selectedMeeting.members.splice(this.selectedMeeting.members.indexOf(this.currentUser), 1);
        this.emptySeats = new Array(this.selectedMeeting.max_member - this.selectedMeeting.members.length);
        this.alreadyJoined = false;
        });
    }
  }

  closeMeeting(): void {
    // Only for the author
    if (confirm('Are you sure to close this meeting?\n(You cannot edit or delete this meeting after closing.)')) {
      this.meetingService.closeMeeting(this.selectedMeeting.id);
      this.selectedMeeting.is_closed = true;
    }
  }
}
