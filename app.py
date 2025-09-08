import streamlit as st
import openai

st.set_page_config(
    page_title="Asistente TUPA",
    page_icon="🏛️",
    layout="centered"
)

# CSS
st.markdown("""
<style>
.stApp {
    background: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}
.chat-message {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
}
.user-message {
    background: #2563eb;
    color: white;
    margin-left: 20%;
}
.assistant-message {
    background: white;
    border: 1px solid #e2e8f0;
    margin-right: 20%;
}
</style>
""", unsafe_allow_html=True)

# Base de conocimientos TUPA
RESPUESTAS_TUPA = {
    "licencia": """
    **LICENCIA DE FUNCIONAMIENTO - GORE CUSCO**
    
    📋 **Requisitos:**
    • Solicitud dirigida al Alcalde
    • Vigencia de poder del representante legal
    • Declaración Jurada de Condiciones de Seguridad
    • Copia del RUC y DNI
    • Copia de Licencia Municipal (cuando corresponda)
    
    ⏰ **Plazo:** 15 días hábiles
    💰 **Costo:** S/ 45.00
    """,
    
    "construccion": """
    **PERMISO DE CONSTRUCCIÓN - GORE CUSCO**
    
    📋 **Requisitos:**
    • Solicitud FUE con declaración jurada
    • Copia literal del dominio
    • Certificado de Zonificación
    • Planos de arquitectura y estructuras
    • Memoria descriptiva
    • Estudio de mecánica de suelos (obras mayores)
    
    ⏰ **Plazo:** 30 días hábiles
    💰 **Costos:**
    - Hasta 120 m²: S/ 180.00
    - 121 a 500 m²: S/ 350.00
    - Más de 500 m²: S/ 650.00
    """,
    
    "horarios": """
    **HORARIOS DE ATENCIÓN - GORE CUSCO**
    
    🕘 **Horarios Generales:**
    • Gerencia Regional: Lunes a Viernes 09:00 - 16:30
    • Gerencia de Salud: Lunes a Viernes 09:00 - 16:00
    • Gerencia de Agricultura: Lunes a Viernes 08:30 - 17:00
    • Gerencia de Educación: Lunes a Viernes 08:30 - 16:30
    
    📍 **Ubicaciones:**
    • Sede Principal: Av. El Sol 101, Cusco
    • Mesa de Partes: 08:00 - 16:00
    """,
    
    "costos": """
    **TASAS Y COSTOS - GORE CUSCO**
    
    💰 **Principales Tasas:**
    • Certificado de Zonificación: S/ 25.00
    • Licencia de Funcionamiento: S/ 45.00
    • Permiso de Construcción: S/ 180.00 - S/ 650.00
    • Certificado de Compatibilidad: S/ 35.00
    • Inspección Técnica: S/ 120.00
    
    📝 **Formas de Pago:**
    • Banco de la Nación
    • Caja de la institución
    • Pagos electrónicos
    """
}

def buscar_respuesta(consulta):
    consulta_lower = consulta.lower()
    
    if any(word in consulta_lower for word in ["licencia", "funcionamiento"]):
        return RESPUESTAS_TUPA["licencia"]
    elif any(word in consulta_lower for word in ["construccion", "construcción", "permiso", "obra"]):
        return RESPUESTAS_TUPA["construccion"]
    elif any(word in consulta_lower for word in ["horario", "horarios", "atencion", "atención", "oficina"]):
        return RESPUESTAS_TUPA["horarios"]
    elif any(word in consulta_lower for word in ["costo", "costos", "precio", "tasa", "pago"]):
        return RESPUESTAS_TUPA["costos"]
    else:
        return """
        **INFORMACIÓN GENERAL - TUPA GORE CUSCO**
        
        El TUPA (Texto Único de Procedimientos Administrativos) contiene todos los trámites del Gobierno Regional del Cusco.
        
        🔍 **Puedes consultar sobre:**
        • Licencias de funcionamiento
        • Permisos de construcción
        • Horarios de atención
        • Tasas y costos
        
        📞 **Contacto:** Mesa de Partes - Av. El Sol 101, Cusco
        """

# Estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #1e40af; margin: 0;">🏛️ Asistente TUPA</h1>
    <p style="color: #64748b; margin: 0.5rem 0;">Gobierno Regional del Cusco</p>
    <p style="color: #94a3b8; font-size: 0.9rem;">Consultas sobre procedimientos administrativos</p>
</div>
""", unsafe_allow_html=True)

# Botones de consultas rápidas
if not st.session_state.messages:
    st.markdown("### 💡 Consultas Frecuentes")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Licencia de Funcionamiento", use_container_width=True):
            consulta = "¿Qué documentos necesito para una licencia de funcionamiento?"
            st.session_state.messages.append({"role": "user", "content": consulta})
            respuesta = buscar_respuesta(consulta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.rerun()
            
        if st.button("⏰ Horarios de Atención", use_container_width=True):
            consulta = "¿Cuáles son los horarios de atención?"
            st.session_state.messages.append({"role": "user", "content": consulta})
            respuesta = buscar_respuesta(consulta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.rerun()
    
    with col2:
        if st.button("🏗️ Permisos de Construcción", use_container_width=True):
            consulta = "¿Qué necesito para un permiso de construcción?"
            st.session_state.messages.append({"role": "user", "content": consulta})
            respuesta = buscar_respuesta(consulta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.rerun()
            
        if st.button("💰 Tasas y Costos", use_container_width=True):
            consulta = "¿Cuáles son las tasas y costos?"
            st.session_state.messages.append({"role": "user", "content": consulta})
            respuesta = buscar_respuesta(consulta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.rerun()

# Mostrar conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu consulta sobre el TUPA..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generar respuesta
    with st.spinner("Buscando información..."):
        respuesta = buscar_respuesta(prompt)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
    
    st.rerun()

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Información")
    st.success("🟢 Sistema Activo")
    st.metric("Consultas", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    if st.button("🔄 Nueva Conversación"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    **📍 Ubicación:**  
    Av. El Sol 101, Cusco
    
    **📞 Teléfono:**  
    (084) 201-230
    
    **🕘 Atención:**  
    Lunes a Viernes  
    08:00 - 16:00
    """)
