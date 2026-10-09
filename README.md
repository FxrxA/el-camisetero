# ⚽ El Camisetero — Asistente Comercial Agéntico en Tiempo Real

**El Camisetero** es un asistente conversacional agéntico desarrollado para la búsqueda, traducción de jerga futbolera y recomendación en tiempo real de productos dentro del catálogo de **Classic Football Shirts**.

Construido utilizando **Groq (OpenAI GPT-OSS-120B)** para el razonamiento y function calling, junto con la API de **Parse.bot** para la consulta de productos en vivo y **Streamlit** para la interfaz gráfica.

---

## 🚀 Características Principales

- **Traducción de Jerga Futbolera:** Interpreta consultas informales o históricas (ej: *"la de los invictos del Arsenal"*, *"la de la novena del Madrid"*) y las traduce a parámetros de búsqueda precisos (*"Arsenal 2003-04"*).
- **Flujo Agéntico con Function Calling:** Invocación autónoma de herramientas de catálogo (`search_products` y `get_products_by_team`) mediante llamadas iterativas.
- **Consultas y Resultados en Tiempo Real:** Interfaz estilo dashboard en dos columnas (Buscador a la izquierda, Resultados detallados a la derecha).
- **Formato Comercial Completo:** Genera tablas en Markdown con nombre del producto, precio en libras (GBP), talles, disponibilidad de stock y link directo de compra.

---

## 🛠️ Arquitectura y Tecnologías

- **Lenguaje:** Python 3.14
- **LLM / Backend AI:** Groq API (`openai/gpt-oss-120b`)
- **API de Productos:** Parse.bot API (Integración en vivo con Classic Football Shirts)
- **Frontend / UI:** Streamlit (Layout personalizado en tema oscuro)

---

## 📁 Estructura del Proyecto

```text
.
├── agent_tools.py      # Funciones wrapper para interactuar con Parse.bot API
├── streamlit_app.py    # Interfaz de usuario Streamlit y ciclo agéntico
├── logo.png            # Identidad visual del asistente
├── .streamlit/
│   └── config.toml     # Configuración del tema oscuro de Streamlit
└── README.md           # Documentación del proyecto


## 💻 Instalación y Ejecución Local
1. Requisitos Previos
Asegúrate de contar con las librerías necesarias:

# Bash
pip install streamlit groq requests
2. Configurar Variables de Entorno
Configura las claves de API necesarias en tu terminal:

# DOS
set GROQ_API_KEY=gsk_TU_GROQ_API_KEY
set PARSE_BOT_API_KEY=TU_PARSE_BOT_API_KEY
3. Ejecutar la Aplicación
Inicia la interfaz de Streamlit:

# DOS
python -m streamlit run streamlit_app.py
Accede desde tu navegador web en http://localhost:8501.

## ⚽ Ejemplo de Uso
Ingresa la consulta en la caja izquierda: "Búscame la camiseta de Chelsea 2015-16 away".

El agente identificará autónomamente la consulta, ejecutará la llamada a la herramienta de Parse.bot y presentará la lista de indumentaria disponible en la columna derecha.

¡Gracias por confiar en EL CAMISETERO ⚽!