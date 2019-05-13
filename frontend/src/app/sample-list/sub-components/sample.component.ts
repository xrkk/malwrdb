import { Component, ViewChild, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { Sample } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';
import { SharedDataService } from '../../services/shared-data.service';

@Component({
  selector: 'sample',
  template: `
    <div href="" style="background-color: yellow" [contextMenu]="basicMenu">
      <span>{{ sample.sample_name }}</span>
    </div>

    <!-- RightClick menu to select actions -->
    <context-menu>
      <ng-template contextMenuItem (execute)="routeToSample()">Watch Details</ng-template>
      <ng-template contextMenuItem (execute)="convertToRefFile()">Convert to reference file!</ng-template>
      <ng-template contextMenuItem (execute)="renameSample()">Rename</ng-template>
      <ng-template contextMenuItem (execute)="delSample()">Delete</ng-template>
    </context-menu>
  `
})

export class SampleComponent implements OnInit {
  @Input() sample: Sample;
  @ViewChild(ContextMenuComponent) basicMenu: ContextMenuComponent;

  constructor(
    private _svrdata: ServerDataService,
    private _shrdate: SharedDataService,
    private _router: Router
  ) { }

  ngOnInit() {
    // get data from server
  }

  routeToSample() {
    this._shrdate.currentSample = this.sample;
    this._router.navigateByUrl('/sample-detail');
  }

  convertToRefFile() {
    console.log("convert sample to file");
  }

  renameSample() {
    console.log("rename sample");
  }

  delSample() {
    console.log("del sample");
  }
}
