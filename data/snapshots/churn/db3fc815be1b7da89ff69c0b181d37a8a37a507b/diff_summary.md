# Commit db3fc815
- Date: 2016-09-19
- Churn: 1682
### Added classes
- PetClinicApplication
- PetResource
### Removed classes
- CrashController
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
- EntityUtils
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