import streamlit as st
import openai

st.set_page_config(page_title="Asistente TUPA", page_icon="🏛️")

try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("Configura openai_api_key en Settings > Secrets")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🏛️ Asistente TUPA")
st.write("Gobierno Regional del Cusco")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Pregunta sobre TUPA"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")
