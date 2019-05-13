import { Routes } from '@angular/router';
import { HomeComponent } from './home';
import { TestComponent } from './test';
import { SampleUploadComponent } from './sample-upload';
import { SampleListComponent } from './sample-list';
import { SampleDetailComponent } from './sample-detail';
import { AdminLogComponent } from './admin-log/admin-log.component';
import { AboutComponent } from './about';
import { NoContentComponent } from './no-content';
import { TaskListComponent } from './tasks/tasks-list.component';

export const ROUTES: Routes = [
  { path: '',      component: HomeComponent },
  { path: 'home',  component: HomeComponent },
  { path: 'test',  component: TestComponent },
  { path: 'sample-upload',  component: SampleUploadComponent },
  { path: 'sample-list',  component: SampleListComponent },
  { path: 'sample-detail', component: SampleDetailComponent },
  { path: 'logline', component: AdminLogComponent },
  { path: 'tasks', component: TaskListComponent },

  { path: 'about', component: AboutComponent },
  { path: 'detail', loadChildren: './+detail#DetailModule'},
  { path: 'barrel', loadChildren: './+barrel#BarrelModule'},
  { path: '**',    component: NoContentComponent },
];
