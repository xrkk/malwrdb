import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';

import { PeHeaderComponent } from './pe-header.component';
import { PeSectionComponent } from './pe-section.component';
import { PeImportComponent } from './pe-import.component';
import { PeExportComponent } from './pe-export.component';
import { PeBehvFileComponent } from './pe-behv-file.component';

@Component({
  selector: 'pe-detail',
  template: `
  <h1>Pe Details</h1>

  <p>{{ peSample?.md5 }}</p>
  <p>{{ peSample?.sha1 }}</p>
  <p>{{ peSample?.sha128 }}</p>
  <p>{{ peSample?.sha256 }}</p>

  <pe-header [peSample]="peSample"></pe-header>
  <pe-section [peSample]="peSample"></pe-section>
  <pe-import [peSample]="peSample"></pe-import>
  <pe-export [peSample]="peSample"></pe-export>
  <pe-behv-file [peSample]="peSample"></pe-behv-file>
  `,
})
export class PeDetailComponent implements OnInit {
  @Input() peSample: PeSample;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // this._svrdata.get();
  }

}
