import { Component, OnInit, Input } from '@angular/core';
import { User } from '../models/user';
import { Message } from '../models/message';
import { UserService } from '../services/user.service';
import { MessageService } from '../services/message.service';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import 'rxjs/add/operator/switchMap';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css'],
})
export class MessagesComponent implements OnInit {

  constructor(
    private messageService: MessageService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  private currentUser: User;
  private sentMessages: Message[];
  private receivedMessages: Message[];
  private selectedUser: User;

  @Input() my_between: boolean; // tab my messages, between messages
  @Input() selected_id: number;

  ngOnInit() {
    this.route.paramMap
      .switchMap((params: ParamMap) =>
        this.messageService.getSentMessage(+params.get('id')))
      .subscribe(messages => this.sentMessages = messages);
    this.route.paramMap
      .switchMap((params: ParamMap) =>
        this.messageService.getReceivedMessage(+params.get('id')))
      .subscribe(messages => this.receivedMessages = messages);
    this.my_between = true;
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
  }

  onSelect(user: User): void {
    this.selectedUser = user;
  }

  showMyMessage(): void {
    this.my_between = true;
  }

  showBetweenMessage(): void {
    this.my_between = false;
  }

  sendMessage(target_id: number): void {
  }
}
