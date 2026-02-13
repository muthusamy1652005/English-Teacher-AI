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
        st.error(f"Configuration Error: {e}")
        st.stop()
else:
    st.error("Secrets-la API key illa nanba!")
    st.stop()

# --- TEACHER SYSTEM PROMPT ---
TEACHER_PROMPT = (
    "Act as a patient and friendly English Teacher named 'Gemini Nanban'. "
    "Check for grammar mistakes, explain them simply in English, "
    "and provide the corrected version. Always reply to keep the conversation going."
)

st.title("👨‍🏫 My AI English Tutor")
st.markdown("---")

# History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
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
            # TRYING THE MOST STABLE MODEL NAME FOR NEW KEYS
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            full_query = f"{TEACHER_PROMPT}\n\nStudent says: {prompt}"
            
            with st.spinner("Teacher is thinking..."):
                response = model.generate_content(full_query)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # SECOND TRY WITH ALTERNATIVE MODEL NAME IF FLASH FAILS
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response_alt = model_alt.generate_content(f"{TEACHER_PROMPT}\nStudent: {prompt}")
                st.markdown(response_alt.text)
                st.session_state.messages.append({"role": "assistant", "content": response_alt.text})
            except Exception as e2:
                st.error(f"Actual Error: {str(e2)}")
                st.info("Nanba, intha error message-ah screenshot anuppunga!")


