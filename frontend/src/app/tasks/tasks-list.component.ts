import { Component, OnInit, Input } from '@angular/core';

import { ActiveTask, HistoryTask } from '../models/models';
import { ServerDataService } from '../services/server-data.service';

import { MaterialComponentModule } from '../modules/material-component.module';

@Component({
  selector: 'task-list',
  template: `
  <h3>Active Tasks</h3>
  <div *ngFor="let task of activeTaskList">
      <label>{{ task?.id }}</label>
      <button mat-raised-button color="primary" (click)="cancelTask(task)">Cancel</button>
  </div>

  <h3>History Tasks</h3>
  <div *ngFor="let task of historyTaskList">
      <label>{{ task?.celery_task_id }}</label>
  </div>
  `
})

export class TaskListComponent implements OnInit {
  activeTaskList: ActiveTask[];
  historyTaskList: HistoryTask[];

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this.reload();
  }

  reload() {
    this._svrdata.getTaskList().subscribe(
      v => {
        console.log(v);
        this.activeTaskList = v["active"];
        this.historyTaskList = v["history"]
      },
      e => {
        console.log("getTaskList fail: " + e);
      }
    );
  }

  cancelTask(task: ActiveTask) {
    this._svrdata.cmdCancelTask(task.id);
    this.reload();
  }
}
