# ⚓ Anchor — AI Caregiver Support Tool

An AI-powered caregiver support tool that remembers what works — turning everyday questions into a personal knowledge base.

Built for **ForgeHacks Online 2026** — Track: **AI + Healthcare**

🔗 **Live Demo:** [https://anchor-caregiver.streamlit.app](https://anchor-caregiver.streamlit.app)

🎥 **Demo Video:** [https://youtu.be/uwWJreIBK-Y](https://youtu.be/uwWJreIBK-Y)

---

## The Problem

Caregivers ask questions constantly — about sleep, behavior, routines, and communication. They search Google, ask friends, read articles. Sometimes they find useful answers, sometimes they don't. And almost never can they remember what worked last time.

There is no tool that learns from a caregiver's own experience.

---

## What Anchor Does

Anchor is a web app for caregivers. Users:

1. **Ask a question** — anything a caregiver needs help with
2. **Get an AI-generated answer** — clear, practical, in bullet points
3. **Rate the answer** — 👍 Worked or 👎 Didn't work
4. **Build a personal knowledge base** — every question and answer is saved

When a similar question is asked later, Anchor **surfaces the past answer** alongside the new one, using TF-IDF vector similarity to find matches from the user's own history.

Anchor also **detects themes** across questions — sleep, behavior, routine, communication, anxiety, focus — and tracks what's worked over time.

**It's not a chatbot. It's a personal knowledge base that happens to use AI.**

---

## Key Features

- 🧠 **AI-powered answers** via Groq's LLM API (Llama-based models)
- 📚 **Persistent question history** in SQLite
- 🔍 **Similarity search** using TF-IDF + cosine similarity (scikit-learn)
- 📊 **Theme detection** — categorizes questions across 8 caregiver topics
- 👍 **Feedback loop** — track which answers actually helped
- ⚡ **Fast, single-page app** built with Streamlit

---

## How to Run Locally

### Prerequisites
- Python 3.11 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/kirtiv-CANADA/anchor.git
cd anchor

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the project root
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# 5. Run the app
streamlit run app.py


The app will open at http://localhost:8501.

Technologies Used
Layer	Technology
Language	Python 3.11
Web framework	Streamlit
Storage	SQLite
LLM	Groq API (openai/gpt-oss-120b)
Retrieval	scikit-learn (TF-IDF + cosine similarity)
Secrets	python-dotenv (local), Streamlit Secrets (production)
Deployment	Streamlit Community Cloud
Version control	Git + GitHub
Project Structure
text
anchor/
├── app.py              # Main Streamlit application
├── database.py         # SQLite helpers + similarity search
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes .env, venv/, data/
├── .env                # (local only) Groq API key — NOT in repo
└── README.md           # This file
Architecture
text
User Input
   ↓
Streamlit UI (app.py)
   ↓
┌─────────────────────┬──────────────────────┐
│ Similarity Search   │  LLM API Call        │
│ (TF-IDF over        │  (Groq's             │
│  user's history)    │   openai/gpt-oss)    │
└─────────────────────┴──────────────────────┘
   ↓
Combined Response + Save to SQLite
   ↓
Display in UI + Add Feedback Buttons
What's Next
🔐 User accounts with Google Sign-In (in progress)

📱 Mobile-optimized interface

📤 Export answers as PDF or share with a child's therapist

📧 Weekly summary emails

🌐 Bilingual support (English + French)

Author
Kirti — https://github.com/kirtiv-CANADA

Built solo for ForgeHacks Online 2026.

License
MIT License — free to use, modify, and share.