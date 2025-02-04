import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Meeting } from '../models/meeting';
import { Comment } from '../models/comment';
import { User } from '../models/user';
import { Tag } from '../models/tag';
import { MeetingService } from '../services/meeting.service';
import { UserService } from '../services/user.service';
import { RecommendService } from '../services/recommend.service';
import { CommentService} from '../services/comment.service';
import { Datetime} from '../models/datetime';
import { MessageService } from '../services/message.service';

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
    private recommendService: RecommendService,
    private meetingService: MeetingService,
    private commentService: CommentService,
    private messageService: MessageService
  ) { }

  private selectedMeeting: Meeting;

  private comments: Comment[];
  private author: User;
  private currentUser: User;
  private alreadyJoined = false;
  private datetime: Datetime;

  private selectedComment: Comment = null;   // Comment to be edited

  @Input() private newComment: string = null;
  private isPrivate = false;
  private isPrivate_edit = false;

  private tags: Tag[];

  private memberName = null;
  private emptySeats = null;

  private MAX_INVITATION = 5;
  private recommendedUsers: User[] = null;
  private invitationList: User[] = [];

  private month = ['January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.meetingService.getMeeting(+params['id'])
        .then(meeting => {
          if(meeting == null) {
            this.router.navigate(['/404']);
          }
          this.selectedMeeting = meeting;
          this.author = meeting.author;
          this.tags = meeting.tags;

          this.datetime = meeting.datetime;

          this.emptySeats = new Array(this.selectedMeeting.max_member - this.selectedMeeting.members.length);
          this.userService.getLoginedUser()
            .then(user => {
              this.currentUser = user;
              if (!this.currentUser) {
                this.router.navigate(['/signin_first']);
              }
              this.getRecUsers();
              if (this.selectedMeeting.members.find(member => member.id === this.currentUser.id)) {
                this.alreadyJoined = true;
              }
            });
        });
      this.commentService.getCommentsOnMeeting(+params['id'])
        .then(comments => {
          this.comments = comments.reverse();
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
    if (confirm('Are you sure to delete this meeting?')) {
      this.meetingService.deleteMeeting(this.selectedMeeting.id)
        .then(() => {
          this.router.navigate(['/meeting']);
        });
    }
  }

  createComment(content: string): void {
    if (this.newComment !== null) {
      this.commentService.createComment(this.selectedMeeting.id, this.currentUser, content, !this.isPrivate)
        .then(res => {
          this.comments.unshift(res);
          this.newComment = null;
          this.isPrivate = false;
        });
    }
  }

  toEditMode(comment: Comment): void {
    this.selectedComment = comment;
  }

  cancleEditMode(comment: Comment): void {
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
    if (confirm('Are you sure to delete this comment?')){
      console.log(comment);
      this.commentService.deleteComment(comment.id)
        .then(() => {
          this.comments.splice(this.comments.indexOf(comment), 1);
        });
    }
  }

  isOwner(): boolean {
    if (this.currentUser && this.selectedMeeting) {
      return this.currentUser.id === this.author.id;
    } else {
      // No user logged in
      return false;
    }
  }

  signOut(): void {
    this.userService.signOut()
      .then(() => this.router.navigate(['/signin']));
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
    if (confirm('Will you be with us?')) {
      this.meetingService.joinMeeting(this.selectedMeeting.id, this.currentUser.id)
        .then(() => {
          this.selectedMeeting.members.push(this.currentUser);
          this.emptySeats = new Array(this.selectedMeeting.max_member - this.selectedMeeting.members.length);
          this.alreadyJoined = true;
          alert('Welcome!');
        });
    }
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

  getRecUsers(): void {
    this.recommendService.getRecUsersForMeeting(this.currentUser.id, this.selectedMeeting.id, 8)
      .then(users => {
        this.recommendedUsers = users;
        console.log(this.recommendedUsers);
      });
  }

  addInvitationList(user: User): void {
    if (this.invitationList.indexOf(user) !== -1) {
      alert('This user is already in the list!');
      return;
    } else if (this.invitationList.length >= this.MAX_INVITATION) {
      alert('Cannot add more users! (You can send invitation to maximum ' + this.MAX_INVITATION + ' members)');
      return;
    }
    this.invitationList.push(user);
  }

  sendInvitation(): void {
    if (confirm('Are you sure to send invitations to these users?')) {
      const content: string = `Invitation message from ${this.currentUser.name}(${this.currentUser.username})!\n` +
                       `Do you want to join this meeting?\n\n` +
                       `No. ${this.selectedMeeting.id}\n` +
                       `Title: ${this.selectedMeeting.title}\n` +
                       `Subject: ${this.selectedMeeting.subject.name}\n\n` +
                       `You are always welcome! Looking forward to be with you :)`;
      for (const user of this.invitationList){
        this.messageService.sendMessage(this.currentUser.id, user.id, content);
      }
      alert('Invitation message has been sent to selected users!');
      this.invitationList = [];
    }
  }

  padLeft(n: number, padChar: string, size: number): string {
    return (String(padChar).repeat(size) + String(n)).substr( (size * -1), size) ;
  }

  changeMemberNameShown(name: string) {
    this.memberName = name;
  }

}
