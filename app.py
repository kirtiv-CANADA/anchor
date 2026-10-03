import streamlit as st
import requests
import os
from dotenv import load_dotenv
from database import (
    init_db, save_qa, get_all_history, clear_history, find_similar,
    set_feedback, detect_themes
)

load_dotenv()

init_db()

st.set_page_config(page_title="Anchor", page_icon="⚓", layout="wide")

st.title("⚓ Anchor")
st.write("Never lose what you've learned.")

st.divider()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"


def ask_ai(question):
    """Send a question to the AI and get a fresh answer."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Anchor, a helpful assistant for caregivers. "
                    "Give clear, practical answers in 3-5 short bullet points. "
                    "Be warm and direct. No medical diagnoses."
                )
            },
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            return f"❌ ERROR {response.status_code}\n\n{response.text}"
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Exception: {str(e)}"


# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("📚 Your Past Questions")
    history = get_all_history()

    if not history:
        st.caption("No questions yet. Ask one to get started.")
    else:
        st.caption(f"{len(history)} question(s) saved")
        for row in history:
            qid, q, a, ts, fb = row
            date_str = ts[:10]
            icon = "👍" if fb == "up" else "👎" if fb == "down" else "  "
            with st.expander(f"{icon} {date_str} — {q[:38]}..."):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:**\n\n{a}")
                if fb:
                    st.caption(f"Your feedback: {'👍 worked' if fb == 'up' else '👎 did not work'}")

    st.divider()

    # Patterns section
    themes = detect_themes()
    if themes:
        st.header("📊 Patterns")
        st.caption("What you're asking about most")
        sorted_themes = sorted(themes.items(), key=lambda x: x[1]["count"], reverse=True)
        for name, data in sorted_themes:
            st.markdown(f"**{name}** — {data['count']} question(s)")
            if data["worked"]:
                st.caption(f"  ✅ Worked: {data['worked']}")
            if data["not_worked"]:
                st.caption(f"  ❌ Didn't work: {data['not_worked']}")
        st.divider()

    if st.button("🗑️ Clear all history"):
        clear_history()
        st.rerun()


# ---------- MAIN ----------
st.subheader("Ask a question")
question = st.text_input(
    "Type your question here:",
    placeholder="e.g., What helps with bedtime resistance?"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please type a question first.")
    elif not API_KEY:
        st.error("API key missing. Check your .env file.")
    else:
        # Similar past questions
        similar = find_similar(question)
        if similar:
            st.info("📌 You asked something similar before. Here's what you found last time:")
            for item in similar:
                with st.expander(f"{item['date']} — {item['question']}  (similarity {item['score']})"):
                    st.markdown(item['answer'])
            st.divider()

        # Fresh AI answer
        with st.spinner("Thinking..."):
            answer = ask_ai(question)

        # Save and remember the row id
        new_id = save_qa(question, answer)

        st.success("Answer:")
        st.markdown(answer)
        st.caption("✅ Saved to your history")

        # Feedback buttons
        st.markdown("**Did this help?**")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍 Worked", key=f"up_{new_id}"):
                set_feedback(new_id, "up")
                st.success("Thanks! Marked as worked.")
        with col2:
            if st.button("👎 Didn't work", key=f"down_{new_id}"):
                set_feedback(new_id, "down")
                st.info("Thanks! Marked as did not work.")