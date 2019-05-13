import { Component, OnInit, Input } from '@angular/core';

import { MatTableDataSource } from '@angular/material';
import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample, PeValueStructure } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';
import { PeValueTableComponent } from './pe-value-table.component';

@Component({
  selector: 'pe-header',
  template: `
  <h1>Pe Header</h1>
  <mat-accordion>

    <mat-expansion-panel>
      <mat-expansion-panel-header>
        <mat-panel-title>Dos Header</mat-panel-title>
      </mat-expansion-panel-header>
      <pe-value-table [theSourceList]="dosHeader"></pe-value-table>
    </mat-expansion-panel>

    <mat-expansion-panel>
      <mat-expansion-panel-header>
        <mat-panel-title>File Header</mat-panel-title>
      </mat-expansion-panel-header>
      <pe-value-table [theSourceList]="fileHeader"></pe-value-table>
    </mat-expansion-panel>

    <mat-expansion-panel>
      <mat-expansion-panel-header>
        <mat-panel-title>Nt Header</mat-panel-title>
      </mat-expansion-panel-header>
      <pe-value-table [theSourceList]="ntHeader"></pe-value-table>
    </mat-expansion-panel>

  </mat-accordion>
  `,
})
export class PeHeaderComponent implements OnInit {
  @Input() peSample: PeSample;

  dosHeader: Array<PeValueStructure>;
  fileHeader: Array<PeValueStructure>;
  ntHeader: Array<PeValueStructure>;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this._svrdata.getPeHeaderInfo(this.peSample._id).subscribe(
      v => {
        this.dosHeader = v["dos_header"];
        this.fileHeader = v["file_header"];
        this.ntHeader = v["nt_header"];
      },
      e => {
        console.log(e);
      }
    );
  }
}
