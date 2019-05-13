import { Component, OnInit, Input } from '@angular/core';

import { LogLine } from '../models/models';
import { ServerDataService } from '../services/server-data.service';

import { MaterialComponentModule } from '../modules/material-component.module';

@Component({
  selector: 'admin-log',
  template: `
  <mat-checkbox [(ngModel)]="isWarn">Warn</mat-checkbox>
  <mat-checkbox [(ngModel)]="isDebug">Debug</mat-checkbox>
  <button (click)="clearLog()">Clear All Logs</button>
  <div *ngFor="let log of logLines">
      <div [ngSwitch]="log.level">
          <div *ngSwitchCase="'ERROR'">
              <span style="color: red; font-weight: bold;">{{ log.info }}</span>
          </div>
          <div *ngSwitchCase="'WARN'">
              <span *ngIf="isWarn" style="color: yellow">{{ log.info }}</span>
          </div>
          <div *ngSwitchCase="'DEBUG'">
              <span *ngIf="isDebug" >{{ log.info }}</span>
          </div>
      </div>
      <br/>
  </div>
  `
})

export class AdminLogComponent implements OnInit {
  logLines: LogLine[];
  isWarn: boolean = true;
  isDebug: boolean = true;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this._svrdata.getLogLines(this.isWarn, this.isDebug).subscribe(
      v => {
        this.logLines = v;
      },
      e => {
        console.log("getLogLines fail: " + e);
      }
    );
  }

  clearLog() {
    this._svrdata.clearLogLines();
    this.logLines = [];
  }
}
