import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="English Tutor AI", page_icon="👨‍🏫", layout="centered")

# --- SECURE API KEY LOADING ---
# Streamlit Secrets-la irunthu key-ah load panrom
if "GEMINI_API_KEY" in st.secrets:
    try:
        # Key-la spaces irundha remove panna .strip() use panrom
        API_KEY = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.error(f"API Configuration-la error nanba: {e}")
        st.stop()
else:
    st.error("Secrets-la 'GEMINI_API_KEY' set panna marandhuteenga! Check 'Manage App -> Settings -> Secrets'.")
    st.stop()

# --- TEACHER SYSTEM PROMPT ---
TEACHER_PROMPT = (
    "Act as a patient and friendly English Teacher named 'Gemini Nanban'. "
    "Check for grammar mistakes, explain them simply in English, "
    "and provide the corrected version. Always reply to keep the conversation going."
)

st.title("👨‍🏫 My AI English Tutor")
st.markdown("---")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT & AI LOGIC ---
if prompt := st.chat_input("Type your English sentence here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Teacher Response Logic
    with st.chat_message("assistant"):
        try:
            # Gemini 1.5 Flash model setup
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Combine instruction with user prompt
            full_query = f"{TEACHER_PROMPT}\n\nStudent says: {prompt}"
            
            with st.spinner("Nanba, teacher yosikiraaru..."):
                response = model.generate_content(full_query)
                teacher_reply = response.text
            
            st.markdown(teacher_reply)
            # Save assistant reply to history
            st.session_state.messages.append({"role": "assistant", "content": teacher_reply})
            
        except Exception as e:
            # Detailed error-ah screen-la kaaturom debugging-kaga
            st.error(f"Detailed Error: {str(e)}")
            st.info("Intha error message-ah screenshot anuppunga nanba!")
