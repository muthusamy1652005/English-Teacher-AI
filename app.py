import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="English Tutor AI", page_icon="👨‍🏫", layout="centered")

# --- SECURE API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        st.stop()
else:
    st.error("Secrets-la 'GEMINI_API_KEY' illa nanba!")
    st.stop()

# --- TEACHER SYSTEM PROMPT ---
TEACHER_PROMPT = (
    "Act as a patient and friendly English Teacher named 'Gemini Nanban'. "
    "Check for grammar mistakes, explain them simply, and provide the correct version."
)

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
            # TRYING 'gemini-pro' INSTEAD OF 'gemini-1.5-flash'
            # Ithu ella API key-kum support aagum
            model = genai.GenerativeModel('gemini-pro')
            
            full_query = f"{TEACHER_PROMPT}\n\nStudent says: {prompt}"
            
            with st.spinner("Thinking..."):
                response = model.generate_content(full_query)
                teacher_reply = response.text
            
            st.markdown(teacher_reply)
            st.session_state.messages.append({"role": "assistant", "content": teacher_reply})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Nanba, 'gemini-pro' mathiyum varalana sollunga, vera oru solution iruku!")

