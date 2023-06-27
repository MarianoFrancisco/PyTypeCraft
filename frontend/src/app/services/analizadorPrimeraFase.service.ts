import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AnalizadorPrimeraFaseService {

  constructor(private http:HttpClient) { }

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type": "application/json"
  });

  Analizer(code:String){
    const url = 'http://34.28.167.82:4000/compile'
    return this.http.post<any>(
      url,
      {
        "code": code,
      }
    ).pipe(map(data=>data));
  }

  Errores(){
    const url = 'http://34.28.167.82:4000/mistake'
    return this.http.get<any>(url)
  }

  Tabla(){
    const url = 'http://34.28.167.82:4000/symbol'
    return this.http.get<any>(url)
  }
}
