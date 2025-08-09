# Commit 536e7e9a
- Date: 2016-11-12
- Churn: 746
### Added classes
- AbstractResourceController
- OwnerService
- PetService
- PetclinicProperties
- VetService
- VisitService
### Removed classes
- ClinicService
- ClinicServiceImpl
### Unchanged classes
- BaseEntity
- CacheConfig
- CallMonitoringAspect
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
- VisitResource
- WebConfig

### Added relationships
- AbstractResourceController <|-- OwnerResource
- AbstractResourceController <|-- PetResource
- AbstractResourceController <|-- VetResource
- AbstractResourceController <|-- VisitResource
- OwnerResource --> OwnerService
- OwnerService --> OwnerRepository
- PetResource --> OwnerService
- PetResource --> PetService
- PetService --> PetRepository
- VetResource --> VetService
- VetService --> VetRepository
- VisitResource --> PetService
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
- VisitResource --> ClinicService

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
- Visit --> Pet