# 🛒 AI Sales Intelligence Assistant

An AI-powered sales analytics application that combines business intelligence, data analysis, and LLM-based insights to help users understand sales performance through natural language questions.

---

## Project Overview

This project allows users to upload sales datasets and interact with the data using plain English questions.

The system:
- analyzes sales performance,
- generates business summaries,
- identifies high and low performing regions,
- and provides AI-assisted business insights.

The application uses Hugging Face LLM integration with a fallback rule-based insight engine to ensure the app remains functional even if the LLM fails.

---

## Features

### Sales Analysis
- Total sales and profit tracking
- Region performance analysis
- Product category insights
- Business summary generation

---

### AI-Powered Insights
Users can ask questions such as:
- Why is profit low?
- Which region performs worst?
- Which category performs best?
- What business risks exist?

The app generates:
- business explanations,
- analytical insights,
- and recommendations.

---

### Fallback Intelligence System
If the Hugging Face API fails or becomes unavailable, the app automatically switches to a rule-based business insight engine.

---

###Interactive Interface
Built with Streamlit for:
- dataset uploads,
- AI interaction,
- business reporting,
- and analytics visualization.

---

## Project Architecture

```text
Sales Dataset
      ↓
Data Cleaning
      ↓
Business Analysis
      ↓
Context Generation
      ↓
LLM / Fallback Engine
      ↓
AI Business Insights
      ↓
Streamlit Interface
```

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming |
| Pandas | Data analysis |
| Streamlit | Web application |
| Hugging Face | LLM inference |
| NLP | AI insight generation |

---

## 📂 Project Structure

```text
ai-sales-intelligence/
│── app.py
│── README.md
│── requirements.txt
│── .gitignore
│
├── data/
│   ├── Sample - Superstore.csv
│   └── superstore_clean.csv
│
├── src/
│   ├── __init__.py
│   ├── load_data.py
│   ├── analyze_data.py
│   └── llm_engine.py
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Run helper scripts

```bash
python src/load_data.py
python src/analyze_data.py
```

---

### 3️⃣ Start Streamlit app

```bash
python -m streamlit run app.py
```

---

## Hugging Face Configuration

Create:

```text
.streamlit/secrets.toml
```

Add your Hugging Face token locally:

```toml
HF_TOKEN = "YOUR_TOKEN_HERE"
HF_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
```

---

## Example Questions

- Why is profit low in some regions?
- Which region performs worst?
- What category performs best?
- Give a sales performance summary.
- What business recommendations would you suggest?

---

## Business Value

This project demonstrates how AI and data analytics can work together to:
- support business decision-making,
- identify sales weaknesses,
- improve operational awareness,
- and generate executive-level insights.

---

## Future Improvements

- SQL database integration
- Better visualization dashboards
- Real-time sales ingestion
- Advanced LLM prompting
- RAG (Retrieval-Augmented Generation)
- Chat memory and conversation history

---

## Author
Joshua OBIKUNLE