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

  private messages: Message[] = [];
  private users: User[] = [];
  private fbFriends: User[] = [];
  private loginedUser: User;
  private betweenMessages: Message[] = [];
  private selectedUser: User;
  private onChat: User[] = []; // tab my messages, between messages
  @Input() newMessage: string;

  ngOnInit() {
    this.getMessages();
    this.userService.getLoginedUser().then(user => {
      this.loginedUser = user;
      this.fbFriends = user.fb_friends;
    });
    this.userService.getUsers().then(users => this.users = users);
  }

  getMessages(): void {
    this.messageService.getMessages().then(messages => this.messages = messages);
  }

  getUser(id: number): User {
    return this.users.find(u => u.id === id);
  }

  selectAll(): void {
    this.selectedUser = null;
  }

  onDoubleClick(user: User): void {
    if(user.id != this.loginedUser.id){
      if(this.onChat.length == 0 || this.onChat.indexOf(user) == -1) {
        this.onChat.unshift(user);
      }
      this.onSelect(user);
    }
    else {
      window.alert("Cannot chat with yourself!");
    }
  }

  onSelect(user: User): void {
    this.selectedUser = user;
    this.betweenMessages = this.messages.filter(m => 
      (m.sender.id === this.loginedUser.id && m.receiver.id === user.id) ||
      (m.sender.id === user.id && m.receiver.id === this.loginedUser.id)
    );
  }

  deSelect(user: User): void {
    this.onChat = this.onChat.filter(u => u.id !== user.id);
    if(user.id === this.selectedUser.id) {
      this.selectAll();
    }
  }

  sendMessage(sender: User, receiver: User, content: string): void {
    if(this.newMessage != null) {
      let message;
      this.messageService.sendMessage(sender, receiver, content)
        .then(res => {
          message = res;
          this.messages.push(res);
          this.betweenMessages.push(res);
          this.newMessage = null;
        });
    }
  }

  signOut(): void {
    this.userService.signOut();
    this.router.navigate(['/']);
  }
}
