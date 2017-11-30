import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { PaginationDirective } from '../../node_modules/angular2-bootstrap-pagination/directives/pagination.directive';
import { APP_BASE_HREF } from '@angular/common';

import { AppComponent } from './app.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ProfileComponent } from './profile/profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { MeetingDetailComponent} from './meeting-detail/meeting-detail.component';
import { MeetingCreateComponent } from './meeting-create/meeting-create.component';
import { MeetingsComponent } from './meetings/meetings.component';
import { MessagesComponent } from './messages/messages.component';
import { MeetingsComponent } from './meetings/meetings.component';
import { MeetingEditComponent } from './meeting-edit/meeting-edit.component';

import { UserService } from './services/user.service';
import { MeetingService } from './services/meeting.service';
import { CommentService } from './services/comment.service';
import { MessageService } from './services/message.service';
import { MetaDataService } from './services/meta-data-service';

import { AppRoutingModule } from './app.routing.module';

export function CSRFStrategy() {
  return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
}

@NgModule({
  declarations: [
    AppComponent,
    SignInComponent,
    SignUpComponent,
    ProfileComponent,
    EditProfileComponent,
    MeetingDetailComponent,
    MeetingCreateComponent,
    MeetingsComponent,
    MessagesComponent,
    MeetingEditComponent,
    PaginationDirective,
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    AppRoutingModule,
  ],
  providers: [
    MeetingService,
    CommentService,
    UserService,
    MessageService,
    MetaDataService,
    {
      provide: APP_BASE_HREF,
      useValue : '/'
    },
    {
      provide: XSRFStrategy,
      useFactory: CSRFStrategy
    },
  ],
  bootstrap: [AppComponent]
}
)

export class AppModule { }
