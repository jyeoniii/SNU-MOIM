import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { APP_BASE_HREF } from '@angular/common';

import { AppComponent } from './app.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ProfileComponent } from './profile/profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import {MeetingDetailComponent} from './meeting-detail/meeting-detail.component';

import { UserService } from './user-service';
import {MeetingService} from './meeting.service';
import {CommentService} from './comment.service';

import { AppRoutingModule } from './app.routing.module';


@NgModule({
  declarations: [
    AppComponent,
    SignInComponent,
    SignUpComponent,
    ProfileComponent,
    EditProfileComponent,
    MeetingDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [
    MeetingService,
    CommentService,
    UserService,
    {
      provide: APP_BASE_HREF,
      useValue : '/'
    }
  ],
  bootstrap: [AppComponent]
}
)

export class AppModule { }
