package org.springframework.samples.petclinic.domain.model.vet;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.cache.annotation.CacheResult;
import java.util.Collection;

/**
 * @author mszarlinski on 2016-10-30.
 */
@Service
public class VetService {

    private final VetRepository vetRepository;

    @Autowired
    public VetService(VetRepository vetRepository) {
        this.vetRepository = vetRepository;
    }

    @Transactional(readOnly = true)
    @CacheResult(cacheName = "vets")
    public Collection<Vet> findVets() throws DataAccessException {
        return vetRepository.findAll();
    }
}
