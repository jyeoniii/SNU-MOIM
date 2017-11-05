import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ProfileComponent } from './profile/profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';

const routes: Routes = [
  { path: '', redirectTo: '/sign_in', pathMatch: 'full' },
  { path: 'sign_in',  component: SignInComponent },
  { path: 'sign_up', component: SignUpComponent },
  { path: 'user/:id', component: ProfileComponent },
  { path: 'user/:id/edit', component: EditProfileComponent },
  { path: '**', redirectTo: '/sign_in' }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
