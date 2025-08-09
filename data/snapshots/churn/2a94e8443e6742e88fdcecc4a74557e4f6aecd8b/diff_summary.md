# Commit 2a94e844
- Date: 2016-11-12
- Churn: 1296
### Added classes
- AbstractResourceController
- CacheConfig
- ClientsServiceApplication
- ConfigServerApplication
- DiscoveryServerApplication
- OwnerService
- PetService
- PetclinicProperties
- VetService
- VetsServiceApplication
- VisitResource
- VisitService
- VisitsServiceApplication
- WebConfig
### Removed classes
- ClinicService
- ClinicServiceImpl
- PetClinicApplication
- VisitController
### Unchanged classes
- BaseEntity
- CallMonitoringAspect
- NamedEntity
- Owner
- OwnerRepository
- OwnerResource
- Person
- Pet
- PetRepository
- PetResource
- PetType
- PetValidator
- Specialty
- Vet
- VetRepository
- VetResource
- Vets
- Visit
- VisitRepository

### Added relationships
- OwnerResource --> OwnerService
- OwnerService --> OwnerRepository
- PetResource --> OwnerService
- PetResource --> PetService
- PetService --> PetRepository
- VetResource --> VetService
- VetService --> VetRepository
- VisitResource --> VisitService
- VisitService --> VisitRepository

### Removed relationships
- ClinicService <|.. ClinicServiceImpl
- ClinicServiceImpl --> OwnerRepository
- ClinicServiceImpl --> PetRepository
- ClinicServiceImpl --> VetRepository
- ClinicServiceImpl --> VisitRepository
- OwnerResource --> ClinicService
- PetResource --> ClinicService
- VetResource --> ClinicService
- Visit --> Pet
- VisitController --> ClinicService

### Unchanged relationships
- BaseEntity <|-- NamedEntity
- BaseEntity <|-- Person
- BaseEntity <|-- Visit
- NamedEntity <|-- Pet
- NamedEntity <|-- PetType
- NamedEntity <|-- Specialty
- Person <|-- Owner
- Person <|-- Vet
- Pet --> Owner
- Pet --> PetType