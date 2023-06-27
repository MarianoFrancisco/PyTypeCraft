import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalizadorPrimeraFaseComponent } from './analizadorPrimeraFase.component';

describe('AnalizadorPrimeraFaseComponent', () => {
  let component: AnalizadorPrimeraFaseComponent;
  let fixture: ComponentFixture<AnalizadorPrimeraFaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnalizadorPrimeraFaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AnalizadorPrimeraFaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
