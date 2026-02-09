import streamlit as st
import requests

# Set the model you're using (you must have already pulled this with: ollama pull gemma)
OLLAMA_MODEL = "gemma"

def generate_sql_with_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama server not running. Please open a terminal and run: `ollama run gemma`"

def main():
    st.set_page_config(
        page_title="SQL Query Generator (Gemma)",
        page_icon="🧠",
        layout="centered"
    )

    st.title("🧠 SQL Query Generator")
    st.markdown("Using **Gemma (via Ollama)** to convert natural language to SQL — completely offline and private!")

    with st.expander("ℹ️ Instructions", expanded=False):
        st.markdown("""
        1. Make sure [Ollama](https://ollama.com) is installed.
        2. Pull the model with: `ollama pull gemma`
        3. Run the model with: `ollama run gemma`
        4. Then launch this app with: `streamlit run app.py`
        """)

    user_input = st.text_area(
        "📝 Describe your SQL query:",
        placeholder="e.g., get all users where age > 30"
    )

    if st.button("Generate SQL"):
        if not user_input.strip():
            st.warning("Please enter a description first.")
        else:
            st.info("💡 Generating SQL using Gemma...")
            prompt = f"""
You are a helpful AI assistant that converts English instructions into SQL queries.
Only return the SQL query, without explanations.

Instruction:
{user_input}
"""
            sql_code = generate_sql_with_ollama(prompt)
            st.code(sql_code, language="sql")

    st.markdown("---")
    st.caption("⚡ Powered locally by `gemma` using Ollama and Streamlit — no cloud, no API keys.")

if __name__ == "__main__":
    main()