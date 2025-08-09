# Commit 06ddea85
- Date: 2016-12-08
- Churn: 819
### Added classes
- ApiGatewayController
- CustomersServiceApplication
- CustomersServiceClient
- OwnerDetails
- PetDetails
- PetRequest
- VisitDetails
- VisitsServiceClient
- ZipkinServer
### Removed classes
- BaseEntity
- ClientsServiceApplication
- NamedEntity
- OwnerService
- Person
- PetService
- PetValidator
- VetService
- Vets
- VisitService
### Unchanged classes
- ApiGatewayApplication
- CacheConfig
- CallMonitoringAspect
- ConfigServerApplication
- DiscoveryServerApplication
- Monitored
- MonitoringConfig
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
- WebConfig

### Added relationships
- ApiGatewayController --> CustomersServiceClient
- ApiGatewayController --> VisitsServiceClient
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
- CacheConfig --> VetsProperties
- Pet --> Owner
- Pet --> PetType