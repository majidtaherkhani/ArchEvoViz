/*
 * Copyright 2002-2013 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.springframework.samples.petclinic.boundary.web.visit;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.samples.petclinic.domain.model.pet.PetService;
import org.springframework.samples.petclinic.domain.model.visit.Visit;
import org.springframework.samples.petclinic.domain.model.visit.VisitService;
import org.springframework.samples.petclinic.support.web.AbstractResourceController;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

/**
 * @author Juergen Hoeller
 * @author Ken Krebs
 * @author Arjen Poutsma
 * @author Michael Isvy
 */
@RestController
public class VisitResource extends AbstractResourceController {

    private final VisitService visitService;

    private final PetService petService;

    @Autowired
    public VisitResource(VisitService visitService, PetService petService) {
        this.visitService = visitService;
        this.petService = petService;
    }

    @PostMapping("/owners/{ownerId}/pets/{petId}/visits")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void create(
            @Valid @RequestBody Visit visit,
            @PathVariable("petId") int petId) {

        petService.findPetById(petId).addVisit(visit);
        visitService.saveVisit(visit);
    }

    @GetMapping("/owners/{ownerId}/pets/{petId}/visits")
    public Object visits(@PathVariable("petId") int petId) {
        return petService.findPetById(petId).getVisits();
    }
}
