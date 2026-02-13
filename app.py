import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="English Tutor AI", page_icon="👨‍🏫", layout="centered")

# --- SECURE API KEY LOADING ---
# GitHub-la key-ah direct-ah podama, Streamlit Cloud settings-la "Secrets"-la poduvom.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Nanba, Streamlit Secrets-la 'GEMINI_API_KEY' set panna marandhuteenga!")
    st.stop()

# --- SYSTEM PROMPT ---
TEACHER_PROMPT = (
    "Act as a patient and friendly English Teacher named 'Gemini Nanban'. "
    "Your goal is to help the user practice English. "
    "1. Always check for grammar mistakes in the student's message. "
    "2. If there's a mistake, explain it simply in English and give the correct version. "
    "3. If the sentence is correct, praise the student. "
    "4. Always reply to their message to keep the conversation flowing naturally."
)

# --- UI DESIGN ---
st.title("👨‍🏫 Gemini English Tutor")
st.markdown("---")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Enga, English-la ethachum type pannunga..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Teacher AI Response Logic
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Sending full context for better tutoring
            full_query = f"{TEACHER_PROMPT}\n\nStudent says: {prompt}"
            
            with st.spinner("Teacher is thinking..."):
                response = model.generate_content(full_query)
                teacher_reply = response.text
                
            st.markdown(teacher_reply)
            
            # Save assistant reply to history
            st.session_state.messages.append({"role": "assistant", "content": teacher_reply})
        except Exception as e:
            st.error("Sorry nanba, server-la chinna problem. Konja neram kazhichu try pannunga.")