# 🤖 AI-Powered Server Health Agent

An autonomous, human-in-the-loop infrastructure management agent designed to monitor system health, diagnose resource bottlenecks using the Google Gemini API, request explicit safety approval, and execute corrective terminal commands safely.

---

## 🚀 Architectural Flow (The Agentic Loop)
This project moves beyond passive text generation by implementing a complete autonomous agent cycle:
1. **Perceive:** Gathers real-time host metrics (CPU, RAM, Disk) using `psutil`.
2. **Reason:** Feeds raw metrics to **Google Gemini (`gemini-2.5-flash`)** to act as a senior Linux system administrator.
3. **Plan:** The LLM analyzes the state and formulates a specific, safe CLI command to resolve bottlenecks.
4. **Safety Gate:** Pauses execution and requires explicit human approval (`y/n`) before touching the host system.
5. **Act:** Securely runs the approved command via Python's `subprocess` module and reports back results.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 3.11+
* **AI Engine:** Google GenAI SDK (`google-genai`)
* **System Monitoring:** `psutil`
* **Containerization:** Docker (WSL2 / Linux lightweight container runtime)

---

## 📂 Project Structure
```text
server-health-agent/
│
├── health_agent.py      # Core agent script (Metrics, AI call, Safety gate, Execution)
├── Dockerfile           # Multi-stage/lightweight Linux container configuration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

⚙️ Quick Start & Local Setup
Clone or download this repository.

Install dependencies:

Bash
pip install -r requirements.txt
Set your Google Gemini API Key:

Windows (PowerShell): $env:GEMINI_API_KEY="your_api_key"

Linux/Mac: export GEMINI_API_KEY="your_api_key"

Run the Agent:

Bash
python health_agent.py
🐳 Running via Docker (Containerized Linux Environment)
To run the agent inside an isolated Linux container:

Build the Docker image:

Bash
docker build -t server-health-agent .
Run the containerized agent:

Bash
docker run --rm -it -e GEMINI_API_KEY="your_api_key" server-health-agent