import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2'



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  LoginFirstFase(){
    Swal.fire({
      title: 'Welcome to PyTypeCraft First Phase',
      text: "",
      icon: 'success',
      showConfirmButton: false,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Aceptar',
      timer: 1000
    })
    this.router.navigate(['analizarPrimeraFase'])
  }
  LoginSecondFase(){
    Swal.fire({
      title: 'Welcome to PyTypeCraft Second Phase',
      text: "",
      icon: 'success',
      showConfirmButton: false,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Aceptar',
      timer: 1000
    })
    this.router.navigate(['analizarSegundaFase'])
  }
}
