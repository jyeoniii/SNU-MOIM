import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Meeting } from '../models/meeting';
import { Comment } from '../models/comment';
import { User } from '../models/user';
import { MeetingService } from '../services/meeting.service';
import {CommentService} from '../services/comment.service';
import {UserService} from "../services/user.service";

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

  private selectedComment: Comment = null;   // Comment to be edited

  @Input() private newComment: string = null;
  private isPrivate = false;
  private isPrivate_edit = false;

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.meetingService.getMeeting(+params['id'])
        .then(meeting => {
          this.selectedMeeting = meeting;
          this.author = meeting.author;
        });
      this.commentService.getCommentsOnMeeting(+params['id'])
        .then(comments => {
          this.comments = comments;
        });
      this.userService.getLoginedUser()
        .then(user => this.currentUser = user);
    });
  }


  goBack(): void {
    this.router.navigate(['/meeting']);
  }

  // edit(): void {
  //   this.router.navigate(['/meeting', this.selectedArticle.id, 'edit']);
  // }
  //
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

}
