import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ProfileComponent } from './profile/profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { MeetingDetailComponent } from './meeting-detail/meeting-detail.component';
import { MeetingCreateComponent } from './meeting-create/meeting-create.component';
import {MeetingsComponent} from './meetings/meetings.component';

const routes: Routes = [
  { path: '', redirectTo: '/sign_in', pathMatch: 'full' },
  { path: 'sign_in',  component: SignInComponent },
  { path: 'sign_up', component: SignUpComponent },
  { path: 'user/:id', component: ProfileComponent },
  { path: 'user/:id/edit', component: EditProfileComponent },
  { path: 'meeting/create', component: MeetingCreateComponent },
  { path: 'meeting/:id', component: MeetingDetailComponent },
  { path: 'meeting', component: MeetingsComponent},
  { path: '**', redirectTo: '/sign_in' },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
