# Feedback con LLM

**Versión preliminar — ejecución local**

## Descripción
`Feedback con LLM` es un sistema **end‑to‑end** que permite a los usuarios enviar su feedback en texto, procesarlo con un Large Language Model a través de **Groq** y recibir una respuesta personalizada. El feedback y la respuesta se almacenan en **PostgreSQL**, y el histórico se muestra mediante una interfaz sencilla en **Streamlit**.

> Las fases 0‑4 están implementadas y funcionan en local. Las fases 5‑7 están planificadas como trabajo futuro.

## Tabla de contenidos
- [Características](#características)
- [Stack tecnológico](#stack-tecnológico)
- [Arquitectura](#arquitectura)
- [Primeros pasos](#primeros-pasos)
- [Endpoints](#endpoints)
- [Variables de entorno](#variables-de-entorno)
- [Roadmap](#roadmap)
- [Próximos pasos](#próximos-pasos)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Características
- API REST con **Flask** (`/feedback`, `/history`).
- Integración con **Llama‑3 70B** a través del SDK de Groq.
- Persistencia de datos en **PostgreSQL** (contenedor Docker).
- Interfaz **Streamlit** con indicador de carga y listado histórico.

## Stack tecnológico

| Capa        | Tecnología                       |
|-------------|----------------------------------|
| LLM         | Groq SDK + Meta Llama‑3 70B      |
| Backend     | Python 3.12, Flask               |
| Base de datos | PostgreSQL 16 (Docker)         |
| Frontend    | Streamlit ≥ 1.34                 |
| Dev‑Ops     | Docker & docker‑compose          |


## Primeros pasos

### Prerrequisitos
- **Docker** ≥ 24  
- **Python** ≥ 3.12  
- Cuenta en **Groq** con `GROQ_API_KEY` válida.

### Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/xdelrey/feedback.git
cd feedback

# 2. Crea y activa el entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.\.venv\Scripts\Activate.ps1      # Windows PowerShell

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Copia las variables de entorno de ejemplo
cp .env.example .env
# -- Rellena GROQ_API_KEY y GROQ_MODEL si procede

# 5. Levanta PostgreSQL
docker compose up -d db
```

### Ejecución en local

En una terminal (entorno activo):

```bash
python backend/app.py
# Flask escuchará en http://127.0.0.1:8000
```

En otra terminal:

```bash
# La app front se comunica con el backend mediante esta variable
export BACKEND_URL=http://127.0.0.1:8000    # Windows: setx BACKEND_URL ...
streamlit run frontend/app.py
```

Abre `http://localhost:8501` en tu navegador favorito.

## Endpoints

| Método | Ruta        | Body                      | Descripción                                        |
|--------|-------------|---------------------------|----------------------------------------------------|
| POST   | `/feedback` | `{ "texto": "..." }`      | Envía feedback y recibe respuesta generada por LLM |
| GET    | `/history`  | –                         | Devuelve listado de feedbacks y respuestas         |

### Ejemplo `curl`

```bash
curl -X POST http://127.0.0.1:8000/feedback      -H "Content-Type: application/json"      -d '{"texto":"La interfaz se cuelga al guardar."}'
```

## Variables de entorno

| Variable       | Obligatoria | Descripción                                        |
|----------------|-------------|----------------------------------------------------|
| `GROQ_API_KEY` | ✓           | API key de Groq                                    |
| `GROQ_MODEL`   |             | Modelo LLM (`meta-llama-3.3-70b` por defecto)      |
| `BACKEND_URL`  | ✓ (frontend)| URL base del backend utilizada por Streamlit       |

## Roadmap

- [x] **Fase 0** – Setup & Alcance  
- [x] **Fase 1** – Endpoint `/feedback`  
- [x] **Fase 2** – Integración LLM  
- [x] **Fase 3** – Persistencia PostgreSQL  
- [x] **Fase 4** – Frontend Streamlit  
- [ ] **Fase 5** – Prompt Engineering  
- [ ] **Fase 6** – Moderación & Validación  
- [ ] **Fase 7** – Docker multi‑stage & Deploy  

## Próximos pasos
- Afinar prompts y registrar resultados (CSV).  
- Implementar filtros de moderación y protección contra spam.  
- Empaquetar todo en una sola imagen Docker y desplegar en Render/AWS.  

## Licencia
Distribuido bajo la licencia MIT — ver `LICENSE` para más detalles.<br>
Xabi del Rey - Product Manager y Bootcamper<br>
https://www.linkedin.com/in/xabidelrey/