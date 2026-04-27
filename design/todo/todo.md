# ✅ CORE TODO (DO ONLY THIS)

## 1. Project Setup

* [ ] Create GitHub repo
* [ ] Create folders:

  ```
  agent/
  api/
  ```
* [ ] Install deps:

  * fastapi
  * langgraph
  * langchain
  * pydantic
  * psycopg2 (or asyncpg)

---

## 2. Architecture (README.md)

* [ ] Write 1 short paragraph (what system does)

* [ ] Add 1 Mermaid diagram with:

  * FastAPI
  * LangGraph agent
  * PostgreSQL
  * LLM (Groq/OpenRouter)

* [ ] Write 1 full conversation flow:

  * Input: Cox’s Bazar search
  * → extract params
  * → call search tool
  * → return results

* [ ] Define State (fields + 1-line purpose each)

* [ ] Define Nodes (MAX 5):

  * intent_router
  * search_node
  * details_node
  * booking_node
  * fallback_node

* [ ] Define 3 Tools:

  * search_available_properties
  * get_listing_details
  * create_booking

* [ ] Define DB schema (3 tables only):

  * listings
  * bookings
  * conversations

---

## 3. Agent Code (agent/)

### state.py

* [ ] Create `TypedDict` state:

  * user_input: str
  * intent: str
  * location: str | None
  * dates: str | None
  * guests: int | None
  * listing_id: int | None
  * result: dict | None
  * error: str | None

---

### tools.py

* [ ] Create 2–3 tools using `@tool`
* [ ] Add Pydantic schemas
* [ ] Return MOCK data (no real DB needed)

---

### nodes.py

* [ ] intent_router
* [ ] search_node
* [ ] details_node
* [ ] booking_node
* [ ] fallback_node

Each must:

* [ ] Have type hints
* [ ] Update state
* [ ] Be 5–10 lines max

---

### graph.py

* [ ] Build graph
* [ ] Add nodes
* [ ] Add edges
* [ ] Add conditional routing:

  * search → search_node
  * details → details_node
  * book → booking_node
  * else → fallback_node

---

## 4. API (api.md)

### Endpoint 1

* [ ] POST `/api/chat/{conversation_id}/message`

  * request schema
  * response schema
  * example (BD location + BDT)

### Endpoint 2

* [ ] GET `/api/chat/{conversation_id}/history`

  * response schema
  * example

* [ ] Add error cases:

  * invalid input
  * not found
  * internal error

---

## 5. FastAPI (optional but good)

* [ ] Create minimal FastAPI app
* [ ] 1 route calls LangGraph
* [ ] Return response

---

## 6. Final Checks

* [ ] Type hints everywhere
* [ ] Clean folder structure
* [ ] No extra features
* [ ] Only 3 actions supported
* [ ] Add multiple commits (IMPORTANT)

---

## 🚫 DO NOT DO

* [ ] No UI
* [ ] No auth
* [ ] No extra tools
* [ ] No overengineering
* [ ] No real DB required (mock is fine)

---

## 🎯 PRIORITY ORDER (if time is low)

1. Graph + Nodes
2. Tools
3. README
4. API doc
5. Cleanup

---

If you follow this exactly, you’ll finish fast and hit all scoring criteria.
