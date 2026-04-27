you no need to follow those who are already done follow the database design 

This is the explicit, step-by-step execution plan for the backend architecture. You are building an asynchronous FastAPI service integrating an LLM via LangGraph, backed by PostgreSQL. 

Execute these steps in your Ubuntu terminal. 

### Phase 1: Environment and Core Scaffolding
Set up the isolated environment and structural foundation.

1. **Initialize Environment:**
   ```bash
   mkdir -p app/{agent,api,core,crud,models,schemas} design/{assets,database,todo}
   touch app/__init__.py app/main.py
   touch app/agent/{__init__,graph,nodes,state,tools}.py
   touch app/api/{__init__,routes}.py
   touch app/core/{__init__,config,database}.py
   touch app/crud/{__init__,conversation}.py
   touch app/models/{__init__,tables}.py
   touch app/schemas/{__init__,api_models}.py
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy[asyncio] asyncpg alembic pydantic pydantic-settings langgraph langchain-groq
   pip freeze > requirements.txt
   ```
3. **Git Execution:**
   ```bash
   git init
   echo "venv/" > .gitignore
   echo ".env" >> .gitignore
   echo "__pycache__/" >> .gitignore
   git add .
   git commit -m "chore: initialize project structure, virtual environment, and base dependencies"
   git branch -M main
   git push -u origin main
   ```

### Phase 2: Configuration and Database Layer
Implement the data models and migration system.

1. **`app/core/config.py`**: Define `BaseSettings` requiring `DATABASE_URL` and `GROQ_API_KEY`. Set up the `.env` parser.
2. **`app/core/database.py`**: Instantiate `create_async_engine` and `async_sessionmaker`. Define the `DeclarativeBase` base class. Write the `get_db` async generator for FastAPI dependency injection.
3. **`app/models/tables.py`**: Define the schema explicitly using SQLAlchemy 2.0 `Mapped` and `mapped_column`:
   * `listings`: id (UUID), title, location, price_per_night_bdt, max_guests, is_available.
   * `bookings`: id (UUID), listing_id (FK), guest_name, dates, total_price, status.
   * `conversations`: id (UUID), conversation_id (String, Indexed), role, content, created_at.
4. **Alembic Setup**: 
   * Run `alembic init -t async alembic`.
   * In `alembic/env.py`, import your `Base` and set `target_metadata = Base.metadata`.
   * Run `alembic revision --autogenerate -m "Initial schema"`.
   * Run `alembic upgrade head`.
5. **Git Execution:**
   ```bash
   git add .
   git commit -m "feat: implement async sqlalchemy models and configure alembic migrations"
   git push origin main
   ```

### Phase 3: Data Access and Validation
Build the CRUD operations and API contracts.

1. **`app/schemas/api_models.py`**: Define Pydantic models:
   * `ChatRequest`: `message` (str).
   * `ChatResponse`: `response` (str), `requires_human` (bool).
   * `MessageOut`: `role` (str), `content` (str).
   * `HistoryResponse`: `conversation_id` (str), `messages` (List[MessageOut]).
2. **`app/crud/conversation.py`**: 
   * Write `async def save_message(db, conversation_id, role, content)`.
   * Write `async def get_history(db, conversation_id)` utilizing `select(Conversation).order_by(Conversation.created_at)`.
3. **Git Execution:**
   ```bash
   git add .
   git commit -m "feat: build pydantic schemas and async database crud operations for conversations"
   git push origin main
   ```

### Phase 4: LangGraph State and Tools
Define the constraints and capabilities of the AI.

1. **`app/agent/state.py`**: 
   * Define `AgentState` as a `TypedDict`. 
   * Required fields: `messages` (using `Annotated` with `operator.add` for message appending) and `escalation_status` (str: either "none", "offered", or "escalated").
2. **`app/agent/tools.py`**: 
   * Write `@tool` definitions for `search_available_properties`, `get_listing_details`, and `create_booking`.
   * Define strict Pydantic `args_schema` for each tool. The LLM will fail if these schemas are ambiguous.
3. **Git Execution:**
   ```bash
   git add .
   git commit -m "feat: define langgraph typed state and configure core system tools with pydantic validation"
   git push origin main
   ```

### Phase 5: Graph Nodes and Escalation Logic
Engineer the AI execution loop and strict routing rules.

1. **`app/agent/nodes.py`**:
   * Instantiate `ChatGroq`. Bind the tools using `llm.bind_tools()`.
   * **`agent_node`**: Invoke the LLM with the system prompt. **System Prompt Rule:** *"You handle property searches, details, and bookings. If a user asks for anything else, or if an action fails, reply EXACTLY with: 'I cannot help with that. Would you like to speak to a human?'"*
   * **`escalation_evaluation_node`**: Read the last user message. If the state's previous AI message offered a human, and the user said "yes/sure/okay", set `escalation_status = "escalated"`. If "no", set `"none"`.
2. **`app/agent/graph.py`**:
   * Initialize `StateGraph(AgentState)`.
   * Add nodes: `agent`, `evaluate_escalation`, `tools`.
   * **Routing logic (`should_continue`)**:
     * Evaluate the output of `agent_node`.
     * If output contains tool calls -> route to `tools`.
     * If output matches the human offer string -> route to `evaluate_escalation`.
     * If `escalation_status == "escalated"` -> route to `END`.
     * Otherwise -> route to `END`.
   * Compile the graph.
3. **Git Execution:**
   ```bash
   git add .
   git commit -m "feat: implement graph nodes, custom routing logic, and human escalation workflow"
   git push origin main
   ```

### Phase 6: API Integration
Expose the backend via FastAPI.

1. **`app/api/routes.py`**:
   * `POST /api/chat/{conversation_id}/message`:
     * Save incoming user message to DB.
     * Fetch existing history from DB. Format as LangChain `BaseMessage` objects.
     * Execute graph: `app_graph.invoke({"messages": history_messages, "escalation_status": "none"})`.
     * Extract the AI's response and the `escalation_status` from the resulting state.
     * Save AI response to DB.
     * Return `ChatResponse` mapping `escalation_status == "escalated"` to `requires_human = True`.
   * `GET /api/chat/{conversation_id}/history`: Return mapped DB history.
2. **`app/main.py`**: Include the APIRouter.
3. **Testing**: Run `uvicorn app.main:app --reload`. Test via `http://localhost:8000/docs`. Force the failure condition to ensure the `requires_human` flag flips to `True` in the JSON response.
4. **Git Execution:**
   ```bash
   git add .
   git commit -m "feat: integrate compiled langgraph with fastapi routes and finalize endpoint logic"
   git push origin main
   ```

### Phase 7: Documentation
Complete the technical requirements for the assessment.

1. **`README.md`**: 
   * Write the system architecture overview.
   * Write the Mermaid diagram code mapping the request flow.
   * Document the database schema and LangGraph State fields.
2. **`api.md`**: Detail the exact JSON payloads required for the endpoints.
3. **Git Execution:**
   ```bash
   git add .
   git commit -m "docs: finalize architecture documentation and api contracts for submission"
   git push origin main
   ```