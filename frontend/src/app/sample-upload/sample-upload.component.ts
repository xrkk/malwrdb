import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UtilService } from '../services/util.service';
import { MaterialComponentModule } from '../modules/material-component.module';
import { FileUploader } from './upload';

// 变量
const URL = 'http://127.0.0.1:5000/sample/upload/';

@Component({
  selector: 'sample-upload',
  templateUrl: './sample-upload.component.html',
  styleUrls: ['./sample-upload.component.css']
})
export class SampleUploadComponent {
  // this.group_uploader.setOptions({ headers: [{ name: "xxxxxx", value: "yyyyyyyy" }] });   --> request.headers
  // this.group_uploader.setOptions({ additionalParameter: { "xxxx": "yyyy" } });            --> request.form

  // 每个文件都是单独的样本
  public sample_uploader: FileUploader;
  // 所有文件作为同一组样本
  public group_uploader: FileUploader;

  public hasBaseDropZoneOver: boolean = false;
  public hasAnotherDropZoneOver: boolean = false;

  group_id: string = "";

  constructor(
    private _toastr: ToastrService,
    private _util: UtilService) {
    this.sample_uploader = new FileUploader({ url: URL + "?type=sample_list" });
    this.group_uploader = new FileUploader({});

  }

  public fileOverBase(e: any): void {
    this.hasBaseDropZoneOver = e;
  }

  public fileOverAnother(e: any): void {
    this.hasAnotherDropZoneOver = e;
  }

  showSuccess() {
    this._toastr.warning('Hello world!', 'Toastr fun!');
  }

  // group file selected
  groupDirChanged(files: any[]) {
    // generate new group_id
    this.group_id = this._util.generateGuuId();
  }

  // group files upload
  groupDirUpload() {
    console.log("total file count to upload: " + this.group_uploader.queue.length);
    // set url for each file
    for (var i = this.group_uploader.queue.length - 1; i >= 0; i--) {
      let file = this.group_uploader.queue[i];
      file.updateUrl(URL + "?type=sample_group&group_id=" + this.group_id + "&relative_path=" + file._file.webkitRelativePath);
    }
    this.group_uploader.uploadAll();
  }

  // group file cleared(may or may not after upload)
  groupDirClean() {
    this.group_id = "";
    this.group_uploader.clearQueue();
    this.group_uploader.setOptions({ url: "" });
  }
}
