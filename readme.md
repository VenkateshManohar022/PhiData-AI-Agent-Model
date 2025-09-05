# Multi-Agentic AI Task: Marketing Agent Team Setup

This repository demonstrates a **multi-agent AI workflow** using the **DeepSeek v3.1** model and the **Phidata framework**. The system features a team of three interconnected AI agents, each with specific roles, working together to extract website data, prepare marketing scripts, and send them to Telegram.

---

## 🚀 Model & Framework

- **Model:** [DeepSeek v3.1](https://lnkd.in/gf6bm67N)  
- **Framework:** [Phidata](https://lnkd.in/gwNhAK2X)  
- **GitHub Repository:** [PhiData AI Agent Model](https://lnkd.in/giy86cuC)

---

## 🧠 Agents Overview

### 1. Manager Agent
- Acts as the **central controller** of the workflow.
- Has full access to the other agents.
- Coordinates the tasks: website extraction → script summarization → Telegram delivery.
- Monitors and logs all activity across agents.

### 2. Website Data Extraction Agent
- Equipped with the **WebsiteTool** from the Phidata library.
- Extracts **relevant data** from the website you provide.
- Summarizes website content into a structured format.
- Example Usage: Provide a URL and receive the extracted textual content.

### 3. Script Preparation Agent
- Uses a **custom-built tool** for this demo.
- Integrates with the **Telegram API**.
- Converts extracted website content into **concise marketing scripts**.
- Automatically sends scripts to your Telegram account.

---

## ⚡ Features

- Multi-agent workflow with **real-time log streaming**.
- Web scraping and content summarization.
- Automated Telegram messaging for marketing scripts.
- Modular and scalable design — agents can be reused or extended for other tasks.

---

## 🔧 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/phi-data-ai-agent-model.git
   cd phi-data-ai-agent-model