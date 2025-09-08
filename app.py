import streamlit as st
import openai
import time
import re
from typing import Optional

# Configuración
st.set_page_config(
    page_title="Asistente TUPA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar OpenAI
try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("Configura openai_api_key en Streamlit Cloud Settings > Secrets")
    st.stop()

# CSS
st.markdown("""
<style>
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #059669;
        --background: #ffffff;
        --surface: #f8fafc;
        --border: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --radius: 12px;
    }

    .stApp {
        background: var(--background);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    }
    
    .mini-header {
        text-align: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.95);
    }
    
    .mini-header h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .hero-section {
        text-align: center;
        padding: 4rem 2rem 3rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin: 0 0 0.5rem 0;
        font-weight: 400;
    }

    .stChatMessage {
        background: transparent !important;
        padding: 1.5rem 0 !important;
        border: none !important;
        margin: 0 !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div {
        background: var(--primary-color) !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: auto !important;
        max-width: 70% !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] > div {
        background: var(--surface) !important;
        color: var(--text-primary) !important;
        padding: 1.5rem !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: auto !important;
        max-width: 85% !important;
        box-shadow: var(--shadow-sm) !important;
        border: 1px solid var(--border) !important;
    }

    .stChatInputContainer {
        background: white !important;
        border: 2px solid var(--border) !important;
        border-radius: 24px !important;
        box-shadow: var(--shadow-lg) !important;
        max-width: 800px !important;
        margin: 2rem auto !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), var(--shadow-lg) !important;
    }

    footer { display: none; }
    header[data-testid="stHeader"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Funciones
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def call_openai(prompt: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en el TUPA (Texto Único de Procedimientos Administrativos) del Gobierno Regional del Cusco. Responde de manera clara y útil sobre trámites, requisitos, plazos y costos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error procesando consulta: {e}"

def process_query(user_query: str):
    if not user_query.strip():
        return
    
    st.session_state.messages.append(("user", user_query))
    
    with st.spinner("Procesando consulta..."):
        response = call_openai(user_query)
        st.session_state.messages.append(("assistant", response))

# UI Principal
init_session()

# Sidebar
with st.sidebar:
    st.header("🏛️ Asistente TUPA")
    st.divider()
    
    st.subheader("📊 Estado")
    st.metric("Conexión OpenAI", "🟢 Activa")
    st.metric("Mensajes", len(st.session_state.messages))
    
    st.divider()
    
    if st.button("🔄 Nueva Conversación", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()

# Header cuando hay mensajes
if st.session_state.messages:
    st.markdown("""
        <div class="mini-header">
            <h3>🏛️ Asistente TUPA</h3>
        </div>
    """, unsafe_allow_html=True)

# Hero section
if not st.session_state.messages:
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">Asistente TUPA</h1>
            <p class="hero-subtitle">Gobierno Regional del Cusco</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Licencia de Funcionamiento", use_container_width=True):
            process_query("¿Qué documentos necesito para obtener una licencia de funcionamiento?")
            st.rerun()
    
    with col2:
        if st.button("🏗️ Permisos de Construcción", use_container_width=True):
            process_query("¿Cuánto tiempo demora el trámite de permiso de construcción?")
            st.rerun()
    
    with col3:
        if st.button("⏰ Horarios de Atención", use_container_width=True):
            process_query("¿Cuáles son los horarios de atención de las oficinas?")
            st.rerun()
    
    with col4:
        if st.button("💰 Tasas y Costos", use_container_width=True):
            process_query("¿Cuánto cuesta un certificado de zonificación?")
            st.rerun()

# Mostrar mensajes
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# Input del chat
if prompt := st.chat_input("Pregunta sobre procedimientos del TUPA..."):
    process_query(prompt)
    st.rerun()
