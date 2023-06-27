import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalizadorSegundaFaseComponent } from './analizadorSegundaFase.component';

describe('AnalizadorSegundaFaseComponent', () => {
  let component: AnalizadorSegundaFaseComponent;
  let fixture: ComponentFixture<AnalizadorSegundaFaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnalizadorSegundaFaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AnalizadorSegundaFaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
