# Fashion-Visual-Search-Intelligent-Styling-Assistant
# 👗✨ Stylora AI Fashion Assistant – The Intelligent Stylist

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge&logo=groq&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Similarity%20Search-4285F4?style=for-the-badge&logo=facebook&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Stylora is an **enterprise-grade AI fashion assistant** that revolutionizes how users discover outfits.  
It combines **multi-agent orchestration, LLM-powered stylists, visual search, and real-time scraping** into a seamless production-ready platform.

> 💡 *“Your personal stylist, powered by cutting-edge AI.”*

---

## ✨ Advanced Capabilities

- ✅ **Multi-Agent Architecture**  
  Specialized agents (Conversation, Stylist, Scraper, Validator)

- ✅ **LLM + Retrieval (RAG-like)**  
  Context-aware recommendations using conversational memory

- ✅ **Asynchronous & Threaded Execution**  
  Parallel scraping + non-blocking APIs for fast responses

- ✅ **Visual Search**  
  CLIP embeddings + FAISS index

- ✅ **Real-time Web Scraping**  
  Selenium-based Myntra scraping with anti-detection

- ✅ **Conversational State Management**  
  Builds evolving user style profiles

- ✅ **Color-Theory-Aware Styling**  
  Smart outfit generation based on rules + trends

---

## 🏗️ System Architecture


┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Frontend │ │ Backend API │ │ Multi-Agent │
│ (React/TS) │ <──> │ (FastAPI) │ <──> │ Orchestrator │
└─────────────────┘ └────────┬────────┘ └────────┬────────┘
│ │
┌─────────────────────────┼────────────────────────┼─────────────────────────┐
▼ ▼ ▼ ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Conversation │ │ Stylist Agent │ │ Scraper Agent │
│ Manager │ │ (LLM + Rules) │ │ (Selenium) │
│ (LLM + State) │ └─────────────────┘ └─────────────────┘
└────────┬────────┘
▼
┌─────────────────────────┐
│ FAISS + CLIP Index │
│ (Visual Search) │
└─────────────────────────┘



---

## 🧠 Multi-Agent Pipeline

| Agent                | Responsibility | Technology |
|---------------------|--------------|-----------|
| Conversation Manager | Extracts structured intent | Groq LLaMA-3.3-70B |
| Stylist Agent        | Generates outfit plans | LLM + Rules |
| Scraper Agent        | Fetches products | Selenium + Async |
| Validator Agent      | Validates outfit | Rule-based |

---

## 🔄 Data Flow (RAG-like)

1. User message → Conversation Manager → updates `collected_info`
2. When sufficient data → Stylist Agent → creates `outfit_plan`
3. Plan → Scraper Agent → generates queries → scrapes Myntra
4. Products stored in session context
5. Frontend fetches via `/products`

---

## ⚡ Performance Optimizations

- 🚀 Async FastAPI endpoints  
- 🧵 Parallel scraping (thread pools)  
- 🔁 Connection pooling  
- ⚡ In-memory caching  
- 🧠 FAISS GPU similarity search  

---

## 🛠️ Technology Stack

### Backend
- FastAPI
- Groq API (LLaMA 3.3 70B)
- Selenium
- FAISS + CLIP
- Pandas / NumPy
- Uvicorn

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Lucide Icons
- React Router

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- Groq API Key
- Chrome Browser

---

### 🔧 Installation

#### 1. Clone Repo
```bash
git clone https://github.com/Vivek2304shinde/Fashion-Visual-Search-Intelligent-Styling-Assistant.git
```
### 2. Installation
```bash
pip install -r requirements.txt
```
### 3. Frontend
```bash 
cd frontend
npm install
npm start
```
### 4. Backend
```bash
python alternative_main.py
```


## 🎯 Usage Guide

### 🔍 Visual Search
Upload image → get similar products instantly

### 💬 AI Stylist

Start chat:

>*I need a navy blue outfit for a wedding*

AI gathers preferences → generates full outfit plan











