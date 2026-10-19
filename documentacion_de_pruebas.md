# ⚽ El Camisetero - Documentación de Pruebas y Validación (TESTING.md)

Este documento detalla la estrategia de pruebas automatizadas y manuales implementada para el agente e-commerce **El Camisetero**, verificando el correcto funcionamiento del flujo end-to-end, el manejo de excepciones y la desacoplación arquitectónica.

---

## 1. Cobertura de Requisitos del Checklist (Practitioner)

| Criterio Evaluado | Estado | Implementación / Evidencia |
| :--- | :---: | :--- |
| **1. Integración Real** | ✅ | Conector HTTP a la API de Parse.bot en `agent_tools.py` con sistema de fallback inteligente. |
| **2. Manejo Explícito de Errores** | ✅ | Control de timeouts, respuestas no-200, errores de autenticación (401) y fallos del servicio LLM. |
| **3. Credenciales Seguras** | ✅ | Uso exclusivo de `os.getenv` y `st.secrets`. Ninguna API Key expuesta en el código o commits. |
| **4. Caso de Prueba / Pruebas Automatizadas** | ✅ | Suite de pruebas con `pytest` pasando al 100% + guía de prueba manual end-to-end. |
| **5. Separación de Lógica / Prompts** | ✅ | Arquitectura modularizada: `streamlit_app.py` (UI), `agent_core.py` (Agente/Prompts) y `agent_tools.py` (Herramientas). |

---

## 2. Pruebas Automatizadas (Unitarias e Integración)

Las pruebas unitarias están definidas en la carpeta `tests/test_agent.py` utilizando el framework **`pytest`**.

### Casos de Prueba Cubiertos:
1. `test_search_products_fallback()`:
   * **Objetivo:** Verificar que ante la indisponibilidad o fallo de red de la API externa, la herramienta active el mecanismo de respaldo local sin romper el flujo del agente.
   * **Resultado esperado:** Retorna un diccionario con estado `"success"` y productos válidos.

2. `test_get_parse_bot_key()`:
   * **Objetivo:** Confirmar que la extracción de credenciales prioriza fuentes seguras de variables de entorno y secretos sin arrojar excepciones no controladas.
   * **Resultado esperado:** Retorna un valor tipo string seguro.

### Instrucciones de Ejecución de Pruebas

Para ejecutar la suite de pruebas unitarias desde la raíz del proyecto:

```bash
python -m pytest tests/test_agent.py
```

**Resultado de ejecución esperado:**
```text
 collected 2 items

 tests/test_agent.py ..                                                 [100%]

 ========================== 2 passed in 1.47s ==========================
```

---

## 3. Flujo de Prueba Manual End-to-End (E2E)

Para validar el funcionamiento completo de la interfaz y la integración con la IA, siga el siguiente procedimiento manual:

### Paso 1: Configuración del Entorno
Asegúrese de contar con las claves configuradas en `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_tu_clave_real"
PARSE_BOT_API_KEY = "tu_clave_parse_bot"
```

### Paso 2: Inicio de la Aplicación
Ejecute el servidor de Streamlit:
```bash
python -m streamlit run streamlit_app.py
```

### Paso 3: Escenarios de Consulta Probados
1. **Búsqueda por Equipo:**
   * *Entrada:* `"Camiseta del Chelsea actual"`
   * *Comportamiento:* El agente invoca `search_products(query='Chelsea')`, procesa los resultados y formatea una respuesta comercial clara con el modelo, precio y detalles.
2. **Búsqueda por Jugador/Leyenda:**
   * *Entrada:* `"Camiseta de Iniesta"`
   * *Comportamiento:* El agente identifica el jugador, realiza la llamada a las herramientas de catálogo y presenta la camiseta retro/homenaje correspondiente.
3. **Respuesta ante Fallo de Credenciales:**
   * *Escenario:* Clave API revocada o ausente.
   * *Comportamiento:* La aplicación captura la excepción `401 / Invalid API Key` y muestra un mensaje amigable al usuario indicando el problema sin colapsar la interfaz.

---

## 4. Estructura de Archivos del Proyecto

```text
.
├── .streamlit/
│   └── secrets.toml          # Credenciales locales (no commit en git)
├── tests/
│   └── test_agent.py         # Tests automatizados (pytest)
├── agent_core.py             # Configuración del LLM (Groq), prompts y orquestación
├── agent_tools.py            # Integración a APIs externas, fallback y manejo de errores
├── streamlit_app.py          # Interfaz de usuario y chat interactivo
├── pytest.ini                # Exclusión de directorios del sistema para pytest
└── TESTING.md                # Documentación del plan de pruebas
```