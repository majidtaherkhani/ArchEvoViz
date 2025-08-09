# Commit 39f6670e
- Date: 2024-01-05
- Churn: 139
### Added classes
- ApiGatewayController
- CustomersServiceClient
- Mapper
- MetricConfig
- OwnerDetails
- OwnerEntityMapper
- PetDetails
- ResourceNotFoundException
- SpringBootAdminApplication
- VisitDetails
- Visits
- VisitsServiceClient
### Removed classes
- BaseEntity
- CallMonitoringAspect
- Monitored
- MonitoringConfig
- NamedEntity
- OwnerService
- Person
- PetService
- PetValidator
- VetService
- Vets
- VisitService
- WebConfig
### Unchanged classes
- ApiGatewayApplication
- CacheConfig
- ConfigServerApplication
- CustomersServiceApplication
- DiscoveryServerApplication
- Owner
- OwnerRepository
- OwnerResource
- Pet
- PetRepository
- PetResource
- PetType
- Specialty
- Vet
- VetRepository
- VetResource
- VetsProperties
- VetsServiceApplication
- Visit
- VisitRepository
- VisitResource
- VisitsServiceApplication

### Added relationships
- ApiGatewayController --> CustomersServiceClient
- ApiGatewayController --> VisitsServiceClient
- Mapper <|.. OwnerEntityMapper
- OwnerResource --> OwnerEntityMapper
- OwnerResource --> OwnerRepository
- PetDetails --> PetType
- PetResource --> OwnerRepository
- PetResource --> PetRepository
- VetResource --> VetRepository
- VisitResource --> VisitRepository

### Removed relationships
- BaseEntity <|-- NamedEntity
- BaseEntity <|-- Person
- BaseEntity <|-- Visit
- CacheConfig --> VetsProperties
- NamedEntity <|-- Pet
- NamedEntity <|-- PetType
- NamedEntity <|-- Specialty
- OwnerResource --> OwnerService
- OwnerService --> OwnerRepository
- Person <|-- Owner
- Person <|-- Vet
- PetResource --> OwnerService
- PetResource --> PetService
- PetService --> PetRepository
- VetResource --> VetService
- VetService --> VetRepository
- VisitResource --> VisitService
- VisitService --> VisitRepository

### Unchanged relationships
- Pet --> Owner
- Pet --> PetType