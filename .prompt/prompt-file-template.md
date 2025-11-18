# File: <relative/path/to/source/file>

## 1. Purpose
Describe in full sentences:

- What this file represents in the original system.
- What business or functional purpose it serves.
- Whether this file is UI, business logic, infrastructure, configuration, or a helper.
- Any high-level intent or known constraints behind the file.

## 2. Domain Role
Explain the business/domain relevance of this file:

- What domain entity, workflow, or behavior it models.
- The business rules or invariants it enforces.
- Its upstream and downstream relationships in the domain.
- Whether it represents state, transformation, orchestration, or side effects.

## 3. Public API (FULL DETAIL)
List ALL public-facing API surfaces with exact signatures.

### Classes
```
class ClassName(Base?, Interfaces?)
```
- Constructors
- Public methods with parameters + return types
- Public properties / fields
- Events / signals (if applicable)

### Functions
```
def function_name(param: type) -> type — description
```

### Interfaces / Protocols / Types
- Fields and required members.

### Constants / Enums
- List values and meaning.

**The goal:** A developer should be able to recreate the file's external contract from this section alone.

## 4. Internal Structure
Document key internal elements—NOT trivial boilerplate:

- private/protected/internal methods (signatures only)
- private fields or state variables
- initialization patterns
- overridden framework lifecycle methods
- internal helper utilities
- architectural patterns used (Factory, Strategy, Observer, Adapter, etc.)

## 5. Internal Behavior & Data Flow
Describe step‑by‑step how the file behaves internally:

- How input enters the file
- How data is validated
- How transformations occur
- How external calls are made (services, DB, APIs)
- How outputs or side effects are produced

### Data Flow Steps
1. **Input**
2. **Transformations**
3. **External calls**
4. **Output**

## 6. Relationships & Collaboration
Describe how this file interacts with other modules:

- imported or injected dependencies
- collaborators (services, models, utilities)
- framework bindings (FastAPI router, Django model, Express router, Terraform module, etc.)
- upstream and downstream modules
- event listeners or emitters

## 7. Database Interaction Mapping
If this file interacts with a database:

- list affected tables
- fields read/written
- query patterns (SELECT/INSERT/UPDATE/DELETE)
- ORM model relationships
- transactions or concurrency concerns
- caching or optimization behavior

If no DB interaction: state that explicitly.

## 8. UI Behavior (if applicable)
For UI components/pages/templates:

- purpose of the UI element
- user interactions
- lifecycle (React hooks, Vue lifecycle, template rendering, ASP.NET Page_Load, etc.)
- data binding
- form validation
- event handlers
- UI state transitions

If not UI-related, state: "No UI behavior."

## 9. Key Logic Snippets
Include 10–30 lines of meaningful, non‑trivial code.

**Rules:**
- MUST represent important logic (branching, calculations, transformations)
- MUST NOT include entire file
- MUST include any logic that defines domain behavior
- MUST include comments if helpful

**Example:**
```python
def calculate_total(order):
    if order.is_discounted and order.amount > 1000:
        return order.amount * 0.9
    return order.amount
```

**Example:**
```csharp
public bool IsEligible(Person person) {
    if (person.Age < 18 && !person.HasGuardian)
        return false;
    return true;
}
```

## 10. Architectural Concerns
Document:

- security implications
- error handling strategy
- logging approach
- performance or scalability concerns
- concurrency / async behavior
- framework constraints or lifecycle limitations
- configuration dependencies

## 11. Migration Mapping (Legacy → Modern)
Describe EXACTLY how this file should appear in the new system:

### Backend
- Which service(s)?
- Which repository?
- Which controller/route?
- Which API endpoint?
- Which data model?

### Frontend
- Which component/page?
- Which hooks/state?
- Which API calls?

### Database
- Which table/collection?
- How each property maps to a column or field?

### Shared
- Reusable types?
- Validation logic?
- Utilities?

## 12. Migration Concerns & Recommendations
Explain:

- ambiguous logic needing clarification
- hidden or implicit business rules
- risks or technical debt
- areas that must be redesigned, not copied
- recommended improvements in modernization

## 13. Dependencies
Populate using dependency-graph.json:

### dependsOn
- list all files this file depends on

### usedBy
- list all files depending on this file

These lists must be accurate to build the plan layer.

## 14. Tags
Provide 5–12 classification tags, such as:

- domain-model
- business-logic
- service
- controller
- repository
- ui-component
- validation
- workflow
- state-machine
- infra
- migration-critical
- legacy-quirk

These tags improve semantic indexing and plan‑layer generation.
