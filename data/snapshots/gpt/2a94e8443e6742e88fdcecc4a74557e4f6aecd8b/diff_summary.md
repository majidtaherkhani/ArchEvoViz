# Commit 2a94e844
- Date: 2016-11-12
- Churn: 1296
### Added classes
- ClientsServiceApplication
- ConfigServerApplication
- DiscoveryServerApplication
- VetsServiceApplication
- VisitsServiceApplication
### Removed classes
- PetClinicApplication
### Unchanged classes
- AbstractResourceController
- BaseEntity
- CacheConfig
- CallMonitoringAspect
- NamedEntity
- Owner
- OwnerRepository
- OwnerResource
- OwnerService
- Person
- Pet
- PetRepository
- PetResource
- PetService
- PetType
- PetValidator
- PetclinicProperties
- Specialty
- Vet
- VetRepository
- VetResource
- VetService
- Vets
- Visit
- VisitRepository
- VisitResource
- VisitService
- WebConfig

### Removed relationships
- AbstractResourceController <|-- OwnerResource
- AbstractResourceController <|-- PetResource
- AbstractResourceController <|-- VetResource
- AbstractResourceController <|-- VisitResource
- Visit --> Pet
- VisitResource --> PetService

### Unchanged relationships
- BaseEntity <|-- NamedEntity
- BaseEntity <|-- Person
- BaseEntity <|-- Visit
- NamedEntity <|-- Pet
- NamedEntity <|-- PetType
- NamedEntity <|-- Specialty
- OwnerResource --> OwnerService
- OwnerService --> OwnerRepository
- Person <|-- Owner
- Person <|-- Vet
- Pet --> Owner
- Pet --> PetType
- PetResource --> OwnerService
- PetResource --> PetService
- PetService --> PetRepository
- VetResource --> VetService
- VetService --> VetRepository
- VisitResource --> VisitService
- VisitService --> VisitRepository