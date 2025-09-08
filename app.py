import streamlit as st

st.title("🏛️ Asistente TUPA - Test")
st.write("Si ves esto, Streamlit funciona")

try:
    import openai
    st.success("✅ OpenAI importado correctamente")
    
    try:
        api_key = st.secrets["openai_api_key"]
        st.success("✅ API Key encontrada")
        st.write(f"API Key: {api_key[:10]}...")
    except KeyError:
        st.error("❌ No se encontró openai_api_key en secrets")
        
except ImportError:
    st.error("❌ No se pudo importar OpenAI")
