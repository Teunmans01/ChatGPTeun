import streamlit as st
import pdfplumber
import openai

# Haal OpenAI API-sleutel op uit Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ChatGPTeun", page_icon="🤖")
st.title("🤖 ChatGPTeun – PDF Chatbot")

uploaded_file = st.file_uploader("📄 Upload een PDF-bestand", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""

    st.success("✅ PDF succesvol geladen!")

    if "history" not in st.session_state:
        st.session_state.history = []

    question = st.text_input("Stel een vraag over het document:")

    if st.button("Stel vraag") and question:
        prompt = f"Het volgende document is geüpload:\n\n{full_text[:3000]}\n\nVraag: {question}\nAntwoord:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Je bent een behulpzame PDF-assistent genaamd ChatGPTeun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3,
            )
            answer = response.choices[0].message["content"].strip()
            st.session_state.history.append((question, answer))
        except Exception as e:
            st.error(f"Fout bij het ophalen van antwoord: {e}")
            answer = None

    for q, a in st.session_state.history[::-1]:
        st.markdown(f"**👤 Vraag:** {q}")
        st.markdown(f"**🤖 ChatGPTeun:** {a}")
        st.markdown("---")
