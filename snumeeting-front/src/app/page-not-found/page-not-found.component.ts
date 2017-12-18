import { NgModule, Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from '../models/user';
import { UserService } from '../services/user.service';
import { MetaDataService } from '../services/meta-data-service';

@Component({
  selector: 'page-not-found',
  templateUrl: './page-not-found.component.html',
  styleUrls: ['./page-not-found.component.css']
})
export class PageNotFoundComponent implements OnInit {

  constructor(
    private metaDataService: MetaDataService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute,
  ) { }
  private currentUser: User;
  private loginedUser: User = null;

  ngOnInit() {
    this.userService.getLoginedUser().then(user => {
      this.loginedUser = user;
      if (this.loginedUser) {
      } else {
        this.router.navigate(['/signin_first']);
      }
    });
  }

  signOut(): void {
    this.userService.signOut()
    .then(() => this.router.navigate(['/signin']));
  }
}

