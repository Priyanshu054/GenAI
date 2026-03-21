# Airline AI Assistant - Complete Guide

## Overview

The **Airline AI Assistant** is an intelligent chatbot powered by Ollama (local LLM) and Gradio UI. It helps customers search for flights, check prices, departure times, and get flight details using a natural conversation interface.

### Key Features
- 🤖 Local AI model (no cloud dependency)
- 🛠️ Function calling - AI can automatically look up flight information
- 💬 Streaming responses for real-time feedback
- 🎯 Specialized airline customer service capabilities

---

## Architecture

### Components

```
┌─────────────┐
│   Gradio    │ ← User Interface (Chat)
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│  chat_with_tools() Function     │
│  - Builds message history       │
│  - Makes API calls to Ollama    │
│  - Handles tool calls           │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   Ollama (Local LLM)            │
│   Model: qwen2.5:7b-instruct    │
│   - Understands user questions  │
│   - Decides when to use tools   │
│   - Generates responses         │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│    Flight Data & Tools          │
│  - flights[] (30 flight data)   │
│  - get_ticket_price()           │
│  - get_departure_time()         │
│  - get_flights_to_destination() │
└─────────────────────────────────┘
```

---

## System Prompt (Optimized)

The assistant follows this optimized system prompt:

```
You are a helpful customer service assistant for FlightAI airline.
Keep responses brief and courteous (1-2 sentences).
Use tools to find flight prices, times, and routes when asked about specific flights.
If a flight doesn't exist, inform the customer clearly.
Always be accurate. If unsure, say so.
```

**Why this prompt is optimized:**
- Short and concise (~85 tokens vs 200+ tokens)
- Faster model response time
- Covers all essential behavior rules
- Clear instructions on tool usage

---

## Available Tools

The assistant can call 3 tools to fetch flight information:

### 1. `get_ticket_price(origin, destination)`
**Purpose:** Find the ticket price for a specific route

**Example:**
```python
get_ticket_price("Delhi", "Mumbai")
# Returns: "The ticket price from Delhi to Mumbai is ₹5500."
```

### 2. `get_departure_time(origin, destination)`
**Purpose:** Find the departure time for a specific route

**Example:**
```python
get_departure_time("Mumbai", "Bangalore")
# Returns: "The departure time from Mumbai to Bangalore is 10:30."
```

### 3. `get_flights_to_destination(destination)`
**Purpose:** Get all flights arriving at a specific city

**Example:**
```python
get_flights_to_destination("Mumbai")
# Returns details of all flights going to Mumbai with times & prices
```

---

## How It Works - Step by Step

### Example Conversation 1: Simple Price Query

```
User: "How much is a ticket from Delhi to Mumbai?"
```

**Flow:**
1. User enters question in Gradio UI
2. `chat_with_tools()` builds message list:
   - System prompt
   - Chat history (empty, first message)
   - User message

3. Sends to Ollama with available tools
4. Ollama recognizes need for ticket price → calls `get_ticket_price("Delhi", "Mumbai")`
5. Tool function returns: `"The ticket price from Delhi to Mumbai is ₹5500."`
6. Ollama processes tool result and generates response:

```
Assistant: "A ticket from Delhi to Mumbai costs ₹5500. Would you like to book?"
```

---

### Example Conversation 2: Multiple Tool Calls

```
User: "I want to go from Delhi to Mumbai. When does the flight leave and how much?"
```

**Flow:**
1. Ollama decides it needs 2 pieces of information
2. Makes 2 tool calls:
   - `get_departure_time("Delhi", "Mumbai")` → "08:00"
   - `get_ticket_price("Delhi", "Mumbai")` → "₹5500"
3. Processes both results
4. Generates response:

```
Assistant: "The Delhi-Mumbai flight departs at 08:00 and costs ₹5500. Shall I help with booking?"
```

---

### Example Conversation 3: List All Flights

```
User: "What flights are going to Mumbai today?"
```

**Flow:**
1. Ollama recognizes need for multiple flights → calls `get_flights_to_destination("Mumbai")`
2. Tool returns all flights to Mumbai with details:
   ```
   Flight FL-001: Delhi → Mumbai, Time: 08:00, Price: ₹5500
   Flight FL-005: Mumbai → Delhi (not relevant, but data returns)
   Flight FL-007: Kolkata → Mumbai, Time: 11:30, Price: ₹6800
   ...
   ```
3. Ollama processes and responds:

```
Assistant: "There are several flights to Mumbai. The earliest is from Delhi at 08:00 (₹5500), 
and another from Kolkata at 11:30 (₹6800). Which interests you?"
```

---

### Example Conversation 4: Unknown Route

```
User: "Is there a flight from Delhi to London?"
```

**Flow:**
1. Ollama calls `get_ticket_price("Delhi", "London")`
2. Tool returns: `"No flight found from Delhi to London."`
3. Ollama understands and responds:

```
Assistant: "Unfortunately, we don't have flights from Delhi to London at this time. 
Can I help you with another route?"
```

---

## Flight Data Structure

The assistant uses 30 flights stored in the `flights` list:

```python
{
    "flight_id": "FL-001",
    "origin_city": "Delhi",
    "destination_city": "Mumbai",
    "time": "08:00",
    "price": 5500,
}
```

---

## Message Storage & Structure

### How Messages Are Stored

Messages in the Airline AI Assistant are stored as **Python dictionaries** in a **list** (chat history). Each message follows the OpenAI/Ollama message format:

#### Message Structure

```python
{
    "role": "system" | "user" | "assistant" | "tool",
    "content": "string",
    # Optional fields:
    "tool_calls": [...],      # Only for assistant messages
    "tool_call_id": "string"  # Only for tool messages
}
```

### Message Roles

| Role | Purpose | Who Creates It |
|------|---------|---|
| **system** | System instructions & assistant behavior | Developer (system_prompt) |
| **user** | Customer's question or request | User (Gradio UI) |
| **assistant** | AI's response or tool decision | Ollama model |
| **tool** | Result of executing a tool/function | handle_tool_calls() function |

### Example Message Flow

Here's how messages are stored for a typical conversation:

#### Initial Message List (Before API Call)
```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful customer service assistant for FlightAI airline..."
    },
    {
        "role": "user",
        "content": "How much is Delhi to Mumbai?"
    }
]
```

#### After Ollama Decides to Call a Tool
```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful customer service assistant for FlightAI airline..."
    },
    {
        "role": "user",
        "content": "How much is Delhi to Mumbai?"
    },
    {
        "role": "assistant",
        "content": None,  # No text response, only tool calls
        "tool_calls": [
            {
                "id": "call_123",
                "function": {
                    "name": "get_ticket_price",
                    "arguments": '{"origin": "Delhi", "destination": "Mumbai"}'
                }
            }
        ]
    }
]
```

#### After Tool Execution Result Added
```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful customer service assistant for FlightAI airline..."
    },
    {
        "role": "user",
        "content": "How much is Delhi to Mumbai?"
    },
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [...]  # Same as above
    },
    {
        "role": "tool",
        "name": "get_ticket_price",
        "content": "The ticket price from Delhi to Mumbai is ₹5500.",
        "tool_call_id": "call_123"
    }
]
```

#### Final Response (No More Tool Calls)
```python
messages = [
    # ... all previous messages ...
    {
        "role": "assistant",
        "content": "A ticket from Delhi to Mumbai costs ₹5500. Would you like to book?",
        "tool_calls": None  # No more tools to call
    }
]
```

### Chat History Accumulation

After each conversation turn, the **entire message history** is passed to Ollama, including:
1. System prompt
2. All previous user messages
3. All previous assistant responses
4. All tool calls made
5. All tool results

This allows the AI to understand context and maintain coherent conversations.

### Gradio Chat Interface Integration

The Gradio `ChatInterface` automatically manages the message display:
- It stores the conversation in a **chat_history** parameter
- Each element is a tuple: `(user_message, assistant_response)`
- The function receives this history and should return the new response

```python
def chat_with_tools(user_message, chat_history):
    # chat_history example:
    # [
    #     ("How much is Delhi to Mumbai?", "₹5500"),
    #     ("When does it depart?", "08:00")
    # ]
    
    # Convert Gradio format to Ollama format
    messages = (
        [{"role": "system", "content": system_prompt}]
        + chat_history  # This gets converted properly
        + [{"role": "user", "content": user_message}]
    )
    
    # ... rest of logic ...
```

### Message Size & Performance

- **System Prompt:** ~85 tokens
- **Per User Message:** ~10-30 tokens
- **Per Assistant Response:** ~20-100 tokens
- **Per Tool Call + Result:** ~50-150 tokens

**Total tokens sent to Ollama increases with conversation length!**

Example:
- 1st turn: ~150 tokens
- 2nd turn: ~200 tokens (includes history)
- 3rd turn: ~250 tokens (more history)

For very long conversations, consider:
- Summarizing old history
- Implementing conversation reset
- Using a database for persistent storage

---

## Conversation Flow Diagram

```
User Input (Gradio UI)
        ↓
chat_with_tools() function
        ↓
Build Messages [System Prompt + History + User Message]
        ↓
Call Ollama API with tools
        ↓
Ollama Response ─────┬─→ No tool calls? → Generate final answer → Return to User
                     │
                     └─→ Tool calls? → Execute tools (handle_tool_calls)
                                          ↓
                                     Add tool results to messages
                                          ↓
                                     Call Ollama again (loop)
                                          ↓
                                     Final response with all info
```

---

## How to Run

### 1. Start Ollama Server
```bash
ollama serve
```

### 2. Run the Notebook
Open `Airline_AI_Assistant.ipynb` and execute cells in order:
- Cell 1-4: Setup & imports
- Cell 5: Initialize Ollama client
- Cell 6-10: Define tools
- Cell 11: Launch Gradio UI

### 3. Access the Chat Interface
The Gradio interface will launch at `http://localhost:7860`

---

## Real-World Example Conversations

### Conversation #1: Simple Price Query
```
User: "How much does it cost to fly from Mumbai to Bangalore?"

[Assistant calls: get_ticket_price("Mumbai", "Bangalore")]
Tool Response: "The ticket price from Mumbai to Bangalore is ₹4800."

Assistant Response: "A ticket from Mumbai to Bangalore costs ₹4800. Would you like to know the departure time?"
```

### Conversation #2: Checking Multiple Details
```
User: "Tell me the time and price for Delhi to Kolkata"

[Assistant calls TWO tools:]
- get_departure_time("Delhi", "Kolkata") → "12:15"
- get_ticket_price("Delhi", "Kolkata") → "₹6200"

Assistant Response: "The Delhi-Kolkata flight departs at 12:15 and costs ₹6200. Need help booking?"
```

### Conversation #3: Finding All Flights to a Destination
```
User: "What are all the flights to Chennai?"

[Assistant calls: get_flights_to_destination("Chennai")]
Tool Response:
  - Flight FL-004: Bangalore → Chennai, 14:45, ₹3900

Assistant Response: "There's a flight to Chennai from Bangalore departing at 14:45 for ₹3900. 
Any other routes you'd like to check?"
```

### Conversation #4: Route Not Available
```
User: "Can I fly from Delhi to New York?"

[Assistant calls: get_ticket_price("Delhi", "New York")]
Tool Response: "No flight found from Delhi to New York."

Assistant Response: "Unfortunately, we don't offer international flights right now. 
Would you like domestic flight options instead?"
```

### Conversation #5: Multi-turn with Follow-up
```
User: "Flights from Hyderabad to Bangalore?"

[Assistant calls:
  - get_ticket_price("Hyderabad", "Bangalore") → ₹4000
  - get_departure_time("Hyderabad", "Bangalore") → 14:30
]

Assistant Response: "There's a flight from Hyderabad to Bangalore at 14:30 for ₹4000."

User: "And from Mumbai to Bangalore?"

[Assistant calls:
  - get_ticket_price("Mumbai", "Bangalore") → ₹4800
  - get_departure_time("Mumbai", "Bangalore") → 10:30
]

Assistant Response: "From Mumbai to Bangalore, there's a flight at 10:30 for ₹4800. Which one suits you?"
```

---

## Key Features Explained

### 1. **Automatic Tool Calling**
The Ollama model intelligently decides WHEN to use tools based on user queries:
- "How much is a flight?" → Calls `get_ticket_price()`
- "When does it depart?" → Calls `get_departure_time()`
- "What flights go to X?" → Calls `get_flights_to_destination()`
- "Hello" / "Hi" → No tool call needed

### 2. **Conversation Memory**
Each message is added to the conversation history so the assistant:
- Remembers previous context
- Can answer follow-up questions
- Maintains a coherent conversation flow

### 3. **Error Handling**
- If a tool fails: Tool error caught and reported
- If a flight doesn't exist: Tool returns "No flight found" message
- If parameters are wrong: Graceful error messages

### 4. **Loop-based Tool Handling**
The `chat_with_tools()` function runs in a while loop:
1. Send message to Ollama
2. If Ollama response has tool calls → Execute them
3. Add tool results back to message history
4. Send updated messages to Ollama again
5. Repeat until no more tool calls (final response ready)

This allows the assistant to gather information progressively!
