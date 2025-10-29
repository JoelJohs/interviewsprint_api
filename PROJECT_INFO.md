
# InterviewSprint — Backend API

## Descripción general del proyecto

InterviewSprint es una aplicación para gestionar planes de estudio técnicos personalizados. Este repositorio contiene el **backend API** que expone endpoints REST para que clientes (web/móvil) puedan rastrear la confianza del usuario por tema, registrar progreso y obtener sesiones de estudio personalizadas.

**Por qué este backend funciona**: demuestra diseño de APIs escalables, integración con Firebase (Firestore + Auth), implementación de algoritmos (repetición espaciada) y arquitectura modular en Python.

## Alcance de este repositorio (Backend únicamente)

Este proyecto se enfoca **exclusivamente en el backend**:
- API REST construida con FastAPI
- Integración con Firebase (Firestore para base de datos, Firebase Auth para autenticación)
- Algoritmo de repetición espaciada para recomendar temas
- Arquitectura modular: controllers → services → repositories
- Tests unitarios y documentación OpenAPI

Los clientes (web React, móvil React Native) consumirán esta API pero **no están incluidos en este repositorio**.

## Enfoque de diseño

- **Prioridad**: backend primero, porque es la capa que conecta todos los clientes.
- **Estilo de entrega**: principalmente pasos y consejos; evitar código salvo para casos raros o situaciones poco comunes.
- **Arquitectura**: modular y escalable (separación en capas: API, servicios, repositorios).
- **Base de datos**: Firebase Firestore para sincronización en tiempo real entre clientes.
- **Autenticación**: Firebase Authentication.

## Objetivos del MVP (Backend)

1. **API REST (FastAPI)** que expone endpoints para: obtener temas, registrar progreso, generar sesión diaria, autenticar usuarios.
2. **Algoritmo de repetición espaciada**: función que prioriza temas según confianza, fecha de última revisión y streak.
3. **Integración con Firestore**: CRUD sobre colecciones `users`, `topics`, `user_progress`.
4. **Autenticación**: middleware que valida tokens de Firebase Auth en cada request protegido.
5. **Documentación**: OpenAPI generada automáticamente por FastAPI.

## Componentes del Backend y habilidades demostradas

### API REST (FastAPI)

- Endpoints para CRUD de temas, progreso y sesiones.
- Middleware de autenticación que valida tokens de Firebase.
- Manejo de errores HTTP (400, 401, 404, 500) con mensajes descriptivos.
- Documentación automática OpenAPI (/docs).
- CORS configurado para permitir requests desde clientes web/móvil.

### Algoritmo de repetición espaciada

- Función principal que calcula prioridad por tema basada en: `confidence_level`, `last_reviewed_at`, `streak`.
- Uso de generadores (`yield`) para construir sesiones de forma lazy y permitir streaming/paginación.
- Estructuras de datos eficientes: dicts para acceso O(1) por `topic_id`.
- Tests unitarios: happy path + casos borde (usuario nuevo sin progreso, temas no revisados en >30 días).

### Integración con Firebase

- **Firestore**: repositorio que encapsula acceso a colecciones (`users`, `topics`, `user_progress`).
- **Firebase Auth**: verificación de tokens JWT en middleware.
- **Config centralizada**: `config.py` carga credenciales desde variable de entorno o archivo JSON.
- Manejo seguro de I/O: context managers (`with`) para operaciones de carga de datos iniciales.

### Arquitectura modular (capas)

- **Controllers** (`app/api/`): handlers HTTP (reciben request, validan input, llaman servicios, devuelven response).
- **Services** (`app/services/`): lógica de negocio (algoritmo de recomendación, validaciones complejas).
- **Repositories** (`app/repositories/`): acceso a Firestore (queries, CRUD).
- **Models** (`app/models/`): schemas Pydantic para validación de inputs/outputs.
- **Config** (`app/config.py`): inicialización de Firebase, variables de entorno.

## Esquema de base de datos (Firestore)

### Colecciones principales

**users**: `users/{userId}`
- `email`: string
- `display_name`: string (opcional)
- `created_at`: timestamp
- `last_login`: timestamp

**topics**: `topics/{topicId}`
- `name`: string (ej. "Closures en JavaScript")
- `category`: string (ej. "JavaScript", "Python", "Algoritmos")
- `difficulty`: string (ej. "Baja", "Media", "Alta")
- `description`: string (opcional)
- `created_at`: timestamp

**user_progress**: `user_progress/{userId}/progress/{topicId}`
- `confidence_level`: int (1=Baja, 2=Media, 3=Alta)
- `last_reviewed_at`: timestamp
- `streak`: int (días consecutivos estudiando este tema)
- `total_reviews`: int
- `correct_count`: int
- `incorrect_count`: int

### Consultas clave (conceptual)

- Obtener temas con confianza baja para un usuario:
  - Query: `user_progress/{userId}/progress` WHERE `confidence_level == 1`
- Obtener temas no revisados en >7 días:
  - Query: `user_progress/{userId}/progress` WHERE `last_reviewed_at < (NOW - 7 days)`
- Para usuarios nuevos sin progreso: tratar temas como confianza=1 (Baja) por defecto.

## Contrato de la API (endpoints principales)

### 1. GET /api/v1/topics

**Descripción**: Obtiene la lista de temas disponibles.

**Query params**:

- `category` (opcional): filtrar por categoría (ej. "JavaScript", "Python")
- `difficulty` (opcional): filtrar por dificultad ("Baja", "Media", "Alta")

**Response 200**:

```json
{
  "topics": [
    {
      "id": "topic_123",
      "name": "Closures en JavaScript",
      "category": "JavaScript",
      "difficulty": "Media",
      "description": "..."
    }
  ]
}
```

**Errores**: 401 (no autenticado), 500 (error interno)

---

### 2. POST /api/v1/sessions/today

**Descripción**: Genera la sesión diaria de estudio para el usuario autenticado.

**Headers**: `Authorization: Bearer <firebase_token>`

**Request body**:

```json
{
  "limit": 5
}
```

**Response 200**:

```json
{
  "session_id": "session_abc",
  "items": [
    {
      "topic_id": "topic_123",
      "topic_name": "Closures en JavaScript",
      "question": "¿Qué es un closure?",
      "priority": 8.5
    }
  ]
}
```

**Errores**: 401 (no autenticado), 400 (payload inválido), 500 (error interno)

---

### 3. POST /api/v1/progress

**Descripción**: Registra el progreso del usuario en un tema específico.

**Headers**: `Authorization: Bearer <firebase_token>`

**Request body**:

```json
{
  "topic_id": "topic_123",
  "result": "correct",
  "new_confidence_level": 2
}
```

**Response 200**:

```json
{
  "message": "Progress updated successfully",
  "updated_progress": {
    "topic_id": "topic_123",
    "confidence_level": 2,
    "streak": 3,
    "last_reviewed_at": "2025-10-29T12:00:00Z"
  }
}
```

**Errores**: 401 (no autenticado), 404 (tema no encontrado), 400 (payload inválido), 500 (error interno)

---

### 4. GET /api/v1/users/me

**Descripción**: Obtiene información del usuario autenticado.

**Headers**: `Authorization: Bearer <firebase_token>`

**Response 200**:

```json
{
  "user_id": "user_xyz",
  "email": "user@example.com",
  "display_name": "John Doe",
  "created_at": "2025-01-15T10:00:00Z"
}
```

**Errores**: 401 (no autenticado), 500 (error interno)

## Algoritmo de repetición espaciada (detalles técnicos)

### Función principal: `calculate_topic_priority(topic, user_progress)`

**Inputs**:

- `topic`: objeto con `id`, `difficulty`
- `user_progress`: objeto con `confidence_level`, `last_reviewed_at`, `streak` (puede ser None para usuarios nuevos)

**Output**: float (prioridad, mayor = más urgente estudiar)

**Lógica conceptual**:

1. Si `user_progress` es None (tema nunca estudiado): prioridad base = 10.0
2. Si `confidence_level == 1` (Baja): prioridad base = 8.0
3. Si `confidence_level == 2` (Media): prioridad base = 5.0
4. Si `confidence_level == 3` (Alta): prioridad base = 2.0
5. Ajustar según días desde última revisión:
   - Si `last_reviewed_at` > 7 días: +3.0
   - Si `last_reviewed_at` > 14 días: +5.0
   - Si `last_reviewed_at` > 30 días: +8.0
6. Ajustar según streak:
   - Si streak == 0: +1.0 (motivar a retomar)
   - Si streak > 5: -1.0 (ya tiene momentum)
7. Devolver prioridad final.

**Uso de generadores**:

La función `generate_daily_session(user_id, limit=5)` debe usar `yield` para construir la lista de temas de forma lazy:

```python
def generate_daily_session(user_id, limit=5):
    topics = get_all_topics()
    progress_map = get_user_progress_map(user_id)
    
    priorities = []
    for topic in topics:
        progress = progress_map.get(topic.id)
        priority = calculate_topic_priority(topic, progress)
        priorities.append((priority, topic))
    
    # Ordenar por prioridad (mayor primero)
    priorities.sort(reverse=True, key=lambda x: x[0])
    
    # Yield los top N
    for i, (priority, topic) in enumerate(priorities):
        if i >= limit:
            break
        yield {
            "topic_id": topic.id,
            "topic_name": topic.name,
            "priority": priority
        }
```

**Casos borde a testear**:

1. Usuario nuevo (sin progreso): todos los temas deben tener prioridad alta.
2. Todos los temas con confianza=3 y revisados ayer: prioridades bajas.
3. Un tema no revisado en 60 días: debe aparecer primero.

## Arquitectura técnica recomendada

### Stack tecnológico

- **Framework**: FastAPI (rendimiento, documentación OpenAPI automática, async/await nativo)
- **Base de datos**: Firebase Firestore (sincronización en tiempo real, SDK robusto)
- **Autenticación**: Firebase Authentication (tokens JWT validados en middleware)
- **Testing**: pytest + pytest-asyncio
- **Linting/Formatting**: flake8 + black (opcional)
- **Variables de entorno**: python-dotenv o variables del sistema

### Separación en capas (modular)

```text
app/
├── api/               # Controllers (endpoints HTTP)
│   ├── __init__.py
│   ├── topics.py      # GET /topics
│   ├── sessions.py    # POST /sessions/today
│   ├── progress.py    # POST /progress
│   └── users.py       # GET /users/me
├── services/          # Lógica de negocio
│   ├── __init__.py
│   ├── recommendation_service.py  # Algoritmo repetición espaciada
│   └── progress_service.py
├── repositories/      # Acceso a Firestore
│   ├── __init__.py
│   ├── topic_repository.py
│   ├── user_repository.py
│   └── progress_repository.py
├── models/            # Schemas Pydantic
│   ├── __init__.py
│   ├── topic.py
│   ├── user.py
│   └── session.py
├── middleware/        # Autenticación, CORS, logging
│   ├── __init__.py
│   └── auth.py
├── config.py          # Inicialización Firebase, env vars
└── main.py            # Entry point FastAPI
```

### Configuración (`config.py`)

- Cargar credenciales de Firebase desde variable de entorno `FIREBASE_CREDENTIALS` (ruta al JSON) o `GOOGLE_APPLICATION_CREDENTIALS`.
- Inicializar Firebase una sola vez (evitar re-inicialización).
- Devolver cliente Firestore para uso en repositorios.
- Usar logging en vez de prints.

## Prácticas recomendadas (guía de implementación)

- **Separación de responsabilidades**: evitar colocar lógica de negocio en handlers HTTP; delegar a servicios.
- **Contratos estables**: mantener inputs/outputs pequeños y estables; versionar la API (`/api/v1/`).
- **Tests unitarios**: escribir tests para el algoritmo de recomendación (happy path + 2 casos borde: sin progreso, progreso muy antiguo).
- **Manejo de errores**: usar excepciones personalizadas y mapearlas a códigos HTTP apropiados (400, 401, 404, 500).
- **Logging**: usar `logging` module en vez de prints; nivel INFO para flujo normal, ERROR para excepciones.
- **Variables de entorno**: nunca hardcodear credenciales; usar `.env` y python-dotenv o variables del sistema.
- **CI/CD**: pipeline que corre tests y chequeos estáticos (flake8/black opcional).

## Git y flujo de trabajo

- Usar ramas `feature/nombre-feature` para nuevas funcionalidades.
- Pull Requests a `main` con revisión de código.
- Revertir errores en `main` con `git revert` (seguro, mantiene historial).
- Limpiar historia local con `git reset` en feature branches antes de PR (opcional).
- `.gitignore` debe incluir: `serviceAccountKey.json`, `.env`, `__pycache__/`, `*.pyc`, `venv/`.

## Entregables del MVP

- `README.md` con instrucciones de setup (instalación, variables de entorno, Firebase setup, correr local).
- Endpoints documentados (OpenAPI en `/docs` gracias a FastAPI).
- Tests unitarios para el algoritmo (`tests/test_recommendation_service.py`).
- Script de seed para colección `topics` (`scripts/seed_topics.py`).
- `.gitignore` actualizado.
- `requirements.txt` con dependencias.

## Casos borde y consideraciones

- **Usuarios nuevos**: tratar temas no revisados como confianza=1 (Baja) por defecto.
- **Grandes catálogos**: paginar `GET /topics` con query params `limit` y `offset`.
- **Queries Firestore**: usar índices compuestos si se filtran múltiples campos.
- **Tokens expirados**: el middleware debe devolver 401 y mensaje claro ("Token expired").
- **Concurrencia**: Firestore maneja transacciones; usar cuando se actualice progreso para evitar race conditions.

## Notas finales

- En su mayoría: dar pasos, consejos y diseño; evitar incluir código en este documento salvo para ejemplos muy específicos.
- Mantener la lógica de negocio en servicios y el acceso a Firebase en repositorios (separación de capas).
- Preferir claridad y documentación sobre micro-optimizaciones tempranas.

---

_Documento de referencia rápida: usar como guía del proyecto backend y como checklist de implementación._
