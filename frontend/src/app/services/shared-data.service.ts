import { Injectable } from '@angular/core';

import { Sample } from '../models/models'

@Injectable()
export class SharedDataService {

  // 当前选中的样本
  private _currentSample: Sample;
  get currentSample(): Sample {
    return this._currentSample;
  }
  set currentSample(sample: Sample) {

    if (this._currentSample == undefined || (this._currentSample.sha256 != sample.sha256)) {
      this._currentSample = sample;
    }
  }
}
