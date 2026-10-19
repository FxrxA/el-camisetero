⚽ El Camisetero — Asistente Comercial Agéntico en Tiempo Real

El Camisetero es un asistente conversacional agéntico desarrollado para la búsqueda, traducción de jerga futbolera y recomendación en tiempo real de productos dentro del catálogo de Classic Football Shirts.
Construido utilizando Groq para el razonamiento y function calling, junto con la API de Parse.bot y respaldo local híbrido para la consulta de productos, y Streamlit para la interfaz gráfica.

🚀 Características Principales

* **Traducción de Jerga Futbolera:** Interpreta consultas informales o históricas (ej: "la de los invictos del Arsenal", "la de la novena del Madrid") y las traduce a parámetros de búsqueda precisos.
* **Flujo Agéntico con Function Calling:** Invocación autónoma de herramientas de catálogo (`search_products` y `get_products_by_team`) mediante llamadas iterativas.
* **Resiliencia e Integración Híbrida:** Sistema de respaldo automático en caso de fallos de red o de la API externa para garantizar continuidad operativa.
* **Formato Comercial Completo:** Presenta información detallada con precios, descripciones y disponibilidad de stock.

🛠️ Arquitectura y Tecnologías

* **Lenguaje:** Python 3.14
* **LLM / Backend AI:** Groq API
* **API de Productos:** Parse.bot API con capa híbrida de respaldo local
* **Frontend / UI:** Streamlit (Layout personalizado)
* **Testing:** Pytest (Suite automatizada)

📁 Estructura del Proyecto

.
├── agent_core.py       # Lógica del agente y configuración del modelo
├── agent_tools.py      # Funciones wrapper con manejo explícito de errores y respaldo
├── streamlit_app.py    # Interfaz de usuario Streamlit y ciclo agéntico
├── TESTING.md          # Documentación formal de casos de prueba
├── tests/
│   └── test_agent.py   # Pruebas automatizadas con pytest
├── .streamlit/
│   ├── secrets.toml    # Configuración de secretos y API keys (local)
│   └── config.toml     # Configuración del tema de Streamlit
└── README.md           # Documentación del proyecto

💻 Instalación y Ejecución Local

1. Requisitos Previos
Asegúrate de contar con las librerías necesarias:

```bash
pip install streamlit groq requests pytest
