import { Component, OnInit, Input } from '@angular/core';

import { RefGroup, RefDir, Sample, RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

import { RefDirComponent } from './ref-dir.component';

@Component({
    selector: 'ref-group',
    template: `
    <div *ngFor="let topRefDir of topRefDirList">
        <ref-dir [refDir]="topRefDir"> </ref-dir>
    </div>
  `
})

export class RefGroupComponent implements OnInit {
    @Input() refGroup: RefGroup;
    topRefDirList: RefDir[];
  constructor(private _svrdata: ServerDataService) { }

  ngOnInit(){
      this._svrdata.getTopRefDir(this.refGroup.group_id).subscribe(
        v => {
            this.topRefDirList = v;
        },
        e => {
            console.log("getTopRefDir error: " + e);
        },
        () => { }
       );
  }
}
