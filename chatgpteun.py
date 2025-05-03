
import streamlit as st
import pdfplumber
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="ChatGPTeun", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: white;'>ChatGPTeun – PDF Assistent</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Upload een PDF en stel er vragen over. ChatGPTeun helpt je!</p><br>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload een PDF-bestand", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""

    st.success("PDF succesvol geladen!")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("### Stel een vraag over het document:")
    question = st.text_input("", placeholder="Bijv. Wat is de conclusie op pagina 2?")

    if st.button("Beantwoord vraag") and question:
        prompt = f"Het volgende document is geüpload:\n\n{full_text[:3000]}\n\nVraag: {question}\nAntwoord:"

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Je bent een behulpzame PDF-assistent genaamd ChatGPTeun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3,
            )
            answer = response.choices[0].message.content.strip()
            st.session_state.history.append((question, answer))
        except Exception as e:
            st.error(f"Fout bij het ophalen van antwoord: {e}")
            answer = None

    if st.session_state.history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Antwoorden")
        for q, a in st.session_state.history[::-1]:
            with st.container():
                st.markdown(f"<b>Vraag:</b> {q}", unsafe_allow_html=True)
                st.markdown(f"<b>Antwoord:</b><br>{a}", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
