import { HttpClient } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnalizadorPrimeraFaseComponent } from './analizadorPrimeraFase/analizadorPrimeraFase.component';
import { AnalizadorSegundaFaseComponent } from './analizadorSegundaFase/analizadorSegundaFase.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  {
    path: 'analizarPrimeraFase',
    component: AnalizadorPrimeraFaseComponent
  },
  {
    path: 'analizarSegundaFase',
    component: AnalizadorSegundaFaseComponent
  },
  {
    path: 'home',
    component: HomeComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 
  constructor(private http: HttpClient){}
  uploadFile(formData:any){
    let url = ''
  }
}
