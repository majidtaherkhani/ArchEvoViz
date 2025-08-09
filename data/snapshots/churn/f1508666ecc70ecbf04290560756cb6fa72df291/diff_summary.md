# Commit f1508666
- Date: 2015-06-11
- Churn: 233378
### Added classes
- OwnerResource
- SpringDataOwnerRepository
- VetResource
### Removed classes
- OwnerController
- VetController
- VetsAtomView
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
- VetRepository
- Vets
- Visit
- VisitController
- VisitRepository

### Added relationships
- OwnerRepository <|-- SpringDataOwnerRepository
- OwnerResource --> ClinicService
- VetResource --> ClinicService

### Removed relationships
- OwnerController --> ClinicService
- VetController --> ClinicService

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
- VetRepository <|-- SpringDataVetRepository
- VetRepository <|.. JdbcVetRepositoryImpl
- VetRepository <|.. JpaVetRepositoryImpl
- Visit --> Pet
- VisitController --> ClinicService
- VisitRepository <|-- SpringDataVisitRepository
- VisitRepository <|.. JdbcVisitRepositoryImpl
- VisitRepository <|.. JpaVisitRepositoryImpl