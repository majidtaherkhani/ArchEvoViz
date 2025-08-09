# Commit 872c7d5e
- Date: 2016-10-23
- Churn: 465
### Added classes
- CacheConfig
- VisitResource
- WebConfig
### Removed classes
- VisitController
### Unchanged classes
- BaseEntity
- CallMonitoringAspect
- ClinicService
- ClinicServiceImpl
- NamedEntity
- Owner
- OwnerRepository
- OwnerResource
- Person
- Pet
- PetClinicApplication
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
- VisitResource --> ClinicService

### Removed relationships
- VisitController --> ClinicService

### Unchanged relationships
- BaseEntity <|-- NamedEntity
- BaseEntity <|-- Person
- BaseEntity <|-- Visit
- ClinicService <|.. ClinicServiceImpl
- ClinicServiceImpl --> OwnerRepository
- ClinicServiceImpl --> PetRepository
- ClinicServiceImpl --> VetRepository
- ClinicServiceImpl --> VisitRepository
- NamedEntity <|-- Pet
- NamedEntity <|-- PetType
- NamedEntity <|-- Specialty
- OwnerResource --> ClinicService
- Person <|-- Owner
- Person <|-- Vet
- Pet --> Owner
- Pet --> PetType
- PetResource --> ClinicService
- VetResource --> ClinicService
- Visit --> Pet