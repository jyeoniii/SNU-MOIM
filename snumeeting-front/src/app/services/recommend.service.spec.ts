import { TestBed, inject } from '@angular/core/testing';
import {HttpModule} from '@angular/http';

import { RecommendService } from './recommend.service';


describe('RecommendService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RecommendService],
      imports: [ HttpModule ]
    });
  });

  it('should be created', inject([RecommendService], (service: RecommendService) => {
    expect(service).toBeTruthy();
  }));
});
