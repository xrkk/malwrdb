import { Directive, EventEmitter, ElementRef, Input, HostListener, Output } from '@angular/core';

import { FileUploader } from './file-uploader.class';

@Directive({ selector: '[ng2DirSelect]' })
export class DirSelectDirective {
  @Input() public uploader: FileUploader;
  @Output() public OnDirChanged: EventEmitter<File[]> = new EventEmitter<File[]>();

  protected element: ElementRef;

  public constructor(element: ElementRef) {
    this.element = element;
  }

  public getOptions(): any {
    return this.uploader.options;
  }

  public getFilters(): any {
    return {};
  }

  public isEmptyAfterSelection(): boolean {
    return !!this.element.nativeElement.attributes.multiple;
  }

  @HostListener('change')
  public onChange(): any {
    let files = this.element.nativeElement.files;
    let options = this.getOptions();
    let filters = this.getFilters();

    if (files.length == 0){
      console.log("no file in target dir, ignore this action");

    }
    else if (files.length <= 100) {

      console.log("file count in selected dir:" + files.length);

      this.uploader.clearQueue();
      this.uploader.addToQueue(files, options, filters);
      this.OnDirChanged.emit(files);

      if (this.isEmptyAfterSelection()) {
        this.element.nativeElement.value = '';
      }
    }
    else {
      console.log("选中文件个数太多, 忽略:" + files.length)
    }
  }
}
