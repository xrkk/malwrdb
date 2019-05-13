/**
 * Angular 2 decorators and services
 */
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { environment } from 'environments/environment';
import { AppState } from './app.service';

/**
 * App Component
 * Top Level Component
 */
@Component({
  selector: 'app',
  encapsulation: ViewEncapsulation.None,
  styleUrls: [
    './app.component.css'
  ],
  template: `
    <nav>
      <a [routerLink]=" ['./'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Index
      </a>
      <a [routerLink]=" ['./home'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Home
      </a>
      <a [routerLink]=" ['./test'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Test
      </a>
      <a [routerLink]=" ['./sample-upload'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        样本上传
      </a>
      <a [routerLink]=" ['./sample-list'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        样本列表
      </a>
      <a [routerLink]=" ['./sample-detail'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        样本详情
      </a>
      <a [routerLink]=" ['./logline'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        日志
      </a>
      <a [routerLink]=" ['./tasks'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Tasks
      </a>

      <!--
      <a [routerLink]=" ['./detail'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Detail
      </a>
      <a [routerLink]=" ['./barrel'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        Barrel
      </a>
      <a [routerLink]=" ['./about'] "
        routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        About
      </a>
      <a *ngIf="showDevModule" [routerLink]=" ['./dev-module'] "
         routerLinkActive="active" [routerLinkActiveOptions]= "{exact: true}">
        DevModule
      </a>
      -->

    </nav>

    <main>
      <router-outlet></router-outlet>
    </main>

    <pre class="app-state">this.appState.state = {{ appState.state | json }}</pre>

    <footer>
      <span>Angular Starter by <a [href]="twitter">@gdi2290</a></span>
      <div>
        <a [href]="url">
          <img [src]="tipe" width="25%">
        </a>
      </div>
    </footer>
  `
})
export class AppComponent implements OnInit {
  public name = 'Angular Starter';
  public tipe = 'assets/img/tipe.png';
  public twitter = 'https://twitter.com/gdi2290';
  public url = 'https://tipe.io';
  public showDevModule: boolean = environment.showDevModule;

  constructor(
    public appState: AppState
  ) {}

  public ngOnInit() {
    console.log('Initial App State', this.appState.state);
  }

}

/**
 * Please review the https://github.com/AngularClass/angular2-examples/ repo for
 * more angular app examples that you may copy/paste
 * (The examples may not be updated as quickly. Please open an issue on github for us to update it)
 * For help or questions please contact us at @AngularClass on twitter
 * or our chat on Slack at https://AngularClass.com/slack-join
 */
