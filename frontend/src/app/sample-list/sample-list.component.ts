import { Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';

import { MaterialComponentModule } from '../modules/material-component.module';
import { PageEvent } from '@angular/material';

import { ServerDataService } from '../services/server-data.service';
import { SharedDataService } from '../services/shared-data.service';
import { RefGroup, Sample } from '../models/models';

import { RefGroupComponent } from './ref-group/ref-group.component';

@Component({
  selector: 'sample-list',
  template: `
  <mat-toolbar color="primary">
    <mat-toolbar-row>
      <button mat-raised-button color="warn" (click)="clearTree($event)">DeleteTree</button>
    </mat-toolbar-row>
  </mat-toolbar>

  <div *ngFor="let group of showGroupList">
      <ref-group [refGroup]="group"></ref-group>
      <br/>
  </div>

  <mat-paginator [length]="allGroupLength"
                [pageSize]="defaultPageSize"
                [pageSizeOptions]="pageSizeOptions"
                (page)="reload($event)">
  </mat-paginator>
  `,
  styleUrls: ['./sample-list.component.css']
})
export class SampleListComponent {
  defaultPageSize = 10;
  pageSizeOptions = [5, 10, 25, 100];

  is_updating: boolean = false;

  showGroupList: RefGroup[];
  allGroupLength: number;

  constructor(
    private _router: Router,
    private _svrdata: ServerDataService,
    private _shrdata: SharedDataService
  ) { }

  ngOnInit(){
    this.getGroupList();
  }

  getGroupList(pageSize: number = this.defaultPageSize, pageIndex: number = 0): void {
    this.is_updating = true;
    this._svrdata.getGroupList(pageSize, pageIndex).subscribe(
      v => {
        this.showGroupList = v["group_list"];
        this.allGroupLength = v["group_length"];
        this.is_updating = false;
      },
      e => {
        this.is_updating = false;
      },
      () => {
        this.is_updating = false;
      }
    );
  }

  // reload groupList
  reload(evt: any) {
    this.getGroupList(evt.pageSize, evt.pageIndex);
  }

  clearTree(evt: any) {
    this._svrdata.cmdClearTree().subscribe(
      v => {
        this.getGroupList();
      });
  }
}
