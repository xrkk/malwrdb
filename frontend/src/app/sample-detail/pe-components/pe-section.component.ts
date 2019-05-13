import { Component, OnInit, Input } from '@angular/core';

import { MatTableDataSource } from '@angular/material';
import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample, PeSection } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';


@Component({
  selector: 'pe-section',
  template: `
  <h1>Pe Section</h1>

  <mat-table #table [dataSource]="dataSource">
    <mat-header-row *matHeaderRowDef="displayedColumns"></mat-header-row>
    <mat-row *matRowDef="let row; columns: displayedColumns;"></mat-row>

    <ng-container matColumnDef="PointerToRelocations">
      <mat-header-cell *matHeaderCellDef> PointerToRelocations. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.PointerToRelocations}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="Characteristics">
      <mat-header-cell *matHeaderCellDef> Characteristics. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.Characteristics}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="Misc">
      <mat-header-cell *matHeaderCellDef> Misc. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.Misc}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="Misc_PhysicalAddress">
      <mat-header-cell *matHeaderCellDef> Misc_PhysicalAddress. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.Misc_PhysicalAddress}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="Misc_VirtualSize">
      <mat-header-cell *matHeaderCellDef> Misc_VirtualSize. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.Misc_VirtualSize}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="Name">
      <mat-header-cell *matHeaderCellDef> Name. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.Name}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="NumberOfLinenumbers">
      <mat-header-cell *matHeaderCellDef> NumberOfLinenumbers. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.NumberOfLinenumbers}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="NumberOfRelocations">
      <mat-header-cell *matHeaderCellDef> NumberOfRelocations. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.NumberOfRelocations}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="PointerToLinenumbers">
      <mat-header-cell *matHeaderCellDef> PointerToLinenumbers. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.PointerToLinenumbers}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="PointerToRawData">
      <mat-header-cell *matHeaderCellDef> PointerToRawData. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.PointerToRawData}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="SizeOfRawData">
      <mat-header-cell *matHeaderCellDef> SizeOfRawData. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.SizeOfRawData}} </mat-cell>
    </ng-container>

    <ng-container matColumnDef="VirtualAddress">
      <mat-header-cell *matHeaderCellDef> VirtualAddress. </mat-header-cell>
      <mat-cell *matCellDef="let element"> {{element.VirtualAddress}} </mat-cell>
    </ng-container>

  </mat-table>
  `,
})
export class PeSectionComponent implements OnInit {
  @Input() peSample: PeSample;
  sectionList: Array<PeSection>;
  displayedColumns = ['Characteristics', 'Misc', 'Misc_PhysicalAddress', 'Misc_VirtualSize',
    'Name', 'NumberOfLinenumbers', 'NumberOfRelocations', 'PointerToLinenumbers',
    'PointerToRawData', 'PointerToRelocations', 'SizeOfRawData', 'VirtualAddress'];
  dataSource: any;

  // Characteristics
  // Misc
  // Misc_PhysicalAddress
  // Misc_VirtualSize
  // Name
  // NumberOfLinenumbers
  // NumberOfRelocations
  // PointerToLinenumbers
  // PointerToRawData
  // PointerToRelocations
  // SizeOfRawData
  // VirtualAddress

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this._svrdata.getPeSectionInfo(this.peSample._id).subscribe(
      v => {
        this.sectionList = v;
        this.dataSource = new MatTableDataSource(v);
      });
  }
}
