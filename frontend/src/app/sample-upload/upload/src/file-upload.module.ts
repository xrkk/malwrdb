import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { FileDropDirective } from './file-drop.directive';
import { FileSelectDirective } from './file-select.directive';
import { DirSelectDirective } from './dir-select.directive';

@NgModule({
  imports: [CommonModule],
    declarations: [FileDropDirective, FileSelectDirective, DirSelectDirective],
    exports: [FileDropDirective, FileSelectDirective, DirSelectDirective]
})
export class UploadModule { }
