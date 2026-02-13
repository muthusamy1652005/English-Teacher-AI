import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="English Tutor AI", page_icon="👨‍🏫", layout="centered")

# --- SECURE API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"].strip()
        # Inga namma explicitly version specify pannuvom
        genai.configure(api_key=API_KEY, transport='grpc') 
    except Exception as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
else:
    st.error("Secrets-la API key illa nanba!")
    st.stop()

st.title("👨‍🏫 My AI English Tutor")

# History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT & AI LOGIC ---
if prompt := st.chat_input("Type your English sentence here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # TRYING THE MOST COMPATIBLE MODEL NAME
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            
            instruction = "Act as an English teacher. Correct grammar mistakes and reply friendly."
            
            with st.spinner("Teacher is thinking..."):
                # Beta feature use pannama simple-aa request anuppuvom
                response = model.generate_content(f"{instruction}\nStudent: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Oru velai flash-latest work aagalana, 'gemini-1.5-flash-001' try pannuvom
            try:
                model_alt = genai.GenerativeModel('gemini-1.5-flash-001')
                response = model_alt.generate_content(f"Teacher: {prompt}")
                st.markdown(response.text)
            except Exception as e2:
                st.error(f"Actual Error: {str(e2)}")
                st.info("Nanba, unga API key romba restrict aagi irukku pola. Fresh API Key use panna try pannunga!")


