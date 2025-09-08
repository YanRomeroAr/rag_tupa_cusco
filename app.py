import streamlit as st

st.title("🏛️ Asistente TUPA - Test")
st.write("Si ves esto, Streamlit funciona")

try:
    import openai
    st.success("✅ OpenAI importado correctamente")
    
    try:
        openai.api_key = st.secrets["openai_api_key"]
        st.success("✅ API Key configurada")
        
        # Test simple
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hola"}]
        )
        st.success("✅ OpenAI funciona correctamente")
        st.write("Respuesta de prueba:", response.choices[0].message.content)
        
    except KeyError:
        st.error("❌ No se encontró openai_api_key en secrets")
    except Exception as e:
        st.error(f"❌ Error con OpenAI: {e}")
        
except ImportError:
    st.error("❌ No se pudo importar OpenAI")
