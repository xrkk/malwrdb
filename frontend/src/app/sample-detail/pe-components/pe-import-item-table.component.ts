import { Component, Input } from '@angular/core';

import { MatTableDataSource } from '@angular/material';
import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeImportDllItem } from '../../models/models-pe';

@Component({
  selector: 'pe-import-item-table',
  template: `
  <mat-table #table [dataSource]="dataSource">

    <mat-header-row *matHeaderRowDef="displayedColumns"></mat-header-row>
    <mat-row *matRowDef="let row; columns: displayedColumns;"></mat-row>

    <ng-container matColumnDef="name">
      <mat-header-cell *matHeaderCellDef> Name. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.name}} </mat-cell>
    </ng-container>

  </mat-table>

  `,
})
export class PeImportItemTableComponent {

  private _importItemList: Array<PeImportDllItem>;
  @Input() set importItemList(v: Array<PeImportDllItem>) {
    this._importItemList = v;
    this.dataSource = new MatTableDataSource(v);
  }
  get importItemList(): Array<PeImportDllItem> {
    return this._importItemList;
  }

  displayedColumns = ['name',];
  dataSource: any;

  constructor() { }
}
