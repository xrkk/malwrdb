// Angular模块
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
// import { HttpModule } from '@angular/http';
import { HttpClientModule } from "@angular/common/http";
import { RouterModule, PreloadAllModules } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// 第三方模块
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ToastrModule } from 'ngx-toastr';
import { ContextMenuModule } from 'ngx-contextmenu';

// 咱自己的模块
import { UploadModule } from './sample-upload/upload'
import { DevModuleModule } from './+dev-module';
import { MaterialComponentModule } from './modules/material-component.module';

/*
 * Platform and Environment providers/directives/pipes
 */
import { environment } from 'environments/environment';
import { ROUTES } from './app.routes';
// App is our top level component
import { AppComponent } from './app.component';
import { APP_RESOLVER_PROVIDERS } from './app.resolver';
import { AppState, InternalStateType } from './app.service';

// Nav Component
import { HomeComponent } from './home';
import { TestComponent } from './test';
import { AboutComponent } from './about';
import { NoContentComponent } from './no-content';

// 自己定义的描述符
import { XLargeDirective } from './home/x-large';

// 自己定义的服务
import { ServerDataService } from './services/server-data.service';
import { SharedDataService } from './services/shared-data.service';
import { UtilService } from './services/util.service';

import '../styles/styles.scss';
import '../styles/headings.css';

// Component-Mine
import { SampleUploadComponent } from './sample-upload/sample-upload.component';
import { SampleListComponent } from './sample-list/sample-list.component';
import { SampleDetailComponent } from './sample-detail/sample-detail.component';

import { PeDetailComponent } from './sample-detail/pe-components/pe.component';
import { PeSectionComponent } from './sample-detail/pe-components/pe-section.component';
import { PeHeaderComponent } from './sample-detail/pe-components/pe-header.component';
import { PeImportComponent } from './sample-detail/pe-components/pe-import.component';
import { PeExportComponent } from './sample-detail/pe-components/pe-export.component';
import { PeBehvFileComponent } from './sample-detail/pe-components/pe-behv-file.component';
import { PeValueTableComponent } from './sample-detail/pe-components/pe-value-table.component';
import { PeImportItemTableComponent } from './sample-detail/pe-components/pe-import-item-table.component'

import { RefGroupComponent } from './sample-list/sub-components/ref-group.component';
import { RefDirComponent } from './sample-list/sub-components/ref-dir.component';
import { RefFileComponent } from './sample-list/sub-components/ref-file.component';
import { SampleComponent } from './sample-list/sub-components/sample.component';
import { AdminLogComponent } from './admin-log/admin-log.component';
import { TaskListComponent } from './tasks/tasks-list.component';

// Application wide providers
const APP_PROVIDERS = [
  ...APP_RESOLVER_PROVIDERS,
  AppState
];

type StoreType = {
  state: InternalStateType,
  restoreInputValues: () => void,
  disposeOldHosts: () => void
};

/**
 * `AppModule` is the main entry point into Angular2's bootstraping process
 */
@NgModule({
  bootstrap: [AppComponent],
  declarations: [
    AppComponent,
    AboutComponent,
    HomeComponent,
    NoContentComponent,
    XLargeDirective,
    TestComponent,

    SampleUploadComponent,
    SampleListComponent,
    SampleDetailComponent,

    PeSectionComponent,
    PeDetailComponent,
    PeBehvFileComponent,
    PeValueTableComponent,
    PeImportItemTableComponent,
    PeExportComponent,
    PeImportComponent,
    PeHeaderComponent,

    RefGroupComponent,
    RefDirComponent,
    RefFileComponent,
    SampleComponent,
    AdminLogComponent,
    TaskListComponent,
  ],
  /**
   * Import Angular's modules.
   */
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    // HttpModule,
    HttpClientModule,
    UploadModule,
    MaterialComponentModule,
    ContextMenuModule.forRoot(),
    NgbModule.forRoot(),
    ToastrModule.forRoot({
      timeOut: 3000,
      positionClass: 'toast-top-right',
      preventDuplicates: false,
    }),
    RouterModule.forRoot(ROUTES, {
      useHash: Boolean(history.pushState) === false,
      preloadingStrategy: PreloadAllModules
    }),

    /**
     * This section will import the `DevModuleModule` only in certain build types.
     * When the module is not imported it will get tree shaked.
     * This is a simple example, a big app should probably implement some logic
     */
    ...environment.showDevModule ? [DevModuleModule] : [],
  ],
  /**
   * Expose our Services and Providers into Angular's dependency injection.
   */
  providers: [
    environment.ENV_PROVIDERS,
    APP_PROVIDERS,
    ServerDataService,
    SharedDataService,
    UtilService,
  ]
})
export class AppModule { }
