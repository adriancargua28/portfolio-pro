# ENTREGA CONVOCATORIA MAYO

## Datos

* Nombre: Adrian Cargua
* Titulación: Ingeniería en Informática
* Cuenta en laboratorios: acargua
* Cuenta URJC: a.cargua
* Vídeo básico (URL): [pendiente]
* Vídeo parte opcional (URL): [pendiente]
* Despliegue (URL): [pendiente]
* Usuarios y contraseñas: alice/alice1234, bob/bob1234
* Cuenta Admin Site: admin/admin1234

## Recursos y métodos HTTP

* Recurso: /
* Métodos permitidos: GET

* Recurso: /about/
* Métodos permitidos: GET

* Recurso: /register/
* Métodos permitidos: GET, POST

* Recurso: /login/
* Métodos permitidos: GET, POST

* Recurso: /logout/
* Métodos permitidos: GET

* Recurso: /conversations/
* Métodos permitidos: GET

* Recurso: /conversations/new/
* Métodos permitidos: GET, POST

* Recurso: /conversations/<id>/
* Métodos permitidos: GET

* Recurso: /conversations/<id>/send/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/stream/
* Métodos permitidos: GET (SSE)

* Recurso: /conversations/<id>/rename/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/archive/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/pin/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/delete/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/change-model/
* Métodos permitidos: POST

* Recurso: /conversations/<id>/export/
* Métodos permitidos: GET

* Recurso: /messages/<id>/feedback/
* Métodos permitidos: POST

* Recurso: /metrics/
* Métodos permitidos: GET

* Recurso: /admin/
* Métodos permitidos: GET, POST

## Resumen parte obligatoria

Aplicación de chat con LLM construida con Django 6, HTMX y Bootstrap 5. Permite a los usuarios registrarse, crear conversaciones con modelos LLM gratuitos de NVIDIA Build, enviar mensajes con streaming en tiempo real mediante SSE, y gestionar su historial de conversaciones. Incluye Admin Site con gestión completa de conversaciones y mensajes, y página de información.

## Lista partes opcionales

* Favicon del sitio: emoji 💬 como favicon SVG inline
* Soporte multi-chat avanzado: renombrado inline con HTMX, archivado, fijado de chats y búsqueda por título o contenido
* Streaming real de tokens: SSE con EventSource en el cliente y StreamingHttpResponse en Django
* Selector de modelo LLM: desplegable por conversación guardado en base de datos, cambiable en tiempo real con HTMX
* Contexto enriquecido: panel colapsable para añadir fragmentos de texto al prompt (máx. 2000 caracteres)
* Evaluación de respuestas: botones like/dislike con HTMX y panel de métricas en Admin Site y vista dedicada
* Exportación de conversaciones: descarga en formato Markdown y JSON
