import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="My AI English Tutor", page_icon="👨‍🏫", layout="centered")

# --- API KEY LOADING ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        # Versioning issue fix panna explicitly transport set panrom
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"API Setup Error: {e}")
        st.stop()
else:
    st.error("Secrets-la API key illa nanba!")
    st.stop()

# --- TEACHER PROMPT ---
TEACHER_PROMPT = (
    "Act as a patient and friendly English Teacher named 'Gemini Nanban'. "
    "Check for grammar mistakes, explain them simply, and provide the correct version. "
    "Reply naturally to keep the conversation going."
)

st.title("👨‍🏫 My AI English Tutor")

# History setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Type your English sentence here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # TRYING THE MOST COMPATIBLE MODEL NAME FOR V1BETA ERROR
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            with st.spinner("Teacher is thinking..."):
                response = model.generate_content(f"{TEACHER_PROMPT}\nStudent: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # If flash-latest fails, trying the generic gemini-pro
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response_alt = model_alt.generate_content(f"{TEACHER_PROMPT}\nStudent: {prompt}")
                st.markdown(response_alt.text)
                st.session_state.messages.append({"role": "assistant", "content": response_alt.text})
            except Exception as e2:
                st.error(f"Detailed Error: {str(e2)}")
                st.info("Nanba, fresh API key generate panni 5 mins wait panni try pannunga!")




