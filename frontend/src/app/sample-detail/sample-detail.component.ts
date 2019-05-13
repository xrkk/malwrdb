import { Component, OnInit } from '@angular/core';

import { SharedDataService } from '../services/shared-data.service';
import { Sample } from '../models/models';
import { PeSample } from '../models/models-pe';

import { PeDetailComponent } from './pe-components/pe.component';

@Component({
  selector: 'sample-detail',
  template: `
  <div *ngIf="sample" class='container'>

    <!--pe-->
    <pe-detail [peSample]="peSample"></pe-detail>

  </div>
  <div *ngIf="!sample">
    <h1>No Sample Selected!</h1>
  </div>
  `,
  styleUrls: ['./sample-detail.component.css']
})
export class SampleDetailComponent implements OnInit {
  sample: Sample;
  peSample: PeSample;

  constructor(private _shrdata: SharedDataService) { }

  ngOnInit() {
    this.sample = this._shrdata.currentSample;
    if (this.sample == undefined) { } else {
      // convert this.sample to this.peSample
      this.peSample = new PeSample();
      this.peSample._id = this.sample._id;
    }
  }

}
