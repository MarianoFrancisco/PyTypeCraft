import { TestBed } from '@angular/core/testing';

import { AnalizadorPrimeraFaseService } from './analizadorPrimeraFase.service';

describe('AnalizadorService', () => {
  let service: AnalizadorPrimeraFaseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalizadorPrimeraFaseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
