import { Component, ViewChild, OnInit, Input } from '@angular/core';

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

@Component({
  selector: 'ref-file',
  template: `
  <div href="" [contextMenu]="basicMenu" style="border: 2px solid black">
      <span>{{ refFile.file_name }}</span>
  </div>

  <!-- RightClick menu to select actions -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <context-menu>
    <ng-template contextMenuItem (execute)="analyzeAsSample()">Analyze!</ng-template>
    <ng-template contextMenuItem (execute)="renameFile()">Rename</ng-template>
    <ng-template contextMenuItem (execute)="delFile()">Delete</ng-template>
  </context-menu>
  `
})

export class RefFileComponent implements OnInit {
  @Input() refFile: RefFile;
    @ViewChild(ContextMenuComponent) basicMenu: ContextMenuComponent;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // get data from server
  }

    analyzeAsSample(){
        this._svrdata.cmdAnalyzeSample(this.refFile._id);
    }

    renameFile(){
        console.log("rename file");
    }

    delFile(){
        console.log("del file");
    }
}
