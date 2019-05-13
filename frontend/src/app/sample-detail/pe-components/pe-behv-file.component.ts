import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';


@Component({
  selector: 'pe-behv-file',
  template: `
  <h1>Pe Behv File</h1>
  `,
})
export class PeBehvFileComponent implements OnInit {
  @Input() peSample: PeSample;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // this._svrdata.get();
  }
}
