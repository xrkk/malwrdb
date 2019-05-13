import { Component, ViewChild } from '@angular/core';
import { ServerDataService } from '../services/server-data.service'

// import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { MaterialComponentModule } from '../modules/material-component.module';

@Component({
  selector: 'test',
  template: `
  <button mat-raised-button color="primary" (click)="test($event)">Test!</button>
  `,
  styleUrls: ['./test.component.css']
})
export class TestComponent{

  constructor(private _svrdata: ServerDataService) { }

  test(evt: any){
    this._svrdata.getTest().subscribe(
      v => {
        console.log(v);
      }
    );
  }

}
