import { TestBed } from '@angular/core/testing';

import { AnalizadorSegundaFaseService } from './analizadorSegundaFase.service';

describe('AnalizadorSegundaFaseService', () => {
  let service: AnalizadorSegundaFaseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalizadorSegundaFaseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
