# Architecture Guide

This guide provides a comprehensive overview of Eneo's technical architecture, design patterns, and system components.

---

## 🏗️ System Overview

Eneo follows a **microservices architecture** with **domain-driven design** principles, built for scalability, maintainability, and democratic AI governance.

### Core Principles

- **🏛️ Domain-Driven Design**: Business logic organized by domain boundaries
- **🔄 Event-Driven Architecture**: Asynchronous processing via Redis pub/sub
- **🔌 API-First Design**: OpenAPI specification with auto-generated documentation
- **🎯 Multi-Tenancy**: Secure isolation between organizations
- **🚀 Real-Time Communication**: WebSockets and Server-Sent Events
- **🔒 Security by Design**: Built-in compliance and access control

---

## 🗄️ High-Level Architecture

<details>
<summary>🔍 Click to view complete system architecture</summary>

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOB[Mobile Apps]
        API_CLIENT[API Clients]
    end
    
    subgraph "Edge Layer"
        CDN[CDN/CloudFlare]
        LB[Load Balancer]
    end
    
    subgraph "Gateway Layer"
        TR[Traefik<br/>Reverse Proxy<br/>SSL Termination]
    end
    
    subgraph "Application Layer"
        FE[SvelteKit Frontend<br/>Node.js Server<br/>Port 3000]
        BE[FastAPI Backend<br/>Python/Uvicorn<br/>Port 8000]
        WK[ARQ Workers<br/>Background Tasks]
    end
    
    subgraph "Domain Services"
        AUTH[Authentication<br/>Service]
        SPACES[Spaces<br/>Management]
        ASSIST[Assistants<br/>Service]
        FILES[File Processing<br/>Service]
        AI[AI Integration<br/>Service]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL 16<br/>+ pgvector<br/>Vector Search)]
        REDIS[(Redis<br/>Cache/Queue/PubSub)]
        FS[File Storage<br/>Local/Cloud]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI API]
        ANTHROPIC[Anthropic API]
        AZURE[Azure OpenAI]
        LOCAL[Local AI Models]
        OAUTH[OAuth Providers]
    end
    
    WEB --> CDN
    MOB --> CDN
    API_CLIENT --> CDN
    CDN --> LB
    LB --> TR
    
    TR --> FE
    TR --> BE
    
    FE --> BE
    BE --> AUTH
    BE --> SPACES
    BE --> ASSIST
    BE --> FILES
    BE --> AI
    
    WK --> REDIS
    WK --> DB
    WK --> FS
    
    AUTH --> DB
    SPACES --> DB
    ASSIST --> DB
    FILES --> DB
    AI --> OPENAI
    AI --> ANTHROPIC
    AI --> AZURE
    AI --> LOCAL
    
    BE --> DB
    BE --> REDIS
    BE --> FS
    
    AUTH --> OAUTH
    
    style FE fill:#f3e5f5
    style BE fill:#e8f5e8
    style WK fill:#fff3e0
    style DB fill:#fce4ec
    style REDIS fill:#f1f8e9
    style TR fill:#e1f5fe
```

</details>

---

## 🏢 Domain-Driven Design Structure

Eneo implements DDD patterns with clear domain boundaries and consistent architectural patterns.

### Domain Organization

```
backend/src/intric/
├── assistants/           # AI Assistant Management Domain
├── spaces/              # Collaborative Workspaces Domain
├── users/               # User Management Domain
├── completion_models/   # AI Model Integration Domain
├── embedding_models/    # Vector Search Domain
├── files/               # Document Processing Domain
├── sessions/            # Conversation Management Domain
├── authentication/     # Security and Access Control Domain
├── groups_legacy/       # User Groups Domain (Legacy)
├── tenants/            # Multi-tenancy Domain
└── workflows/          # Business Process Automation Domain
```

### Domain Pattern Structure

Each domain follows a consistent layered architecture:

<details>
<summary>📁 Click to view domain structure pattern</summary>

```
domain_name/
├── api/                           # Presentation Layer
│   ├── domain_models.py          # Pydantic schemas for API
│   ├── domain_router.py          # FastAPI route definitions
│   └── domain_assembler.py       # Domain-to-API transformation
├── application/                   # Application Layer
│   └── domain_service.py         # Business logic and use cases
├── domain/                        # Domain Layer
│   ├── domain.py                 # Domain entities and value objects
│   └── domain_repo.py            # Repository interfaces
├── infrastructure/               # Infrastructure Layer
│   └── domain_repo_impl.py       # Repository implementations
├── domain_factory.py             # Domain object creation
└── __init__.py
```

**Layer Responsibilities:**
- **API Layer**: HTTP request/response handling, data validation
- **Application Layer**: Business use cases, orchestration
- **Domain Layer**: Core business logic, entities, rules
- **Infrastructure Layer**: Database access, external services

</details>

---

## 🖥️ Frontend Architecture

### SvelteKit Application Structure

```mermaid
graph LR
    subgraph "SvelteKit Frontend"
        ROUTES[File-based Routing<br/>src/routes/]
        COMPONENTS[Reusable Components<br/>src/lib/components/]
        STORES[State Management<br/>Svelte Stores]
        SERVICES[API Services<br/>@intric/intric-js]
        I18N[Internationalization<br/>Paraglide-JS]
    end
    
    subgraph "UI Layer"
        PAGES[Pages/Routes]
        LAYOUTS[Layout Components]
        WIDGETS[UI Widgets]
    end
    
    subgraph "State Layer"
        AUTH_STORE[Authentication Store]
        SPACE_STORE[Space Store]
        CHAT_STORE[Chat Store]
        THEME_STORE[Theme Store]
    end
    
    ROUTES --> PAGES
    COMPONENTS --> LAYOUTS
    COMPONENTS --> WIDGETS
    STORES --> AUTH_STORE
    STORES --> SPACE_STORE
    STORES --> CHAT_STORE
    STORES --> THEME_STORE
    
    SERVICES --> PAGES
    I18N --> PAGES
```

### Key Frontend Technologies

- **Framework**: SvelteKit with TypeScript
- **Package Manager**: pnpm with workspace support
- **UI Components**: Custom component library (@intric/ui)
- **Styling**: Tailwind CSS v4
- **API Client**: Type-safe client (@intric/intric-js)
- **State Management**: Svelte stores with reactive updates
- **Internationalization**: Paraglide-JS for Swedish/English
- **Build Tool**: Vite for development and production builds

---

## ⚙️ Backend Architecture

### FastAPI Application Structure

<details>
<summary>🔍 Click to view backend architecture diagram</summary>

```mermaid
graph TB
    subgraph "HTTP Layer"
        ROUTES[FastAPI Routers]
        MIDDLEWARE[Middleware Stack]
        DEPS[Dependency Injection]
    end
    
    subgraph "Application Layer"
        SERVICES[Domain Services]
        FACTORIES[Domain Factories]
        REPOS[Repository Layer]
    end
    
    subgraph "Domain Layer"
        ENTITIES[Domain Entities]
        VALUE_OBJECTS[Value Objects]
        DOMAIN_SERVICES[Domain Services]
        EVENTS[Domain Events]
    end
    
    subgraph "Infrastructure Layer"
        ORM[SQLAlchemy ORM]
        MIGRATIONS[Alembic Migrations]
        CACHE[Redis Cache]
        QUEUE[ARQ Task Queue]
        STORAGE[File Storage]
        AI_CLIENTS[AI Provider Clients]
    end
    
    ROUTES --> SERVICES
    MIDDLEWARE --> ROUTES
    DEPS --> SERVICES
    
    SERVICES --> FACTORIES
    SERVICES --> REPOS
    FACTORIES --> ENTITIES
    REPOS --> ORM
    
    ENTITIES --> VALUE_OBJECTS
    ENTITIES --> DOMAIN_SERVICES
    DOMAIN_SERVICES --> EVENTS
    
    ORM --> MIGRATIONS
    CACHE --> QUEUE
    STORAGE --> AI_CLIENTS
    
    style ROUTES fill:#e8f5e8
    style SERVICES fill:#f3e5f5
    style ENTITIES fill:#fff3e0
    style ORM fill:#fce4ec
```

</details>

### Core Backend Components

**Framework Stack:**
- **FastAPI**: Modern async web framework
- **SQLAlchemy**: ORM with async support
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization
- **ARQ**: Async Redis Queue for background tasks

**Architecture Patterns:**
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Complex object creation
- **Dependency Injection**: Service composition
- **Event Sourcing**: Domain event handling
- **CQRS**: Command Query Responsibility Segregation

---

## 💾 Data Architecture

### Database Design

<details>
<summary>🗄️ Click to view database schema overview</summary>

```mermaid
erDiagram
    TENANTS ||--o{ USERS : contains
    TENANTS ||--o{ SPACES : contains
    TENANTS ||--o{ ROLES : defines
    
    USERS ||--o{ SESSIONS : creates
    USERS }o--o{ USER_GROUPS : belongs_to
    USERS ||--o{ API_KEYS : owns
    
    SPACES ||--o{ ASSISTANTS : contains
    SPACES ||--o{ INFO_BLOBS : stores
    SPACES }o--o{ USER_GROUPS : accessible_by
    
    ASSISTANTS ||--o{ SESSIONS : powers
    ASSISTANTS }o--|| COMPLETION_MODELS : uses
    ASSISTANTS }o--o{ PROMPTS : configured_with
    
    SESSIONS ||--o{ QUESTIONS : contains
    QUESTIONS }o--o{ INFO_BLOBS : references
    QUESTIONS }o--|| FILES : may_include
    
    INFO_BLOBS ||--o{ INFO_BLOB_CHUNKS : split_into
    INFO_BLOB_CHUNKS }o--|| EMBEDDING_MODELS : embedded_by
    
    COMPLETION_MODELS }o--o{ USER_GROUPS : available_to
    EMBEDDING_MODELS }o--o{ USER_GROUPS : available_to
    
    FILES ||--o{ TRANSCRIPTIONS : may_have
    
    TENANTS {
        uuid id PK
        string name
        string display_name
        jsonb settings
        timestamp created_at
        timestamp updated_at
    }
    
    USERS {
        uuid id PK
        uuid tenant_id FK
        string email
        string username
        string password_hash
        jsonb settings
        timestamp deleted_at
        timestamp created_at
        timestamp updated_at
    }
    
    SPACES {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK
        string name
        string description
        jsonb settings
        timestamp created_at
        timestamp updated_at
    }
    
    ASSISTANTS {
        uuid id PK
        uuid space_id FK
        uuid completion_model_id FK
        string name
        string description
        jsonb configuration
        timestamp created_at
        timestamp updated_at
    }
```

</details>

### Key Data Patterns

**Multi-tenancy:**
- All entities include `tenant_id` for data isolation
- Row-level security ensures tenant separation
- UUID primary keys prevent enumeration attacks

**Soft Deletes:**
- Users support soft deletion with `deleted_at` timestamp
- Maintains referential integrity while hiding deleted records

**Audit Trails:**
- All entities include `created_at` and `updated_at` timestamps
- Database triggers maintain accurate timestamps
- Comprehensive logging for compliance requirements

**Vector Storage:**
- PostgreSQL with pgvector extension for semantic search
- Embeddings stored alongside metadata in `info_blob_chunks`
- Efficient similarity search with indexing strategies

---

## 🔄 Real-Time Communication

### Communication Patterns

<details>
<summary>🔍 Click to view real-time architecture</summary>

```mermaid
sequenceDiagram
    participant C as Client
    participant F as Frontend
    participant B as Backend
    participant R as Redis
    participant W as Worker
    participant AI as AI Provider
    
    Note over C,AI: Chat Message Flow
    C->>F: Send message
    F->>B: POST /api/v1/questions
    B->>R: Queue background task
    B-->>F: SSE stream start
    F-->>C: Stream response start
    
    par Background Processing
        W->>R: Get task
        W->>AI: Send to AI provider
        AI-->>W: Stream response
        W->>R: Publish chunks
    and Real-time Delivery
        R->>B: Notify new chunks
        B-->>F: SSE stream chunks
        F-->>C: Update UI real-time
    end
    
    Note over C,AI: File Upload Flow
    C->>F: Upload file
    F->>B: POST /api/v1/files
    B->>R: Queue processing task
    B-->>F: WebSocket status
    F-->>C: Show upload progress
    
    W->>R: Get file task
    W->>W: Process & chunk file
    W->>R: Update status
    R->>B: Status notification
    B-->>F: WebSocket update
    F-->>C: Processing complete
```

</details>

### Real-Time Technologies

**Server-Sent Events (SSE):**
- Real-time AI response streaming
- Unidirectional server-to-client communication
- Automatic reconnection and error handling
- Browser-native support with EventSource API

**WebSockets:**
- Bidirectional real-time communication
- Background task status updates
- File upload progress tracking
- System-wide notifications

**Redis Pub/Sub:**
- Message broker for real-time events
- Scalable across multiple backend instances
- Event distribution to connected clients
- Persistent connection management

---

## 🔌 AI Integration Architecture

### AI Provider Abstraction

<details>
<summary>🤖 Click to view AI integration architecture</summary>

```mermaid
graph TB
    subgraph "Client Layer"
        CHAT[Chat Interface]
        ASSISTANT[Assistant Config]
    end
    
    subgraph "Application Layer"
        COMPLETION[Completion Service]
        MODEL_MGR[Model Manager]
        PROMPT_MGR[Prompt Manager]
    end
    
    subgraph "Abstraction Layer"
        PROVIDER_FACTORY[Provider Factory]
        BASE_CLIENT[Base AI Client]
        RESPONSE_PARSER[Response Parser]
    end
    
    subgraph "Provider Implementations"
        OPENAI_CLIENT[OpenAI Client]
        ANTHROPIC_CLIENT[Anthropic Client]
        AZURE_CLIENT[Azure Client]
        LOCAL_CLIENT[Local Model Client]
    end
    
    subgraph "External APIs"
        OPENAI_API[OpenAI API]
        ANTHROPIC_API[Anthropic API]
        AZURE_API[Azure OpenAI API]
        LOCAL_API[Local Model API]
    end
    
    CHAT --> COMPLETION
    ASSISTANT --> MODEL_MGR
    ASSISTANT --> PROMPT_MGR
    
    COMPLETION --> PROVIDER_FACTORY
    MODEL_MGR --> PROVIDER_FACTORY
    PROMPT_MGR --> BASE_CLIENT
    
    PROVIDER_FACTORY --> OPENAI_CLIENT
    PROVIDER_FACTORY --> ANTHROPIC_CLIENT
    PROVIDER_FACTORY --> AZURE_CLIENT
    PROVIDER_FACTORY --> LOCAL_CLIENT
    
    BASE_CLIENT --> RESPONSE_PARSER
    
    OPENAI_CLIENT --> OPENAI_API
    ANTHROPIC_CLIENT --> ANTHROPIC_API
    AZURE_CLIENT --> AZURE_API
    LOCAL_CLIENT --> LOCAL_API
    
    style COMPLETION fill:#e8f5e8
    style PROVIDER_FACTORY fill:#f3e5f5
    style OPENAI_CLIENT fill:#fff3e0
    style ANTHROPIC_CLIENT fill:#fff3e0
    style AZURE_CLIENT fill:#fff3e0
    style LOCAL_CLIENT fill:#fff3e0
```

</details>

### AI Integration Features

**Multi-Provider Support:**
- Unified interface for all AI providers
- Runtime provider switching
- Provider-specific optimizations
- Fallback and retry mechanisms

**Model Management:**
- Database-driven model configuration
- Dynamic model loading
- Cost and performance tracking
- Usage analytics and monitoring

**Context Management:**
- Conversation history handling
- System prompt management
- Context window optimization
- Memory management strategies

---

## 🏭 Background Processing

### ARQ Task System

<details>
<summary>⚙️ Click to view background task architecture</summary>

```mermaid
graph LR
    subgraph "Task Producers"
        API[API Endpoints]
        SCHEDULER[Scheduled Tasks]
        WEBHOOK[Webhooks]
    end
    
    subgraph "Queue System"
        REDIS_QUEUE[(Redis Queue)]
        TASK_ROUTER[Task Router]
        PRIORITY[Priority Queues]
    end
    
    subgraph "Workers"
        WORKER1[Worker 1<br/>File Processing]
        WORKER2[Worker 2<br/>AI Tasks]
        WORKER3[Worker 3<br/>Web Crawling]
        WORKER_N[Worker N<br/>General Tasks]
    end
    
    subgraph "Task Types"
        FILE_TASKS[File Processing<br/>• Document parsing<br/>• Image processing<br/>• Audio transcription]
        AI_TASKS[AI Processing<br/>• Embeddings generation<br/>• Content analysis<br/>• Batch completions]
        CRAWL_TASKS[Web Crawling<br/>• Website crawling<br/>• Content extraction<br/>• Sitemap processing]
        MAINTENANCE[Maintenance<br/>• Data cleanup<br/>• Cache warming<br/>• Analytics]
    end
    
    API --> REDIS_QUEUE
    SCHEDULER --> REDIS_QUEUE
    WEBHOOK --> REDIS_QUEUE
    
    REDIS_QUEUE --> TASK_ROUTER
    TASK_ROUTER --> PRIORITY
    
    PRIORITY --> WORKER1
    PRIORITY --> WORKER2
    PRIORITY --> WORKER3
    PRIORITY --> WORKER_N
    
    WORKER1 --> FILE_TASKS
    WORKER2 --> AI_TASKS
    WORKER3 --> CRAWL_TASKS
    WORKER_N --> MAINTENANCE
```

</details>

### Task Categories

**File Processing Tasks:**
- Document parsing and chunking
- Image processing and analysis
- Audio transcription
- Vector embedding generation

**AI Processing Tasks:**
- Batch AI completions
- Content summarization
- Semantic analysis
- Model fine-tuning preparation

**Web Crawling Tasks:**
- Website content extraction
- Sitemap processing
- Link discovery and validation
- Content updates and monitoring

**System Maintenance:**
- Database cleanup and optimization
- Cache warming and invalidation
- Analytics data processing
- Security audits and checks

---

## 🔒 Security Architecture

### Multi-Layer Security

<details>
<summary>🛡️ Click to view security architecture</summary>

```mermaid
graph TB
    subgraph "Perimeter Security"
        WAF[Web Application Firewall]
        DDoS[DDoS Protection]
        RATE_LIMIT[Rate Limiting]
    end
    
    subgraph "Application Security"
        AUTH[Authentication Layer]
        AUTHZ[Authorization Layer]
        JWT[JWT Token Management]
        API_KEYS[API Key Management]
    end
    
    subgraph "Data Security"
        ENCRYPTION[Data Encryption]
        PII[PII Protection]
        AUDIT[Audit Logging]
        BACKUP[Secure Backups]
    end
    
    subgraph "Infrastructure Security"
        TLS[TLS/SSL Termination]
        SECRETS[Secret Management]
        NETWORK[Network Isolation]
        MONITORING[Security Monitoring]
    end
    
    subgraph "Compliance"
        GDPR[GDPR Compliance]
        AI_ACT[EU AI Act]
        AUDIT_TRAIL[Audit Trails]
        DATA_RETENTION[Data Retention]
    end
    
    WAF --> AUTH
    DDoS --> AUTH
    RATE_LIMIT --> AUTH
    
    AUTH --> AUTHZ
    AUTHZ --> JWT
    JWT --> API_KEYS
    
    ENCRYPTION --> PII
    PII --> AUDIT
    AUDIT --> BACKUP
    
    TLS --> SECRETS
    SECRETS --> NETWORK
    NETWORK --> MONITORING
    
    GDPR --> AI_ACT
    AI_ACT --> AUDIT_TRAIL
    AUDIT_TRAIL --> DATA_RETENTION
    
    style AUTH fill:#fce4ec
    style ENCRYPTION fill:#e8f5e8
    style GDPR fill:#fff3e0
    style TLS fill:#e1f5fe
```

</details>

### Security Features

**Authentication & Authorization:**
- JWT-based authentication with secure token management
- Role-based access control (RBAC) with granular permissions
- API key authentication for service integration
- Multi-factor authentication support

**Data Protection:**
- AES-256 encryption for sensitive data at rest
- TLS 1.3 for data in transit
- PII detection and masking
- Secure password hashing with bcrypt

**Compliance:**
- GDPR compliance with data subject rights
- EU AI Act readiness with transparency features
- Comprehensive audit logging
- Data retention policy enforcement

---

## 📊 Monitoring and Observability

### Observability Stack

```mermaid
graph LR
    subgraph "Data Collection"
        LOGS[Application Logs]
        METRICS[System Metrics]
        TRACES[Request Traces]
        EVENTS[Business Events]
    end
    
    subgraph "Processing"
        LOG_PROC[Log Processing]
        METRIC_PROC[Metric Aggregation]
        TRACE_PROC[Trace Correlation]
        EVENT_PROC[Event Analysis]
    end
    
    subgraph "Storage"
        LOG_STORE[(Log Storage)]
        METRIC_STORE[(Metrics DB)]
        TRACE_STORE[(Trace Storage)]
        EVENT_STORE[(Event Store)]
    end
    
    subgraph "Visualization"
        DASHBOARDS[System Dashboards]
        ALERTS[Alert Management]
        REPORTS[Business Reports]
        ANALYTICS[Usage Analytics]
    end
    
    LOGS --> LOG_PROC --> LOG_STORE --> DASHBOARDS
    METRICS --> METRIC_PROC --> METRIC_STORE --> DASHBOARDS
    TRACES --> TRACE_PROC --> TRACE_STORE --> ALERTS
    EVENTS --> EVENT_PROC --> EVENT_STORE --> REPORTS
    
    DASHBOARDS --> ANALYTICS
    ALERTS --> ANALYTICS
    REPORTS --> ANALYTICS
```

### Monitoring Capabilities

**System Monitoring:**
- Application performance metrics
- Resource utilization tracking
- Database query performance
- Background task monitoring

**Business Monitoring:**
- User engagement analytics
- AI usage patterns
- Cost optimization metrics
- Feature adoption tracking

**Security Monitoring:**
- Authentication attempt tracking
- Authorization failure alerts
- Suspicious activity detection
- Compliance violation monitoring

---

## 🚀 Deployment Architecture

### Container Architecture

<details>
<summary>📦 Click to view container deployment architecture</summary>

```mermaid
graph TB
    subgraph "Container Registry"
        FRONTEND_IMG[eneo-frontend:latest]
        BACKEND_IMG[eneo-backend:latest]
        BASE_IMGS[Base Images<br/>Node.js, Python, PostgreSQL, Redis]
    end
    
    subgraph "Deployment Environment"
        COMPOSE[Docker Compose]
        K8S[Kubernetes]
        PODMAN[Podman/RHEL]
    end
    
    subgraph "Runtime Containers"
        TRAEFIK_C[Traefik Container<br/>Reverse Proxy]
        FRONTEND_C[Frontend Container<br/>SvelteKit Server]
        BACKEND_C[Backend Container<br/>FastAPI Server]
        WORKER_C[Worker Container<br/>ARQ Tasks]
        DB_C[Database Container<br/>PostgreSQL + pgvector]
        REDIS_C[Redis Container<br/>Cache/Queue]
    end
    
    subgraph "Persistent Storage"
        DB_VOL[Database Volume]
        REDIS_VOL[Redis Volume]
        BACKEND_VOL[Backend Data Volume]
        CERT_VOL[Certificate Volume]
    end
    
    FRONTEND_IMG --> COMPOSE
    BACKEND_IMG --> COMPOSE
    BASE_IMGS --> COMPOSE
    
    COMPOSE --> FRONTEND_C
    COMPOSE --> BACKEND_C
    COMPOSE --> WORKER_C
    
    K8S --> FRONTEND_C
    K8S --> BACKEND_C
    K8S --> WORKER_C
    
    PODMAN --> FRONTEND_C
    PODMAN --> BACKEND_C
    PODMAN --> WORKER_C
    
    TRAEFIK_C --> FRONTEND_C
    TRAEFIK_C --> BACKEND_C
    
    DB_C --> DB_VOL
    REDIS_C --> REDIS_VOL
    BACKEND_C --> BACKEND_VOL
    TRAEFIK_C --> CERT_VOL
    
    style COMPOSE fill:#e1f5fe
    style FRONTEND_C fill:#f3e5f5
    style BACKEND_C fill:#e8f5e8
    style WORKER_C fill:#fff3e0
    style DB_C fill:#fce4ec
    style REDIS_C fill:#f1f8e9
```

</details>

### Deployment Strategies

**Development:**
- Docker Compose for local development
- DevContainer for consistent development environment
- Hot reloading for rapid iteration
- Simplified networking and storage

**Production:**
- Multi-stage Docker builds for optimization
- Traefik for SSL termination and load balancing
- Persistent volumes for data storage
- Health checks and restart policies

**Enterprise:**
- Kubernetes orchestration for high availability
- Podman for RHEL/enterprise environments
- SystemD integration for service management
- Advanced monitoring and logging

---

## 📈 Scalability Considerations

### Horizontal Scaling

**Stateless Services:**
- Frontend and backend services designed as stateless
- Load balancing across multiple instances
- Session data stored in Redis for sharing
- Database connection pooling

**Background Processing:**
- ARQ workers can be scaled independently
- Queue-based task distribution
- Priority-based task processing
- Worker specialization by task type

**Database Scaling:**
- Read replicas for query scaling
- Connection pooling and optimization
- Vector index optimization for pgvector
- Partitioning strategies for large datasets

### Performance Optimization

**Caching Strategy:**
- Redis for session and application caching
- HTTP caching with appropriate headers
- Database query result caching
- Static asset caching via CDN

**AI Provider Optimization:**
- Request batching and queuing
- Response caching for similar queries
- Provider failover and retry logic
- Cost optimization through model selection

---

## 🔧 Development Patterns

### Code Organization

**Backend Patterns:**
```python
# Domain entity example
@dataclass
class Assistant:
    id: UUID
    space_id: UUID
    name: str
    description: str
    system_prompt: str
    completion_model_id: UUID
    
    def update_configuration(self, config: AssistantConfig) -> None:
        # Domain logic here
        pass

# Repository pattern
class AssistantRepository(Protocol):
    async def find_by_id(self, id: UUID) -> Optional[Assistant]:
        ...
    async def save(self, assistant: Assistant) -> None:
        ...

# Service layer
class AssistantService:
    def __init__(self, repo: AssistantRepository):
        self._repo = repo
    
    async def create_assistant(self, request: CreateAssistantRequest) -> Assistant:
        # Business logic here
        pass
```

**Frontend Patterns:**
```typescript
// Svelte store pattern
export const assistantStore = writable<Assistant[]>([]);

// Service pattern
class AssistantService {
    async createAssistant(data: CreateAssistantRequest): Promise<Assistant> {
        return await apiClient.post('/assistants', data);
    }
}

// Component composition
<script lang="ts">
    import { assistantStore } from '$lib/stores/assistant';
    import AssistantCard from '$lib/components/AssistantCard.svelte';
</script>

{#each $assistantStore as assistant}
    <AssistantCard {assistant} />
{/each}
```

---

## 📚 Architecture Decision Records

### Key Architectural Decisions

**1. Domain-Driven Design Adoption**
- **Decision**: Organize code by business domains rather than technical layers
- **Rationale**: Better maintainability and team ownership
- **Trade-offs**: Increased complexity for simple features

**2. Multi-Provider AI Integration**
- **Decision**: Abstract AI providers behind unified interface
- **Rationale**: Vendor independence and flexibility
- **Trade-offs**: Additional complexity in provider-specific optimizations

**3. Real-Time Communication Strategy**
- **Decision**: Use SSE for streaming, WebSockets for bidirectional communication
- **Rationale**: Browser compatibility and simplicity
- **Trade-offs**: Separate connection management required

**4. Container-First Deployment**
- **Decision**: Docker/Podman as primary deployment method
- **Rationale**: Consistency across environments and simplified operations
- **Trade-offs**: Container orchestration complexity

---

This architecture supports Eneo's mission of democratic AI by providing a scalable, maintainable, and transparent platform that can grow with the needs of public sector organizations while maintaining the highest standards of security and compliance.