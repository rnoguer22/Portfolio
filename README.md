# Rubén Nogueras Portfolio Github Repository 

---

This professional portfolio showcases an interactive full-stack web application integrated with an advanced agentic RAG system and autonomous AI agent. Built using FastAPI, Next.js, LangGraph, and Chroma, the platform highlights my expertise in artificial intelligence, backend engineering, and scalable system design. It features secure user authentication, persistent chat history, and dynamic multi-step reasoning capabilities to deliver an engaging user experience. For more information, visit my website rnoguer.com

---

## 💻 Screenshot 

<img width="1841" height="730" alt="image" src="https://github.com/user-attachments/assets/fa5a031d-e6b0-494d-b1bb-ba75390b0ad5" />


---

## ✨ Features

- **Agentic RAG Architecture**: Built using **LangGraph** and **LangChain** to orchestrate multi-step reasoning, dynamic tool usage, and precise context retrieval.
- **Optimized Vector Retrieval**: Utilizes **Chroma** as a local vectorstore paired with OpenAI's `text-embedding-3-small` for high-speed, cost-effective semantic search while keeping memory overhead minimal.
- **External Tool Integration**: Integrated with **Groq** for lightning-fast LLM inference and **Tavily Search** for live web retrieval capabilities when required by the agent.
- **Secure Authentication**: Features custom session cookie management, one-time password (OTP) email authentication, and robust rate-limiting.
- **Full-Stack Separation**: 
  - **Backend**: High-performance asynchronous REST API built with **FastAPI**.
  - **Frontend**: Responsive, modern user interface built with **Next.js** and styled with Tailwind CSS.
- **Cloud Persistence**: Configured for seamless cloud deployment on **Railway** utilizing persistent volume storage for SQLite and vector database states.

---

## 🛠️ Tech Stack

### **Backend**
- **Language**: Python 3.10+
- **Framework**: FastAPI, Uvicorn
- **AI / Orchestration**: LangChain, LangGraph
- **Vector Database**: Chroma DB
- **Embeddings & LLMs**: OpenAI Embeddings (`text-embedding-3-small`), Groq API, Tavily Search API

### **Frontend**
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **State & Communication**: Axios / Fetch API with custom session handling

### **Infrastructure & DevOps**
- **Database**: SQLite (with Railway Volume persistence)
- **Hosting**: Railway Container Deployment

---

## 📁 Project Structure

```
Portfolio/
├── backend/
│   └── main.py                        # FastAPI application entrypoint
├── frontend/
│   ├── public/
│   │   └── assets/                    # Static resources (CSS, images, JS)
│   ├── src/
│   │   ├── components/                # Reusable UI components (Nav, Footer)
│   │   └── pages/                     # Application views (Home, Agent, Projects)
│   ├── App.tsx                        # Root React component and routing
│   ├── index.css                      # Global styles and Tailwind configuration
│   ├── main.tsx                       # Frontend entry point
│   ├── index.html                     # HTML root template
│   ├── package.json                   # Node.js dependencies and scripts
│   ├── Dockerfile                     # Frontend container build configuration
│   └── nginx.conf                     # Nginx reverse proxy configuration
├── ai/
│   ├── agent/                         # LangGraph ReAct agent definition & tools
│   └── rag/                           # Indexing, document loaders, and vectorstore logic
├── helpers/
│   ├── email_verification.py          # Email verification and OTP utilities
│   ├── pretty_terminal.py             # Rich console output formatting
│   ├── sqlite3_db.py                  # SQLite database connection and operations
│   └── telegram_alert.py              # Telegram notification triggers
├── Dockerfile                         # Backend container build configuration
├── docker-compose.yml                 # Local multi-container orchestration setup
├── requirements.txt                   # Python backend dependencies
└── README.md                          # Project documentation and guide
```

---

## 👨‍💻 Author

**Rubén Nogueras** - [Portfolio](https://rnoguer.com)

---
