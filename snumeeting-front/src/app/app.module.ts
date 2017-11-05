import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { MeetingCreateComponent } from './meeting-create/meeting-create.component';

@NgModule({
  declarations: [
    AppComponent,
    MeetingCreateComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
