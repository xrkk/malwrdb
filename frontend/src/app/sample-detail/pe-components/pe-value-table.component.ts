import { Component, Input } from '@angular/core';

import { MatTableDataSource } from '@angular/material';
import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeValueStructure } from '../../models/models-pe';

@Component({
  selector: 'pe-value-table',
  template: `
  <mat-table #table [dataSource]="dataSource">
    <mat-header-row *matHeaderRowDef="displayedColumns"></mat-header-row>
    <mat-row *matRowDef="let row; columns: displayedColumns;"></mat-row>

    <ng-container matColumnDef="name">
      <mat-header-cell *matHeaderCellDef> Name. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.name}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="offset_file">
      <mat-header-cell *matHeaderCellDef> File Offset. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.offset_file}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="offset_mm">
      <mat-header-cell *matHeaderCellDef> Mm Offset. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.offset_mm}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="value">
      <mat-header-cell *matHeaderCellDef> Value. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.value}} </mat-cell>
    </ng-container>

  </mat-table>

  `,
})
export class PeValueTableComponent {

  private _theSourceList: Array<PeValueStructure>;
  @Input() set theSourceList(v: Array<PeValueStructure>) {
    this._theSourceList = v;
    this.dataSource = new MatTableDataSource(v);
  }
  get theSourceList(): Array<PeValueStructure> {
    return this._theSourceList;
  }

  displayedColumns = ['name', 'offset_file', 'offset_mm', "value"];
  dataSource: any;

  constructor() { }
}
