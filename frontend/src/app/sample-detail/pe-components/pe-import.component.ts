import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample, PeImportDllTable } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';
import { PeImportItemTableComponent } from './pe-import-item-table.component';

@Component({
  selector: 'pe-import',
  template: `
  <h1>Pe Import</h1>

  <mat-accordion>

      <div *ngFor="let importDll of importDllList">

        <mat-expansion-panel>
          <mat-expansion-panel-header>
            <mat-panel-title>{{importDll?.dll_name}}</mat-panel-title>
          </mat-expansion-panel-header>

          <pe-import-item-table [importItemList]="importDll?.item_list"></pe-import-item-table>

        </mat-expansion-panel>

      </div>

  </mat-accordion>

  `,
})
export class PeImportComponent implements OnInit {
  @Input() peSample: PeSample;

  importDllList: Array<PeImportDllTable>;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this._svrdata.getPeImportInfo(this.peSample._id).subscribe(
      v => {
          this.importDllList = v;
      });
  }
}
