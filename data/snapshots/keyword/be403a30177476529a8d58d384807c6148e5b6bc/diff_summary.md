# Commit be403a30
- Date: 2013-02-26
- Churn: 97
### Added classes
- VetsAtomView
### Removed classes
- VisitsAtomView
### Unchanged classes
- BaseEntity
- CallMonitoringAspect
- ClinicService
- ClinicServiceImpl
- CrashController
- EntityUtils
- JdbcOwnerRepositoryImpl
- JdbcPet
- JdbcPetRepositoryImpl
- JdbcPetRowMapper
- JdbcVetRepositoryImpl
- JdbcVisitRepositoryImpl
- JpaOwnerRepositoryImpl
- JpaPetRepositoryImpl
- JpaVetRepositoryImpl
- JpaVisitRepositoryImpl
- NamedEntity
- Owner
- OwnerController
- OwnerRepository
- Person
- Pet
- PetController
- PetRepository
- PetType
- PetTypeFormatter
- PetValidator
- Specialty
- SpringDataPetRepository
- SpringDataVetRepository
- SpringDataVisitRepository
- Vet
- VetController
- VetRepository
- Vets
- Visit
- VisitController
- VisitRepository

### Added relationships
- OwnerController --> ClinicService

### Removed relationships
- OwnerController --> OwnerRepository

### Unchanged relationships
- BaseEntity <|-- NamedEntity
- BaseEntity <|-- Person
- BaseEntity <|-- Visit
- ClinicService <|.. ClinicServiceImpl
- ClinicServiceImpl --> OwnerRepository
- ClinicServiceImpl --> PetRepository
- ClinicServiceImpl --> VetRepository
- ClinicServiceImpl --> VisitRepository
- JdbcOwnerRepositoryImpl --> VisitRepository
- JdbcPetRepositoryImpl --> OwnerRepository
- JdbcPetRepositoryImpl --> VisitRepository
- NamedEntity <|-- Pet
- NamedEntity <|-- PetType
- NamedEntity <|-- Specialty
- OwnerRepository <|.. JdbcOwnerRepositoryImpl
- OwnerRepository <|.. JpaOwnerRepositoryImpl
- Person <|-- Owner
- Person <|-- Vet
- Pet --> Owner
- Pet --> PetType
- Pet <|-- JdbcPet
- PetController --> ClinicService
- PetRepository <|-- SpringDataPetRepository
- PetRepository <|.. JdbcPetRepositoryImpl
- PetRepository <|.. JpaPetRepositoryImpl
- PetTypeFormatter --> ClinicService
- VetController --> ClinicService
- VetRepository <|-- SpringDataVetRepository
- VetRepository <|.. JdbcVetRepositoryImpl
- VetRepository <|.. JpaVetRepositoryImpl
- Visit --> Pet
- VisitController --> ClinicService
- VisitRepository <|-- SpringDataVisitRepository
- VisitRepository <|.. JdbcVisitRepositoryImpl
- VisitRepository <|.. JpaVisitRepositoryImpl