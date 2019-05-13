import { Component, ViewChild, OnInit, Input } from '@angular/core';

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { RefDir, Sample, RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

import { RefFileComponent } from './ref-file.component';
import { SampleComponent } from './sample.component';

@Component({
  selector: 'ref-dir',

  template: `
  <a href="" style="color: green" [contextMenu]="basicMenu">{{ refDir.dir_name }}</a>

  <!-- RightClick menu to select actions -->
  <context-menu>
    <ng-template contextMenuItem (execute)="addFiles()">AddFiles</ng-template>
    <ng-template contextMenuItem (execute)="renameDir()">Rename</ng-template>
    <ng-template contextMenuItem (execute)="delDir()">Delete</ng-template>
  </context-menu>

  <!-- children items -->
  <div style="margin-left: 40px">
      <div *ngIf="subRefDirs">
          <div *ngFor="let dir of subRefDirs">
              <ref-dir [refDir]="dir"></ref-dir>
          </div>
      </div>
      <div *ngIf="subSamples">
          <div *ngFor="let sample of subSamples">
              <sample [sample]="sample"></sample>
          </div>
      </div>
      <div *ngIf="subRefFiles">
          <div *ngFor="let file of subRefFiles">
              <ref-file [refFile]="file"></ref-file>
          </div>
      </div>
  </div>
  `
})

export class RefDirComponent implements OnInit {
  @Input() refDir: RefDir;
  @ViewChild(ContextMenuComponent) basicMenu: ContextMenuComponent;

  subRefDirs: RefDir[];
  subSamples: Sample[];
  subRefFiles: RefFile[];

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // console.log("id:" + this.refDir._id);
    this._svrdata.getSubRefDirs(this.refDir._id).subscribe(
      v => {
        this.subRefDirs = v;
      },
      e => { console.log("getSubRefDirs error: " + e); },
      () => { }
    );
    this._svrdata.getSubSamples(this.refDir._id).subscribe(
      v => {
        this.subSamples = v;
      },
      e => { console.log("getSubSamples error: " + e); },
      () => { }
    );
    this._svrdata.getSubRefFiles(this.refDir._id).subscribe(
      v => {
        this.subRefFiles = v;
      },
      e => { console.log("getSubRefFiles error: " + e); },
      () => { }
    );
  }

  addFiles() {
    console.log("add files to dir");
  }

  renameDir() {
    console.log("rename dir");
  }

  delDir() {
    console.log("del dir");
    this._svrdata.cmdDeleteRefDir(this.refDir._id).subscribe(
      v => {
        // todo: reload
      });
  }
}
