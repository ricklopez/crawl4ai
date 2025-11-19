# Crawl4AI Repository Structure Analysis

**Analysis Date:** 2025-11-18
**Repository:** crawl4ai
**Primary Language:** Python
**Project Type:** Web Crawling & LLM-Friendly Content Extraction Platform

---

## Executive Summary

Crawl4AI is an open-source web crawler and scraper designed to convert web content into clean, LLM-ready Markdown. The repository consists of:

- **Core Python library** (`crawl4ai/`) - Main crawling engine with async capabilities
- **Docker API Server** (`deploy/docker/`) - FastAPI-based REST API and job queue system
- **Browser Extension** (`docs/md_v2/apps/crawl4ai-assistant/`) - Chrome extension for visual schema building
- **Comprehensive Documentation** (`docs/`) - Examples, tutorials, and API documentation

The architecture follows a **strategy pattern** extensively, with clear separation between crawling logic, content extraction, markdown generation, and LLM integration.

---

## 1. File Classification by Language

### Python Files
- **Total Count:** 345 files
- **Primary Use:** Core library, API server, tests, examples
- **Major Categories:**
  - Core crawling engine
  - Strategy implementations
  - API endpoints
  - CLI tools
  - Test suites

### JavaScript Files
- **Total Count:** 47 files
- **Primary Use:** Browser automation, Chrome extension, web UI
- **Major Categories:**
  - Browser snippets (overlay removal, stealth mode)
  - Chrome extension content scripts
  - Web-based playground/monitor UIs
  - C4A Script visual builder (Blockly-based)

### HTML Files
- **Total Count:** 32 files
- **Primary Use:** Web interfaces, examples, documentation
- **Major Categories:**
  - API playground interface
  - Monitoring dashboard
  - Chrome extension UI
  - Tutorial examples

### Markdown Files
- **Total Count:** 127 files
- **Primary Use:** Documentation, guides, release notes
- **Major Categories:**
  - API documentation
  - Tutorials and examples
  - Blog posts and release notes
  - Architecture documentation

### Other Files
- **YAML/TOML:** Configuration files (pyproject.toml, mkdocs.yml, config.yml, cliff.toml)
- **JSON:** Package manifests, extension manifest
- **Dockerfile:** Container definitions for deployment

---

## 2. Directory Architecture

```
crawl4ai/
├── .prompt/                          # DotPrompt workspace (NEW - migration analysis)
│   ├── analysis/                     # Repository analysis outputs
│   ├── ir/                          # Intermediate Representation files
│   └── plan/                        # Architecture blueprints
│       ├── app/
│       │   ├── server/              # Backend service plans
│       │   └── client/              # Frontend component plans
│       ├── db/                      # Database schema plans
│       └── shared/                  # Shared utilities plans
│
├── crawl4ai/                         # Core Python library
│   ├── components/                   # Reusable components
│   ├── crawlers/                     # Specialized crawlers (Amazon, Google)
│   ├── deep_crawling/               # Deep/recursive crawling strategies
│   ├── html2text/                   # HTML to text conversion
│   ├── js_snippet/                  # Browser automation JS snippets
│   ├── legacy/                      # Deprecated/legacy code
│   ├── processors/                   # Content processors (PDF, etc.)
│   └── script/                      # Script generation utilities
│
├── deploy/docker/                    # Docker deployment & API server
│   ├── static/                      # Static web assets
│   │   ├── monitor/                 # Monitoring dashboard
│   │   └── playground/              # API playground
│   └── tests/                       # Docker API tests
│
├── docs/                            # Documentation & examples
│   ├── md_v2/                       # Version 2 documentation
│   │   ├── apps/                    # Applications
│   │   │   ├── crawl4ai-assistant/  # Chrome extension
│   │   │   └── c4a-script/          # Visual script builder
│   │   ├── api/                     # API documentation
│   │   ├── basic/                   # Basic tutorials
│   │   └── advanced/                # Advanced guides
│   ├── examples/                    # Code examples
│   └── blog/                        # Release notes & blogs
│
└── tests/                           # Test suite
```

---

## 3. Frameworks & Technologies Detected

### Backend (Python)
- **FastAPI** - REST API framework (deploy/docker/server.py)
- **Pydantic** - Data validation and settings management
- **Playwright** - Browser automation (async)
- **Patchright** - Enhanced Playwright fork
- **aiohttp** - Async HTTP client
- **aiosqlite** - Async SQLite database
- **Redis (aioredis)** - Job queue and caching
- **LiteLLM** - Multi-provider LLM integration
- **BeautifulSoup4** - HTML parsing
- **lxml** - XML/HTML processing
- **rank-bm25** - BM25 content filtering
- **NLTK** - Natural language processing

### Monitoring & Operations
- **Prometheus** - Metrics collection
- **Supervisor** - Process management
- **slowapi** - Rate limiting
- **psutil** - System monitoring

### Frontend (JavaScript/HTML)
- **Blockly** - Visual programming blocks (C4A Script builder)
- **Marked.js** - Markdown rendering
- **Vanilla JavaScript** - Chrome extension, web UIs
- **WebSocket** - Real-time streaming

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **MkDocs** - Documentation generation
- **MCP (Model Context Protocol)** - LLM tool integration

### Testing & Development
- **pytest** - Testing framework
- **uv** - Python package management
- **setuptools** - Package building

---

## 4. Backend / Frontend / Shared Boundaries

### Backend Services
**Location:** `crawl4ai/` (library) + `deploy/docker/` (API server)

**Responsibilities:**
- Web crawling orchestration
- Browser pool management
- Content extraction and transformation
- Markdown generation
- LLM integration
- Job queue processing
- Webhook notifications
- Metrics and monitoring

**Key Components:**
- `async_webcrawler.py` - Main crawler interface
- `async_crawler_strategy.py` - Core crawling logic
- `browser_manager.py` - Browser lifecycle management
- `async_dispatcher.py` - Job dispatching and rate limiting
- `server.py` - FastAPI application entry point
- `api.py` - API endpoint handlers
- `crawler_pool.py` - Browser pool management

### Frontend Components
**Location:** `docs/md_v2/apps/` + `deploy/docker/static/`

**Responsibilities:**
- Visual schema building (Chrome extension)
- API playground interface
- Real-time monitoring dashboard
- Script generation UI

**Key Components:**
1. **Chrome Extension** (`crawl4ai-assistant/`)
   - Content scripts for page interaction
   - Visual element selection
   - Schema generation
   - Script builder with recording

2. **Web Dashboards** (`deploy/docker/static/`)
   - Playground: Interactive API testing
   - Monitor: Real-time crawler status and metrics

### Shared Utilities
**Location:** `crawl4ai/` (core utilities)

**Responsibilities:**
- Data models (Pydantic)
- Type definitions
- Configuration schemas
- Utility functions

**Key Components:**
- `models.py` - CrawlResult, MarkdownGenerationResult, etc.
- `types.py` - Type aliases and imports
- `async_configs.py` - BrowserConfig, CrawlerRunConfig, LLMConfig
- `utils.py` - Shared helper functions

---

## 5. Domain Models & Business Logic

### Core Domain Models

#### 1. Crawling Domain
**File:** `crawl4ai/models.py`

**Key Models:**
- `CrawlResult` - Complete crawl result with HTML, markdown, media, links
- `AsyncCrawlResponse` - Raw browser response data
- `CrawlStatus` - Enum: QUEUED, IN_PROGRESS, COMPLETED, FAILED
- `CrawlStats` - Crawl performance metrics
- `DispatchResult` - Dispatcher execution result

#### 2. Content Domain
**Files:** `crawl4ai/models.py`, `content_scraping_strategy.py`

**Key Models:**
- `ScrapingResult` - Extracted content with media and links
- `MediaItem` - Image/video/audio metadata
- `Link` - Internal/external link with scoring
- `Media` - Collection of media items
- `Links` - Organized internal/external links

#### 3. Markdown Domain
**Files:** `crawl4ai/models.py`, `markdown_generation_strategy.py`

**Key Models:**
- `MarkdownGenerationResult` - Raw markdown, citations, references, fit markdown
- `DefaultMarkdownGenerator` - Strategy for markdown generation

#### 4. Extraction Domain
**File:** `crawl4ai/extraction_strategy.py`

**Key Models:**
- `ExtractionStrategy` - Base strategy interface
- `LLMExtractionStrategy` - LLM-based extraction
- `JsonCssExtractionStrategy` - CSS selector-based extraction
- `JsonXPathExtractionStrategy` - XPath-based extraction
- `CosineStrategy` - Semantic similarity extraction

#### 5. LLM Integration Domain
**Files:** `crawl4ai/async_configs.py`, `prompts.py`

**Key Models:**
- `LLMConfig` - Provider, model, temperature, base_url
- `TokenUsage` - Token consumption tracking
- Prompts: Block extraction, content filtering, QA generation

### Business Logic Layers

#### 1. Crawling Logic
**Primary Files:**
- `async_webcrawler.py` - Main crawler API
- `async_crawler_strategy.py` - Core crawling algorithm
- `browser_manager.py` - Browser lifecycle and session management
- `browser_profiler.py` - Browser configuration and anti-detection

**Key Workflows:**
1. **URL Processing**
   - URL validation and normalization
   - Cache lookup (BYPASS, READ_ONLY, WRITE_ONLY, ENABLED)
   - Session management
   - Rate limiting

2. **Page Rendering**
   - Browser context creation
   - Page navigation with retries
   - JavaScript execution
   - Screenshot/PDF generation
   - Network request monitoring

3. **Content Extraction**
   - HTML cleaning and scraping
   - Media extraction (images, videos, audio)
   - Link extraction and scoring
   - Table extraction

#### 2. Content Processing Logic
**Primary Files:**
- `content_scraping_strategy.py` - HTML scraping strategies
- `content_filter_strategy.py` - Content filtering strategies
- `markdown_generation_strategy.py` - Markdown conversion

**Key Workflows:**
1. **HTML Scraping**
   - Remove unwanted elements (scripts, styles, overlays)
   - Extract semantic content
   - Preserve structure for markdown

2. **Content Filtering**
   - FIT: Fast Important Text
   - BM25: Keyword relevance ranking
   - LLM: AI-powered content filtering
   - Pruning: Remove low-value content

3. **Markdown Generation**
   - HTML to markdown conversion
   - Citation generation
   - Reference extraction
   - Fit markdown optimization

#### 3. Deep Crawling Logic
**Primary Files:** `crawl4ai/deep_crawling/`
- `base_strategy.py` - Base deep crawl interface
- `bfs_strategy.py` - Breadth-first search
- `dfs_strategy.py` - Depth-first search
- `bff_strategy.py` - Best-first search with scoring
- `filters.py` - URL filtering strategies
- `scorers.py` - URL relevance scoring

**Key Workflows:**
1. **Link Discovery**
   - Extract links from pages
   - Filter by domain, content type, patterns
   - Score by relevance, authority, freshness

2. **Traversal**
   - BFS: Level-by-level exploration
   - DFS: Deep path exploration
   - Best-first: Priority queue based on scores

#### 4. LLM Integration Logic
**Primary Files:**
- `extraction_strategy.py` - LLM extraction strategies
- `content_filter_strategy.py` - LLM content filtering
- `utils.py` - LLM API interaction helpers

**Key Workflows:**
1. **Schema-based Extraction**
   - Define Pydantic schema
   - Generate extraction prompt
   - Parse LLM response to schema

2. **Content Filtering**
   - Semantic relevance scoring
   - Context-aware filtering
   - Multi-provider support (OpenAI, Anthropic, etc.)

#### 5. Job Queue Logic
**Primary Files:** `deploy/docker/`
- `job.py` - Job creation and tracking
- `api.py` - Async job handlers
- `webhook.py` - Webhook delivery service

**Key Workflows:**
1. **Job Lifecycle**
   - Create job with unique ID
   - Store in Redis with status
   - Process asynchronously
   - Track completion/failure

2. **Webhook Notifications**
   - Exponential backoff retry
   - Custom headers support
   - Payload customization
   - Delivery status tracking

---

## 6. API Endpoints Catalog

### REST API Endpoints
**Server:** `deploy/docker/server.py`
**Base URL:** `http://localhost:11235`

#### Core Crawling Endpoints

1. **POST /crawl**
   - **Purpose:** Crawl one or more URLs synchronously
   - **Request:** `CrawlRequestWithHooks` (urls, browser_config, crawler_config, hooks)
   - **Response:** List of `CrawlResult` objects
   - **Authentication:** JWT token required (if enabled)
   - **Rate Limiting:** Configured via slowapi

2. **POST /crawl/stream**
   - **Purpose:** Stream crawl results via Server-Sent Events (SSE)
   - **Request:** `CrawlRequestWithHooks`
   - **Response:** Streaming JSON objects
   - **Use Case:** Real-time progress updates for multi-URL crawls

3. **POST /md**
   - **Purpose:** Get markdown content with optional filtering
   - **Request:** `MarkdownRequest` (url, filter type, query, cache, LLM config)
   - **Response:** Markdown string
   - **Filters:** fit, raw, bm25, llm

4. **POST /html**
   - **Purpose:** Extract raw HTML from URL
   - **Request:** `HTMLRequest` (url)
   - **Response:** HTML string

5. **POST /screenshot**
   - **Purpose:** Capture screenshot of webpage
   - **Request:** `ScreenshotRequest` (url, wait_for, output_path)
   - **Response:** Base64-encoded image or file path

6. **POST /pdf**
   - **Purpose:** Generate PDF from webpage
   - **Request:** `PDFRequest` (url, output_path)
   - **Response:** PDF bytes or file path

7. **POST /execute_js**
   - **Purpose:** Execute custom JavaScript on page
   - **Request:** `JSEndpointRequest` (url, scripts[])
   - **Response:** Execution results

#### LLM & QA Endpoints

8. **GET /llm/{url:path}**
   - **Purpose:** LLM-powered Q&A using page content as context
   - **Query Params:** `q` (question), `provider`, `temperature`, `base_url`
   - **Response:** LLM answer text

9. **GET /ask**
   - **Purpose:** Alternative Q&A endpoint
   - **Query Params:** Similar to /llm
   - **Response:** LLM answer

#### Job Queue Endpoints
**Router:** `deploy/docker/job.py`

10. **POST /crawl/job**
    - **Purpose:** Create async crawl job
    - **Request:** `CrawlRequestWithHooks` + webhook config
    - **Response:** `{"task_id": "...", "status": "QUEUED"}`

11. **GET /crawl/job/{task_id}**
    - **Purpose:** Check job status
    - **Response:** Job status and result (if completed)

12. **GET /crawl/job/{task_id}/stream**
    - **Purpose:** Stream job progress via WebSocket
    - **Response:** Real-time status updates

13. **POST /llm/job**
    - **Purpose:** Create async LLM extraction job
    - **Request:** URLs + LLM config + webhook
    - **Response:** Task ID

14. **GET /llm/job/{task_id}**
    - **Purpose:** Get LLM job result
    - **Response:** Extraction results

#### Monitoring & Admin Endpoints

15. **GET /**
    - **Purpose:** Root endpoint with API info
    - **Response:** Welcome message and version

16. **POST /token**
    - **Purpose:** Generate JWT authentication token
    - **Request:** Email (if domain verification enabled)
    - **Response:** JWT token

17. **POST /config/dump**
    - **Purpose:** Get server configuration
    - **Response:** Config YAML

18. **GET /health**
    - **Purpose:** Health check endpoint
    - **Response:** `{"status": "ok"}`

19. **GET /metrics**
    - **Purpose:** Prometheus metrics
    - **Response:** Metrics in Prometheus format

20. **GET /schema**
    - **Purpose:** Get API schema
    - **Response:** JSON schema for requests

21. **GET /hooks/info**
    - **Purpose:** Get information about available hooks
    - **Response:** Hook documentation

#### MCP (Model Context Protocol) Endpoints
**File:** `deploy/docker/mcp_bridge.py`

22. **GET /mcp/sse**
    - **Purpose:** MCP Server-Sent Events endpoint
    - **Response:** MCP protocol messages

23. **GET /mcp/schema**
    - **Purpose:** MCP tools/resources schema
    - **Response:** MCP capabilities

### MCP Tools (Available to LLMs)
- `crawl_url` - Crawl single URL
- `crawl_multiple` - Crawl multiple URLs
- `extract_with_llm` - LLM-based extraction
- `get_markdown` - Get clean markdown

### API Request Flow Examples

#### Synchronous Crawl
```
Client -> POST /crawl
       -> API validates request
       -> Crawler pool assigns browser
       -> Page loads, content extracted
       -> Markdown generated
       -> Response returned
```

#### Async Job with Webhook
```
Client -> POST /crawl/job + webhook_url
       -> Job created in Redis
       -> Task ID returned immediately
       -> Background worker processes job
       -> On completion, webhook called with result
```

#### Streaming Crawl
```
Client -> POST /crawl/stream (keep-alive)
       <- SSE: {"status": "queued", "task_id": "..."}
       <- SSE: {"status": "processing", "url": "..."}
       <- SSE: {"status": "completed", "result": {...}}
```

---

## 7. Prompt/Agent Infrastructure

### Prompt Management
**File:** `crawl4ai/prompts.py` (1,578 lines)

**Categories:**

1. **Block Extraction Prompts**
   - `PROMPT_EXTRACT_BLOCKS` - Break HTML into semantic blocks
   - Uses XML-style tags for structure
   - Generates index, tags, content, questions for each block

2. **Content Filtering Prompts**
   - LLM-based relevance scoring
   - Query-aware content selection
   - Semantic understanding

3. **Schema Extraction Prompts**
   - Pydantic schema to prompt conversion
   - Structured data extraction
   - Type-aware parsing

4. **Q&A Prompts**
   - Context-aware question answering
   - Page content as context
   - Multi-turn conversation support

### Agent/Automation Infrastructure

#### 1. Browser Automation Agents
**Files:** `crawl4ai/js_snippet/`

**Snippets:**
- `remove_overlay_elements.js` - Remove popup/modal overlays
- `update_image_dimensions.js` - Set image dimensions for rendering
- `navigator_overrider.js` - Stealth mode, anti-detection

#### 2. Chrome Extension Agent
**Location:** `docs/md_v2/apps/crawl4ai-assistant/`

**Capabilities:**
- **Click2Crawl** - Record user interactions as automation scripts
- **Script Builder** - Visual programming interface (Blockly)
- **Schema Builder** - Click elements to generate extraction schemas
- **Markdown Preview** - Real-time markdown rendering
- **Content Analyzer** - Analyze page structure

**Agent Workflow:**
1. User activates extension on target page
2. Extension injects content scripts
3. User clicks elements or records actions
4. Extension generates JSON schema or JS script
5. Export to Crawl4AI format

#### 3. Specialized Crawlers
**Location:** `crawl4ai/crawlers/`

**Pre-built Agents:**
- `amazon_product/crawler.py` - Amazon product extraction
- `google_search/crawler.py` - Google search results

**Pattern:**
- Predefined schemas
- Domain-specific selectors
- Anti-bot techniques
- Data normalization

#### 4. LLM Agent Integration
**Files:** `extraction_strategy.py`, `content_filter_strategy.py`

**Capabilities:**
- **Schema-based Extraction** - Define Pydantic model, LLM extracts
- **Semantic Filtering** - LLM scores content relevance
- **Intelligent Chunking** - Context-aware content splitting
- **Multi-provider Support** - OpenAI, Anthropic, Groq, etc. via LiteLLM

**Agent Pattern:**
```python
strategy = LLMExtractionStrategy(
    provider="openai/gpt-4",
    schema=MyDataModel,  # Pydantic model
    instruction="Extract product details"
)
result = await crawler.arun(url, extraction_strategy=strategy)
extracted_data = result.extracted_content  # Typed object
```

### Prompt Engineering Patterns

1. **XML-Tagged Prompts**
   - Clear structure with `<url>`, `<html>`, `<blocks>` tags
   - Helps LLM parse and respond in structured format

2. **Few-Shot Examples**
   - Inline examples in prompts
   - Show expected output format

3. **Instruction Layering**
   - Step-by-step instructions
   - Validation rules
   - Error handling guidance

4. **Schema-to-Prompt Conversion**
   - Pydantic models converted to natural language descriptions
   - Type hints preserved
   - Field descriptions included

---

## 8. Recommended DotPrompt Plan Structure

Based on the repository analysis, the recommended DotPrompt plan structure aligns with the codebase's natural boundaries:

### `.prompt/plan/` Directory Structure

```
.prompt/plan/
├── app/
│   ├── server/
│   │   ├── api-layer.md                    # FastAPI endpoints and routing
│   │   ├── crawler-engine.md               # Core crawling logic
│   │   ├── browser-management.md           # Browser pool and lifecycle
│   │   ├── job-queue.md                    # Async job processing
│   │   ├── webhook-delivery.md             # Webhook notification system
│   │   ├── monitoring.md                   # Metrics and observability
│   │   └── mcp-bridge.md                   # Model Context Protocol integration
│   │
│   └── client/
│       ├── chrome-extension.md             # Browser extension architecture
│       ├── playground-ui.md                # API playground interface
│       ├── monitor-dashboard.md            # Monitoring dashboard
│       └── script-builder.md               # Visual script builder (Blockly)
│
├── db/
│   ├── cache-layer.md                      # SQLite/Redis caching strategy
│   ├── job-storage.md                      # Redis job queue schema
│   └── crawler-state.md                    # Session and state management
│
└── shared/
    ├── models/
    │   ├── crawl-models.md                 # CrawlResult, CrawlStatus, etc.
    │   ├── content-models.md               # Media, Links, ScrapingResult
    │   ├── extraction-models.md            # ExtractionStrategy hierarchy
    │   └── llm-models.md                   # LLMConfig, TokenUsage
    │
    ├── strategies/
    │   ├── scraping-strategies.md          # ContentScrapingStrategy implementations
    │   ├── extraction-strategies.md        # LLM, Cosine, JsonCss, JsonXPath
    │   ├── filter-strategies.md            # Content filtering (FIT, BM25, LLM)
    │   ├── markdown-strategies.md          # Markdown generation
    │   ├── proxy-strategies.md             # Proxy rotation
    │   └── deep-crawl-strategies.md        # BFS, DFS, Best-first
    │
    ├── utilities/
    │   ├── async-utilities.md              # Async helpers, dispatchers
    │   ├── browser-utilities.md            # Browser profiling, stealth mode
    │   ├── url-utilities.md                # URL normalization, validation
    │   └── llm-utilities.md                # LLM API wrappers, retry logic
    │
    └── configuration/
        ├── browser-config.md               # BrowserConfig schema
        ├── crawler-config.md               # CrawlerRunConfig schema
        └── llm-config.md                   # LLMConfig schema
```

### Rationale for This Structure

1. **app/server/** - Maps to backend services in `crawl4ai/` and `deploy/docker/`
   - Each major subsystem gets its own plan file
   - Clear separation of concerns (API, crawling, jobs, monitoring)

2. **app/client/** - Maps to frontend components in `docs/md_v2/apps/` and `deploy/docker/static/`
   - Each UI component is separately documented
   - Facilitates independent modernization

3. **db/** - Maps to data persistence layer
   - Cache strategy (SQLite for crawl cache, Redis for jobs)
   - State management

4. **shared/models/** - Maps to `crawl4ai/models.py` and domain models
   - Organized by domain (crawl, content, extraction, LLM)
   - Supports both backend and potential frontend use

5. **shared/strategies/** - Maps to strategy pattern implementations
   - Each strategy type in its own file
   - Hierarchical organization

6. **shared/utilities/** - Maps to `crawl4ai/utils.py` and helper modules
   - Cross-cutting concerns
   - Reusable across layers

7. **shared/configuration/** - Maps to `crawl4ai/async_configs.py`
   - Configuration schemas
   - Environment-specific settings

### Migration Use Cases

This structure supports multiple migration scenarios:

1. **Microservice Decomposition**
   - `app/server/crawler-engine.md` → Separate crawling service
   - `app/server/job-queue.md` → Dedicated job processor
   - `app/server/webhook-delivery.md` → Notification service

2. **Frontend Modernization**
   - `app/client/chrome-extension.md` → React-based extension
   - `app/client/playground-ui.md` → Modern SPA framework
   - `app/client/monitor-dashboard.md` → Real-time dashboard

3. **API Evolution**
   - `app/server/api-layer.md` → GraphQL or gRPC migration
   - `shared/models/` → TypeScript type generation
   - `app/server/mcp-bridge.md` → Enhanced LLM integrations

4. **Database Migration**
   - `db/cache-layer.md` → PostgreSQL or MongoDB
   - `db/job-storage.md` → Dedicated queue service (RabbitMQ, Kafka)

---

## 9. Key Architectural Patterns

### 1. Strategy Pattern (Extensively Used)
- **Scraping Strategies** - Different HTML parsing approaches
- **Extraction Strategies** - LLM, CSS, XPath, Cosine similarity
- **Filter Strategies** - Content relevance filtering
- **Markdown Strategies** - Various markdown generation approaches
- **Proxy Strategies** - Proxy rotation algorithms
- **Deep Crawl Strategies** - BFS, DFS, Best-first traversal

### 2. Async/Await Pattern
- All core operations are async
- Non-blocking I/O for browser automation
- Concurrent crawling with rate limiting
- AsyncWebCrawler as primary interface

### 3. Dispatcher Pattern
- `MemoryAdaptiveDispatcher` - Memory-aware task dispatching
- `SemaphoreDispatcher` - Concurrency control
- `RateLimiter` - Domain-level rate limiting

### 4. Pool Pattern
- Browser pool management (deploy/docker/crawler_pool.py)
- Reuse browser contexts
- Automatic cleanup and janitor tasks

### 5. Hook Pattern
- User-defined hooks at various lifecycle points
- `on_page_context_created`, `before_retrieve_html`, etc.
- Function-based hook system in Docker API

### 6. Job Queue Pattern
- Redis-backed async job processing
- Task ID tracking
- Status polling and webhook delivery

### 7. Webhook Pattern
- Exponential backoff retry
- Custom headers and payload customization
- Delivery status tracking

---

## 10. Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **Core Language** | Python 3.10+ |
| **Web Framework** | FastAPI |
| **Browser Automation** | Playwright, Patchright |
| **Async Runtime** | asyncio, aiohttp, aiosqlite |
| **Database** | SQLite (cache), Redis (jobs) |
| **LLM Integration** | LiteLLM (multi-provider) |
| **HTML Processing** | BeautifulSoup4, lxml |
| **Content Ranking** | BM25, NLTK |
| **Monitoring** | Prometheus, psutil |
| **Frontend** | Vanilla JS, Blockly, Marked.js |
| **Browser Extension** | Chrome Manifest V3 |
| **Documentation** | MkDocs |
| **Containerization** | Docker, Docker Compose |
| **Process Management** | Supervisor |
| **Package Management** | uv, setuptools |

---

## 11. Critical Files for Migration Analysis

### Core Library
1. `crawl4ai/__init__.py` - Public API exports
2. `crawl4ai/async_webcrawler.py` - Main crawler interface
3. `crawl4ai/async_crawler_strategy.py` - Core crawling algorithm (2,394 LOC)
4. `crawl4ai/models.py` - Domain models
5. `crawl4ai/utils.py` - Shared utilities (3,657 LOC)

### API Server
6. `deploy/docker/server.py` - FastAPI app entry point
7. `deploy/docker/api.py` - API endpoint handlers
8. `deploy/docker/crawler_pool.py` - Browser pool management
9. `deploy/docker/job.py` - Job queue routing
10. `deploy/docker/webhook.py` - Webhook delivery service

### Configuration
11. `pyproject.toml` - Package metadata and dependencies
12. `deploy/docker/config.yml` - Server configuration
13. `crawl4ai/async_configs.py` - Runtime configuration models (1,951 LOC)

### Strategy Implementations
14. `crawl4ai/extraction_strategy.py` - Extraction strategies (2,160 LOC)
15. `crawl4ai/content_filter_strategy.py` - Filter strategies (1,079 LOC)
16. `crawl4ai/content_scraping_strategy.py` - Scraping strategies (900 LOC)
17. `crawl4ai/markdown_generation_strategy.py` - Markdown generation

### Browser Management
18. `crawl4ai/browser_manager.py` - Browser lifecycle (1,175 LOC)
19. `crawl4ai/browser_profiler.py` - Anti-detection (1,235 LOC)
20. `crawl4ai/browser_adapter.py` - Browser abstraction

---

## 12. Dependency Graph (High-Level)

```
┌─────────────────────────────────────────────────┐
│         FastAPI Server (deploy/docker/)          │
│  - server.py (entry point)                      │
│  - api.py (handlers)                            │
│  - job.py (queue router)                        │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│      Browser Pool (crawler_pool.py)             │
│  - Manages browser instances                    │
│  - Janitor for cleanup                          │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│    AsyncWebCrawler (async_webcrawler.py)        │
│  - Public API interface                         │
│  - Configuration management                     │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  AsyncCrawlerStrategy (async_crawler_strategy.py)│
│  - Core crawling logic                          │
│  - Browser interaction                          │
│  - Content extraction orchestration             │
└──┬────────────┬────────────┬────────────┬───────┘
   │            │            │            │
   ↓            ↓            ↓            ↓
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Browser│  │Scraping  │  │Extraction│  │Markdown  │
│Manager│  │Strategy  │  │Strategy  │  │Generator │
└───────┘  └──────────┘  └──────────┘  └──────────┘
     │           │             │             │
     ↓           ↓             ↓             ↓
┌─────────────────────────────────────────────────┐
│              Shared Models & Utils              │
│  - models.py                                    │
│  - utils.py                                     │
│  - async_configs.py                             │
└─────────────────────────────────────────────────┘
```

---

## 13. Testing Infrastructure

### Test Organization
**Location:** `tests/` (18 subdirectories)

**Categories:**
1. **Core Tests** - `test_web_crawler.py`, `test_main.py`
2. **Docker API Tests** - `test_docker.py`, `test_docker_api_with_llm_provider.py`
3. **Feature Tests** - `test_llm_extraction_*.py`, `test_webhook_*.py`
4. **Config Tests** - `test_config_selection.py`, `test_multi_config.py`
5. **Integration Tests** - `test_arun_many.py`, `test_virtual_scroll.py`

### Docker Tests
**Location:** `deploy/docker/tests/`

**Stress Tests:**
- `test_1_basic.py` - Basic functionality
- `test_2_memory.py` - Memory usage
- `test_3_pool.py` - Browser pool
- `test_4_concurrent.py` - Concurrent requests
- `test_5_pool_stress.py` - High-load stress testing

---

## 14. Documentation Structure

### Main Documentation
**Location:** `docs/md_v2/`

**Sections:**
- `basic/` - Getting started tutorials
- `advanced/` - Advanced features
- `api/` - API reference
- `core/` - Core concepts
- `extraction/` - Extraction strategies
- `migration/` - Version migration guides
- `blog/` - Release notes

### Code Examples
**Location:** `docs/examples/`

**Categories:**
- Adaptive crawling
- Docker usage
- LLM extraction
- Webhook integration
- Stealth mode
- Deep crawling

---

## 15. Security & Authentication

### JWT Authentication
**File:** `deploy/docker/auth.py`

**Features:**
- Optional email domain verification
- Token expiration
- Bearer token authentication
- Email-based token generation

### Rate Limiting
**Implementation:** slowapi

**Configuration:**
- Per-endpoint limits
- IP-based tracking
- Configurable via `config.yml`

### Security Headers
- HTTPS redirect middleware (configurable)
- Trusted host middleware

---

## 16. Observability

### Metrics
- **Prometheus Integration** - `/metrics` endpoint
- **Custom Metrics** - Crawl success/failure, latency, memory usage

### Logging
**File:** `crawl4ai/async_logger.py`

**Features:**
- Structured logging
- Async-safe logging
- Per-crawler instance loggers

### Monitoring Dashboard
**Location:** `deploy/docker/static/monitor/index.html`

**Features:**
- Real-time crawler status
- Pool utilization
- Job queue status
- WebSocket-based updates

---

## 17. Deployment Configurations

### Docker
**Files:** `Dockerfile`, `docker-compose.yml`, `deploy/docker/supervisord.conf`

**Services:**
- FastAPI server (port 11235)
- Redis (for job queue)
- Supervisor (process management)

**Build Args:**
- `INSTALL_MODEL` - Install NLP models
- `ENABLE_GPU` - GPU support for ML models

### Environment Variables
**File:** `deploy/docker/.llm.env.example`

**Required:**
- LLM API keys (OpenAI, Anthropic, etc.)
- Optional: Custom base URLs, timeouts

---

## 18. Chrome Extension Architecture

### Manifest V3
**File:** `docs/md_v2/apps/crawl4ai-assistant/manifest.json`

**Permissions:**
- `activeTab` - Access current tab
- `storage` - Store settings and schemas
- `downloads` - Export schemas
- `<all_urls>` - Work on all websites

### Content Scripts
**Files:** `content/*.js`

**Modules:**
1. `click2crawl.js` - Interaction recording
2. `scriptBuilder.js` - Blockly integration
3. `contentAnalyzer.js` - Page structure analysis
4. `markdownConverter.js` - Live markdown conversion
5. `markdownExtraction.js` - Schema-based extraction

### Background Service Worker
**File:** `background/service-worker.js`

**Responsibilities:**
- Message passing between content and popup
- Storage management
- Download handling

---

## 19. Next Steps for Migration Planning

### Phase 1: IR Generation
1. Generate IR for all files in `crawl4ai/` core library (345 Python files)
2. Prioritize high-LOC files (utils.py, async_crawler_strategy.py, extraction_strategy.py)
3. Focus on strategy implementations first (clear patterns)
4. Document domain models thoroughly

### Phase 2: Dependency Mapping
1. Build complete dependency graph using imports
2. Identify circular dependencies (if any)
3. Map external dependencies to modern equivalents
4. Document breaking changes in upgrades

### Phase 3: Plan Generation
1. Create plan files for each major subsystem
2. Define modernization targets:
   - Python 3.12+
   - FastAPI 0.110+
   - Pydantic v2 (already using)
   - Modern async patterns
3. Identify refactoring opportunities:
   - Split large files (utils.py, async_crawler_strategy.py)
   - Extract shared utilities
   - Improve type hints

### Phase 4: Migration Strategy
1. **Backend Modernization**
   - Upgrade to latest Playwright
   - Enhance type safety with strict mypy
   - Improve test coverage

2. **API Evolution**
   - Consider GraphQL for complex queries
   - Add OpenAPI 3.1 schemas
   - Improve error handling

3. **Frontend Modernization**
   - Chrome extension → React/TypeScript
   - Dashboard → Modern framework (Svelte, Vue, React)
   - Shared component library

4. **Infrastructure**
   - Kubernetes deployment option
   - Distributed crawling architecture
   - Improved observability (OpenTelemetry)

---

## 20. Summary & Recommendations

### Strengths
✅ **Well-organized codebase** with clear separation of concerns
✅ **Extensive use of design patterns** (Strategy, Factory, Dispatcher)
✅ **Comprehensive documentation** and examples
✅ **Production-ready API** with monitoring and webhooks
✅ **Modern async architecture** throughout
✅ **Flexible LLM integration** with multi-provider support
✅ **Strong type safety** with Pydantic models

### Areas for Improvement
⚠️ **Large monolithic files** (utils.py: 3,657 LOC)
⚠️ **Test coverage** could be expanded
⚠️ **Type hints** could be more comprehensive (add mypy strict mode)
⚠️ **Circular imports** possibility (needs verification)
⚠️ **Documentation** could use API versioning

### Modernization Priorities
1. **Split large files** into smaller, focused modules
2. **Enhance type safety** with strict type checking
3. **Improve test coverage** especially for edge cases
4. **Add API versioning** for backward compatibility
5. **Consider microservices** for scaling (crawler, jobs, webhooks)
6. **Frontend modernization** with modern frameworks
7. **Enhanced observability** with distributed tracing

### DotPrompt Workflow Recommendations
1. **Start with high-value files** (core crawling logic, strategies)
2. **Generate IRs in parallel** for independent modules
3. **Focus on strategy patterns first** (clear, well-defined interfaces)
4. **Map dependencies early** to avoid surprises
5. **Use tags extensively** for semantic indexing
6. **Document LLM prompts carefully** (critical for RAG use cases)
7. **Plan for incremental migration** (not big-bang rewrite)

---

**End of Repository Structure Analysis**

This analysis provides a comprehensive foundation for creating detailed IR files and migration plans using the DotPrompt workspace.
