# Commit 79b527a3
- Date: 2024-12-27
- Churn: 1393
### Added classes
- AIBeanConfiguration
- AIDataProvider
- ApiGatewayApplication
- ApiGatewayController
- CustomersServiceApplication
- CustomersServiceClient
- FallbackController
- GenAIServiceApplication
- Mapper
- MetricConfig
- OwnerDetails
- OwnerEntityMapper
- PetDetails
- ResourceNotFoundException
- SpringBootAdminApplication
- VectorStoreController
- VetsProperties
- VisitDetails
- Visits
- VisitsServiceClient
### Removed classes
- AbstractResourceController
- BaseEntity
- CallMonitoringAspect
- ClientsServiceApplication
- NamedEntity
- OwnerService
- Person
- PetService
- PetValidator
- PetclinicProperties
- VetService
- Vets
- VisitService
- WebConfig
### Unchanged classes
- CacheConfig
- ConfigServerApplication
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