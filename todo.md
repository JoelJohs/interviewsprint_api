# InterviewSprint Backend - Todo List

## Descripción general del proyecto

InterviewSprint es una aplicación para gestionar planes de estudio técnicos personalizados. Los usuarios pueden rastrear su confianza por tema, registrar progreso y recibir sesiones de estudio diarias generadas por un algoritmo de repetición espaciada.

Este repositorio contiene el **backend API REST** que expone endpoints para clientes web y móviles, integrándose con Firebase (Firestore + Authentication).

## Descripción del backend

El backend está construido con **FastAPI** (Python) y sigue una arquitectura modular de 3 capas:

- **Controllers (API)**: Handlers HTTP que reciben requests, validan inputs y llaman servicios.
- **Services**: Lógica de negocio (algoritmo de recomendación, validaciones complejas).
- **Repositories**: Acceso a Firestore (queries, CRUD sobre colecciones `users`, `topics`, `user_progress`).

**Tecnologías**:

- FastAPI (framework web async)
- Firebase Admin SDK (Firestore + Auth)
- Pydantic (validación de schemas)
- pytest (testing)

**Endpoints principales**:

- `GET /api/v1/topics` - Obtener lista de temas (con filtros opcionales)
- `POST /api/v1/sessions/today` - Generar sesión diaria de estudio personalizada
- `POST /api/v1/progress` - Registrar progreso del usuario en un tema
- `GET /api/v1/users/me` - Obtener información del usuario autenticado

## Metas del proyecto (orden de implementación)

### Fase 1: Configuración inicial y estructura del proyecto

- [ ] **M1.1**: Crear estructura de carpetas modular (`app/api/`, `app/services/`, `app/repositories/`, `app/models/`, `app/middleware/`)
- [ ] **M1.2**: Configurar `.gitignore` (incluir `serviceAccountKey.json`, `.env`, `__pycache__/`, `*.pyc`, `venv/`)
- [ ] **M1.3**: Actualizar `requirements.txt` con dependencias (FastAPI, firebase-admin, pydantic, uvicorn, pytest, python-dotenv)
- [ ] **M1.4**: Completar `app/config.py` con función `initialize_firebase()` que cargue credenciales desde variable de entorno
- [ ] **M1.5**: Crear `README.md` con instrucciones de setup (instalación, variables de entorno, Firebase credentials, correr local)

### Fase 2: Configuración de Firebase

- [ ] **M2.1**: Crear proyecto en Firebase Console y habilitar Firestore
- [ ] **M2.2**: Habilitar Firebase Authentication (Email/Password y Google Sign-In)
- [ ] **M2.3**: Generar nueva clave de cuenta de servicio (Service Account Key) y configurar variable de entorno `FIREBASE_CREDENTIALS`
- [ ] **M2.4**: Diseñar esquema de colecciones Firestore (`users`, `topics`, `user_progress`) y documentar en `PROJECT_INFO.md`
- [ ] **M2.5**: Configurar reglas de seguridad de Firestore (usuarios solo pueden leer/escribir sus propios datos)

### Fase 3: Modelos y Schemas (Pydantic)

- [ ] **M3.1**: Crear `app/models/topic.py` con schemas `TopicBase`, `TopicCreate`, `TopicResponse`
- [ ] **M3.2**: Crear `app/models/user.py` con schemas `UserBase`, `UserResponse`
- [ ] **M3.3**: Crear `app/models/progress.py` con schemas `ProgressBase`, `ProgressCreate`, `ProgressUpdate`, `ProgressResponse`
- [ ] **M3.4**: Crear `app/models/session.py` con schemas `SessionRequest`, `SessionItem`, `SessionResponse`

### Fase 4: Repositorios (acceso a Firestore)

- [ ] **M4.1**: Crear `app/repositories/topic_repository.py` con funciones CRUD: `get_all_topics()`, `get_topic_by_id()`, `create_topic()`, `filter_topics(category, difficulty)`
- [ ] **M4.2**: Crear `app/repositories/user_repository.py` con funciones: `get_user_by_id()`, `create_user()`, `update_last_login()`
- [ ] **M4.3**: Crear `app/repositories/progress_repository.py` con funciones: `get_user_progress(user_id)`, `get_progress_by_topic(user_id, topic_id)`, `update_progress()`, `create_progress()`

### Fase 5: Servicios (lógica de negocio)

- [ ] **M5.1**: Crear `app/services/recommendation_service.py` con función `calculate_topic_priority(topic, user_progress)` (algoritmo de repetición espaciada)
- [ ] **M5.2**: Implementar generador `generate_daily_session(user_id, limit)` usando `yield` para construir sesión lazy
- [ ] **M5.3**: Crear `app/services/progress_service.py` con funciones: `update_user_progress(user_id, topic_id, result, new_confidence_level)`
- [ ] **M5.4**: Añadir lógica para calcular streak (días consecutivos estudiando un tema)

### Fase 6: Middleware y Autenticación

- [ ] **M6.1**: Crear `app/middleware/auth.py` con función `verify_firebase_token(token)` que valide JWT de Firebase Auth
- [ ] **M6.2**: Implementar dependency `get_current_user()` para FastAPI que extraiga el user_id del token
- [ ] **M6.3**: Configurar CORS en `app/main.py` para permitir requests desde clientes web/móvil
- [ ] **M6.4**: Añadir manejo global de excepciones (mapear excepciones custom a códigos HTTP 400/401/404/500)

### Fase 7: Endpoints (Controllers)

- [ ] **M7.1**: Crear `app/api/topics.py` con endpoint `GET /api/v1/topics` (con filtros opcionales `category`, `difficulty`)
- [ ] **M7.2**: Crear `app/api/sessions.py` con endpoint `POST /api/v1/sessions/today` (requiere autenticación, genera sesión diaria)
- [ ] **M7.3**: Crear `app/api/progress.py` con endpoint `POST /api/v1/progress` (requiere autenticación, registra progreso)
- [ ] **M7.4**: Crear `app/api/users.py` con endpoint `GET /api/v1/users/me` (requiere autenticación, devuelve info del usuario)
- [ ] **M7.5**: Registrar todos los routers en `app/main.py` con prefijo `/api/v1`

### Fase 8: Entry Point y Configuración de FastAPI

- [ ] **M8.1**: Completar `app/main.py` con instancia de FastAPI, configuración de CORS, registro de routers
- [ ] **M8.2**: Añadir metadata a FastAPI (título, descripción, versión) para documentación OpenAPI
- [ ] **M8.3**: Configurar logging global (nivel INFO, formato con timestamp)
- [ ] **M8.4**: Probar servidor local con `uvicorn app.main:app --reload` y verificar `/docs`

### Fase 9: Seed de datos iniciales

- [ ] **M9.1**: Crear `scripts/seed_topics.py` con lista de 20-30 temas de ejemplo (categorías: JavaScript, Python, SQL, Algoritmos, Estructuras de Datos)
- [ ] **M9.2**: Implementar función que cargue topics desde JSON/diccionario y los inserte en Firestore (colección `topics`)
- [ ] **M9.3**: Ejecutar seed y verificar que los temas aparezcan en Firestore Console

### Fase 10: Testing

- [ ] **M10.1**: Configurar `pytest` y `pytest-asyncio` en `tests/conftest.py`
- [ ] **M10.2**: Crear `tests/test_recommendation_service.py` con tests unitarios para `calculate_topic_priority()` (3 casos: happy path, usuario nuevo sin progreso, tema no revisado en >30 días)
- [ ] **M10.3**: Crear `tests/test_sessions_api.py` con tests de integración para `POST /api/v1/sessions/today` (mock Firestore con pytest fixtures)
- [ ] **M10.4**: Crear `tests/test_progress_api.py` con tests para `POST /api/v1/progress`
- [ ] **M10.5**: Ejecutar todos los tests con `pytest` y verificar coverage (objetivo: >80%)

### Fase 11: Documentación final

- [ ] **M11.1**: Completar `README.md` con secciones: Instalación, Setup de Firebase, Variables de entorno, Correr local, Correr tests, Endpoints disponibles
- [ ] **M11.2**: Documentar ejemplos de requests/responses en `README.md` (con `curl` o Postman collections)
- [ ] **M11.3**: Añadir diagrama de arquitectura (opcional, puede ser ASCII art o link a Miro/Excalidraw)
- [ ] **M11.4**: Documentar decisiones técnicas clave en `PROJECT_INFO.md` (por qué FastAPI, por qué Firestore, algoritmo de repetición espaciada)

### Fase 12: Deployment y CI/CD (opcional pero recomendado)

- [ ] **M12.1**: Crear `.github/workflows/test.yml` con pipeline que corre tests en cada push/PR
- [ ] **M12.2**: Añadir step de linting (flake8) al pipeline CI
- [ ] **M12.3**: Configurar despliegue a Cloud Run / Railway / Render (usar secrets para `FIREBASE_CREDENTIALS`)
- [ ] **M12.4**: Documentar proceso de despliegue en `README.md`

## Criterios de aceptación generales

- Todos los endpoints deben estar documentados en OpenAPI (`/docs`)
- Todos los endpoints protegidos deben validar token de Firebase Auth
- El código debe seguir convenciones PEP 8 (linting con flake8 opcional)
- Todos los servicios deben tener tests unitarios con coverage >80%
- El `README.md` debe permitir a un desarrollador nuevo levantar el proyecto en <10 minutos

## Notas para GitHub Copilot

Este documento está estructurado para que GitHub Copilot pueda generar issues automáticamente desde GitHub Web. Cada meta (`M1.1`, `M1.2`, etc.) puede convertirse en una issue con:

- **Título**: El texto después de la meta (ej. "Crear estructura de carpetas modular")
- **Descripción**: Expandir la meta con detalles técnicos, criterios de aceptación y links a documentación relevante
- **Labels**: Sugerencias: `setup`, `firebase`, `api`, `testing`, `documentation`, `deployment`
- **Milestone**: Agrupar por fase (Fase 1, Fase 2, etc.)

---

_Documento vivo: actualizar checkboxes a medida que se completen las metas._
