import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { from } from 'rxjs';
import {HomeComponent} from './home/home.component';
import {DatasetComponent} from './dataset/dataset.component';
import {PlayComponent} from './play/play.component';
//export {};


const routes: Routes = [{
  path: 'home',
  component: HomeComponent
},{
  path: '',
  redirectTo: 'home',
  pathMatch: 'full' // prefix
},{
  path: 'dataset',
  component: DatasetComponent
},{
  path:'play',
  component: PlayComponent
},{
  path: '**',
  component: HomeComponent
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
