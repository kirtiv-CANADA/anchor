# ⚓ Anchor — AI Caregiver Support Tool

An AI-powered caregiver support tool that remembers what works — turning everyday questions into a personal knowledge base.

Built for ForgeHacks Online 2026 — Track: AI + Healthcare

Live Demo: https://anchor-caregiver.streamlit.app

Demo Video: https://youtu.be/uwWJreIBK-Y

---

## The Problem

Caregivers ask questions constantly — about sleep, behavior, routines, and communication. They search Google, ask friends, read articles. Sometimes they find useful answers, sometimes they don't. And almost never can they remember what worked last time.

There is no tool that learns from a caregiver's own experience.

---

## What Anchor Does

Anchor is a web app for caregivers:

- Ask a question — anything a caregiver needs help with
- Get an AI-generated answer — clear, practical, in bullet points
- Rate the answer — Worked or Didn't work
- Build a personal knowledge base — every question and answer is saved

When a similar question is asked later, Anchor surfaces the past answer alongside the new one, using TF-IDF vector similarity.

It's not a chatbot. It's a personal knowledge base that happens to use AI.

---

## Key Features

- AI-powered answers via Groq's LLM API
- Persistent question history in SQLite
- Similarity search using TF-IDF + cosine similarity
- Theme detection across 8 caregiver topics
- Feedback loop to track what helped
- Built with Streamlit

---

## How to Run Locally

Requirements: Python 3.11+ and a free Groq API key from https://console.groq.com

Steps:

1. Clone the repository: `git clone https://github.com/kirtiv-CANADA/anchor.git`
2. Enter the folder: `cd anchor`
3. Create a virtual environment: `python -m venv venv`
4. Activate it (Windows): `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a .env file with: `GROQ_API_KEY=your_key_here`
7. Run: `streamlit run app.py`

The app opens at http://localhost:8501

---

## Technologies Used

- Python 3.11
- Streamlit
- SQLite
- Groq API (openai/gpt-oss-120b)
- scikit-learn (TF-IDF + cosine similarity)
- python-dotenv
- Streamlit Community Cloud
- Git + GitHub

---

## Project Structure

- app.py — Main Streamlit application
- database.py — SQLite helpers and similarity search
- requirements.txt — Python dependencies
- .gitignore — Excludes .env, venv/, data/
- README.md — This file

---

## What's Next

- User accounts with Google Sign-In
- Mobile-optimized interface
- Export answers as PDF
- Weekly summary emails
- Bilingual support (English + French)

---

## Author

Kirti — https://github.com/kirtiv-CANADA

Built solo for ForgeHacks Online 2026.

---

## License

MIT License
