## Core Concepts Breakdown
 ## Tool Calling vs. Function CallingFunction Calling:
 A capability offered by LLM provider APIs (OpenAI, Anthropic, Gemini, Groq) where you provide JSON schemas of functions, and the model outputs structured JSON indicating which function to run and with what arguments.
 Tool Calling: A higher-level abstraction in frameworks like LangChain/LangGraph that wraps Python functions into standardized Tool objects. It handles schema generation, input validation, execution, and output formatting automatically.
 LLM Call vs. AI Agent
 FeatureNormal LLM CallAI Agent (e.g., LangGraph ReAct)ExecutionSingle-pass request and response (input $\rightarrow$ text output).
 Continuous loop: Reason $\rightarrow$ Act $\rightarrow$ Observe $\rightarrow$ Repeat.Tool UsageReturns intent/JSON asking you to run a tool, but cannot run it itself.Decides whether to use tools, calls them autonomously, receives results, and keeps reasoning.Control FlowRigid, single turn.Dynamic, multi-step orchestration (via state graphs).
 Project Architecture (LangGraph + LangSmith + Streamlit)Here is the complete codebase satisfying all core requirements and bonus criteria:At least 2 Custom Tools: Calculator + Weather + Custom Python RAG / KB tool.
 ## LangGraph Workflow: 
 Custom state graph with StateGraph and ToolNode.  LangSmith Tracing: Automatic execution tracking and debugging.  Error Handling & Logging: Robust exceptions inside tools and custom logger output.  File StructurePlaintextai-agent-tool-calling/
│
├── .env
├── requirements.txt
├── tools.py
├── agent.py
└── app.py
# 🤖 Multi-Tool AI Agent with LangGraph & LangSmith

An autonomous, multi-tool AI Agent built using **LangGraph**, **LangChain**, and **Streamlit**. The agent dynamically evaluates user input, selects and executes the appropriate tool(s), handles failures gracefully, and synthesizes a final response. Full execution tracing and evaluation are powered by **LangSmith**.

---

## ✨ Features

- **Autonomous Tool Selection:** Uses LLM function calling to decide when and which tools to trigger.
- **Custom Tool Suite:**
  - 🔢 `calculate`: Safe mathematical evaluation for arithmetic expressions.
  - 🌤️ `get_weather`: Weather lookup for supported cities.
  - 📚 `search_knowledge_base`: Internal corporate/project documentation search.
  - 🌐 `tavily_search_results_json`: Live web search integration via Tavily AI.
- **Stateful Workflow (LangGraph):** Cyclic graph setup utilizing `StateGraph` and `ToolNode` for reasoning loops.
- **Error Handling & Logging:** Detailed terminal logging for selected tools and error catching inside tool definitions.
- **Observability (LangSmith):** Automatic evaluation and step-by-step execution tracing.
- **Interactive UI (Streamlit):** Web interface displaying user chat, tool execution badges, and final responses.

---

## 🏗️ Architecture & Control Flow

```text
               +-------------------+
               |    User Input     |
               +---------+---------+
                         |
                         v
                +-----------------+
                |   Agent Node    |
                |   (LLM Decision)|
                +--------+--------+
                         |
           Does input require a tool?
                  /             \
            [Yes]               [No]
             /                     \
            v                       v
   +-----------------+      +-----------------+
   |   Tool Node     |      |   Final Answer  |
   | (Execute Tool)  |      |   (End Graph)   |
   +--------+--------+      +-----------------+
            |
            v
   (Pass observation
    back to Agent)
