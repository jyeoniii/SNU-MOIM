import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login-required',
  templateUrl: './login-required.component.html',
  styleUrls: ['./login-required.component.css']
})
export class LoginRequiredComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  signIn() {
    this.router.navigate(['/sign_in']);
  }
}
