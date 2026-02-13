import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="My AI English Tutor", page_icon="👨‍🏫")

# --- SECURE API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"API Setup Error: {e}")
        st.stop()
else:
    st.error("Secrets-la API key illa nanba!")
    st.stop()

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
            # Model selection: Explicit name usage
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            instruction = "Act as a friendly English teacher. Correct grammar mistakes and reply naturally."
            
            with st.spinner("Teacher is thinking..."):
                # Simplified response call
                response = model.generate_content(f"{instruction}\nStudent says: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Fallback for 404 models error
            st.error(f"Model Error: {str(e)}")
            st.info("Nanba, unga API key (Screenshot 14) correct-ah Secrets-la save aagi irukkunnu check pannunga.")






