import { TestBed, inject } from '@angular/core/testing';

import { MetaDataService } from './meta-data-service';

describe('MetaDataServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MetaDataService]
    });
  });

  it('should be created', inject([MetaDataService], (service: MetaDataService) => {
    expect(service).toBeTruthy();
  }));
});
