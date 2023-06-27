import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AnalizadorSegundaFaseService {

  constructor(private http:HttpClient) { }

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type": "application/json"
  });

  Analizer(code:String){
    //const url = 'https://calm-dusk-76175.herokuapp.com/prueba'
    const url = 'http://127.0.0.1:4000/compile'
    return this.http.post<any>(
      url,
      {
        "code": code,
      }
    ).pipe(map(data=>data));
  }

  Errores(){
    const url = 'http://127.0.0.1:4000/mistake'
    //const url = 'https://calm-dusk-76175.herokuapp.com/errores'
    return this.http.get<any>(url)
  }

  Tabla(){
    const url = 'http://127.0.0.1:4000/symbol'
    //const url = 'https://calm-dusk-76175.herokuapp.com/simbolos'
    return this.http.get<any>(url)
  }
}
