import os
import json
import base64
import streamlit as st
from agent_core import get_groq_client, MODEL_NAME, tools, SYSTEM_PROMPT
from agent_tools import search_products, get_products_by_team

st.set_page_config(
    page_title="El Camisetero - Classic Football Shirts",
    page_icon="⚽",
    layout="wide"
)

# Función para convertir la imagen local a Base64
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            ext = os.path.splitext(file_path)[1].replace(".", "")
            return f"data:image/{ext};base64,{encoded}"
    return None

logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if not os.path.exists(logo_path):
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")

logo_b64 = get_image_base64(logo_path)

# Estilos CSS en modo oscuro
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Poppins:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #0E1117;
    }

    .header-card {
        background: linear-gradient(135deg, #1E2640 0%, #0F172A 100%);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 1.5rem 1.2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
    }

    .header-logo {
        width: 75px;
        height: 75px;
        object-fit: contain;
        margin-bottom: 0.6rem;
        border-radius: 50%;
        background-color: #FFFFFF;
        padding: 5px;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.2);
    }

    .header-card h1 {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }

    .header-card h3 {
        font-family: 'Poppins', sans-serif;
        color: #00E676;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
    }

    .header-card p {
        color: #94A3B8;
        font-size: 0.85rem;
        font-style: italic;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Layout en dos columnas: Izquierda (Buscador 35%), Derecha (Resultados 65%)
col_left, col_right = st.columns([1, 2], gap="medium")

# --- COLUMNA IZQUIERDA: Búsqueda y Marca ---
with col_left:
    logo_html = f'<img src="{logo_b64}" class="header-logo" alt="Logo">' if logo_b64 else '⚽'

    st.markdown(f"""
        <div class="header-card">
            {logo_html}
            <h1>El Camisetero</h1>
            <h3>Asistente comercial de indumentaria futbolera en tiempo real</h3>
            <p>(Tu ayuda en Classic Football Shirts)</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🔍 Consulta de Catálogo")
    
    with st.form(key="search_form", clear_on_submit=False):
        user_input = st.text_input(
            "Escribe tu búsqueda o jerga futbolera:",
            placeholder="Ej: Camiseta de Chelsea 2015-16 away"
        )
        submit_button = st.form_submit_button("Buscar camisetas ⚽", use_container_width=True)

# --- COLUMNA DERECHA: Resultados de la Última Búsqueda ---
with col_right:
    st.subheader("📦 Resultados de la Búsqueda")
    
    results_placeholder = st.container()

    if submit_button and user_input.strip():
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        with results_placeholder:
            with st.spinner("El camisetero está consultando la API..."):
                try:
                    client = get_groq_client()
                    max_turns = 3
                    turns = 0
                    finalized = False
                    
                    while turns < max_turns:
                        turns += 1
                        
                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=st.session_state.messages,
                            tools=tools,
                            tool_choice="auto",
                            temperature=0.2
                        )
                        
                        response_message = response.choices[0].message
                        tool_calls = response_message.tool_calls

                        if not tool_calls:
                            final_text = response_message.content or "Aquí tienes la información solicitada."
                            st.session_state.messages.append({"role": "assistant", "content": final_text})
                            finalized = True
                            break

                        assistant_msg = {
                            "role": "assistant",
                            "content": response_message.content,
                            "tool_calls": [
                                {
                                    "id": tc.id,
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments
                                    }
                                } for tc in tool_calls
                            ]
                        }
                        st.session_state.messages.append(assistant_msg)

                        for tool_call in tool_calls:
                            function_name = tool_call.function.name
                            function_args = json.loads(tool_call.function.arguments)
                            
                            st.info(f"🤖 **Ejecutando consulta:** `{function_name}` con parámetros: `{function_args}`")
                            
                            if function_name == "search_products":
                                tool_output = search_products(**function_args)
                            elif function_name == "get_products_by_team":
                                tool_output = get_products_by_team(**function_args)
                            else:
                                tool_output = {"error": "Función no encontrada"}

                            st.session_state.messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(tool_output)
                            })

                    if not finalized:
                        forced_messages = st.session_state.messages + [
                            {
                                "role": "user",
                                "content": "Basándote exclusivamente en los resultados obtenidos arriba por las herramientas, redacta tu respuesta comercial final en texto para el usuario."
                            }
                        ]
                        
                        final_response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=forced_messages
                        )
                        
                        final_text = final_response.choices[0].message.content or "No se encontraron resultados exactos."
                        st.session_state.messages.append({"role": "assistant", "content": final_text})

                except Exception as e:
                    error_msg = f"⚠️ **Error en el sistema:** No se pudo procesar la consulta correctamente ({str(e)})."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Renderizar únicamente los mensajes de la búsqueda actual
    with results_placeholder:
        if "messages" in st.session_state:
            for message in st.session_state.messages:
                if message["role"] in ["user", "assistant"] and message.get("content"):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])