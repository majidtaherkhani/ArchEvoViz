# Commit 3510dbfc
- Date: 2016-09-20
- Churn: 144975
### Added classes
- PetClinicApplication
- PetResource
### Removed classes
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
- PetController
- PetTypeFormatter
- SpringDataOwnerRepository
- SpringDataPetRepository
- SpringDataVetRepository
- SpringDataVisitRepository
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
- PetRepository
- PetType
- PetValidator
- Specialty
- Vet
- VetRepository
- VetResource
- Vets
- Visit
- VisitController
- VisitRepository

### Added relationships
- PetResource --> ClinicService

### Removed relationships
- JdbcOwnerRepositoryImpl --> VisitRepository
- JdbcPetRepositoryImpl --> OwnerRepository
- JdbcPetRepositoryImpl --> VisitRepository
- OwnerRepository <|-- SpringDataOwnerRepository
- OwnerRepository <|.. JdbcOwnerRepositoryImpl
- OwnerRepository <|.. JpaOwnerRepositoryImpl
- Pet <|-- JdbcPet
- PetController --> ClinicService
- PetRepository <|-- SpringDataPetRepository
- PetRepository <|.. JdbcPetRepositoryImpl
- PetRepository <|.. JpaPetRepositoryImpl
- PetTypeFormatter --> ClinicService
- VetRepository <|-- SpringDataVetRepository
- VetRepository <|.. JdbcVetRepositoryImpl
- VetRepository <|.. JpaVetRepositoryImpl
- VisitRepository <|-- SpringDataVisitRepository
- VisitRepository <|.. JdbcVisitRepositoryImpl
- VisitRepository <|.. JpaVisitRepositoryImpl

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
- VetResource --> ClinicService
- Visit --> Pet
- VisitController --> ClinicService