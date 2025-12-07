# Copilot Assisted Order Management Tool — Documentación Técnica (ES)

Nota rápida (2025-09-19): el README en inglés (`README.md`) fue actualizado con un resumen de la carpeta `solutions/New_app_manamegent_tool_v2`, enlace directo a `docs/architecture.svg` y pasos de empaquetado/importe mediante `pac`. Este documento en español sigue siendo válido a nivel conceptual; para comandos más recientes consulte también `README.md`.

## Recursos y Programas de Desarrolladores
- Programa para Desarrolladores de Microsoft 365 (FAQ): https://learn.microsoft.com/en-us/office/developer-program/microsoft-365-developer-program-faq
- Requisitos y licenciamiento de Copilot Studio: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions

## 1. Propósito y Alcance
La solución “Copilot Assisted Order Management Tool” es una aplicación basada en Microsoft Power Platform diseñada para gestionar el ciclo de vida de pedidos (orders) mediante dos experiencias complementarias:
- Una aplicación Canvas para interacción visual (alta, consulta, actualización y eliminación de pedidos).
- Un asistente conversacional creado con Copilot Studio que permite a usuarios finales ejecutar tareas naturales como “crear un nuevo pedido”, “listar pedidos” o “actualizar el estado de un pedido” empleando lenguaje natural.

El objetivo principal es acelerar operaciones de backoffice y frontoffice, reducir tiempos de respuesta y mejorar la usabilidad mediante automatización, UI low-code y experiencias conversacionales, manteniendo un modelo de datos centralizado en Dataverse.

## 2. Visión de Alto Nivel y Arquitectura
[Ver diagrama de arquitectura](./docs/architecture.svg)

La solución está empaquetada como un “Solution Package” de Power Platform (versión 1.0.0.1, ver `CopilotAssistedMangementTool_1_0_0_1.zip`). Estructuralmente, el repositorio incluye:
- Canvas App empaquetada (`CanvasApps/…/cr039_copilotassistantmanagementtool_59e71_DocumentUri.msapp`).
- Bot de Copilot Studio (carpeta `botcomponents/` y `bots/Default_Agent7/`) con tópicos e “acciones” conectadas a Dataverse.
- Flujos y componentes de Power Automate/Dataverse (carpetas `Workflows/`, `Assets/`, `dvtablesearchentities/`, `dvtablesearchs/`).
- Archivos de solución (`[Content_Types].xml`, `solution.xml`, `customizations.xml`) y referencias de conexión.
- Dataset de ejemplo `orders.xlsx` (opcional para carga inicial de datos).

Flujo de datos típico:
1. El usuario crea o consulta pedidos desde la Canvas App o a través de Copilot.
2. Las operaciones CRUD se resuelven contra tablas de Dataverse mediante conectores nativos.
3. Opcionalmente, Power Automate puede orquestar validaciones, notificaciones o integraciones externas.
4. El asistente emplea tópicos (Greeting, ConversationStart, CreatenewOrder, Search, Update, Delete, etc.) y acciones generadas (CreateRecord, ListRecords, GetItem, UpdateRecord, DeleteRecord) para traducir la intención del usuario en operaciones sobre Dataverse.

Beneficios clave:
- Menor fricción para usuarios no técnicos.
- Gobierno y seguridad centralizados en Dataverse.
- Despliegue repetible entre entornos mediante soluciones administradas.

## 3. Tecnologías y Componentes
- Microsoft Power Platform
  - Power Apps (Canvas): UI low-code para gestión de pedidos.
  - Copilot Studio: asistente conversacional con tópicos, entidades y acciones vinculadas a Dataverse.
  - Dataverse: almacenamiento transaccional, seguridad basada en roles, auditoría.
  - Power Automate: lógica de negocio, automatización y orquestación (si aplica en su entorno).
- Conectores y Referencias de Conexión: enlaces a Dataverse definidos como “Connection References” dentro de la solución.
- DVT Search (dvtablesearch*): definiciones de búsqueda/tablas virtuales optimizadas para descubrimiento de datos.
- Herramientas ALM:
  - Power Platform CLI (`pac`) para importar/exportar soluciones y gestionar conexiones.
  - Solution Checker y Analytics (opcional) para calidad y observabilidad.

## 4. Modelo de Datos (Dataverse)
La solución asume una tabla de pedidos (p. ej., `cr039_order` o similar, el nombre exacto puede variar según el entorno) con atributos típicos como:
- Número de pedido, cliente, fecha, estado, importe, línea(s) de producto.
- Metadatos de seguimiento: creado por, modificado por, marca temporal.

Si parte de cero, puede:
- Importar la solución para provisionar tablas y metadatos.
- Cargar datos de ejemplo desde `orders.xlsx` usando la funcionalidad de importación de Dataverse (Power Apps Maker) o un dataflow.

## 5. Preparación del Entorno
Antes de configurar/desplegar:
- Licencias: Asegúrese de contar con licencias de Power Apps/Power Automate/Copilot Studio/Dataverse adecuadas.
- Entorno: Use entornos dedicados (Dev/Test/Prod) en Power Platform.
- Permisos: Rol de Maker/Administrador para importar soluciones y configurar conexiones.
- Herramientas: Instale Power Platform CLI (Windows).
  - Descarga: https://aka.ms/pac/cli
  - Verificación en CMD:
    ```cmd
    pac --version
    ```

## 6. Configuración Inicial (Importación de la Solución)
Existen dos caminos: Centro de Administración/Maker Portal (UI) o CLI. La solución empaquetada está en la raíz del repositorio: `CopilotAssistedMangementTool_1_0_0_1.zip`.

### 6.1. Importación vía Portal (UI)
1. Inicie sesión en Power Apps (https://make.powerapps.com) con el entorno de destino.
2. Vaya a Solutions > Import > seleccione el archivo ZIP de solución.
3. Siga el asistente para:
   - Resolver referencias de conexión a Dataverse.
   - Establecer variables de entorno (si corresponden) y parámetros.
   - Completar la importación y publicar.

### 6.2. Importación vía CLI
Autentique y seleccione el entorno:
```cmd
pac auth create --url https://<su-entorno>.crm.dynamics.com --name DEV
pac auth select --name DEV
```
Importe la solución:
```cmd
pac solution import --path "CopilotAssistedMangementTool_1_0_0_1.zip" --publish-changes --activate-plugins
```
Opcionalmente, verifique componentes:
```cmd
pac solution list
pac solution checker run --solution-name <NombreDeLaSolucion>
```

## 7. Referencias de Conexión y Variables de Entorno
Durante la importación, el asistente puede solicitar crear/asociar referencias de conexión (p. ej., Dataverse). Recomendaciones:
- Use cuentas de servicio gestionadas por TI para conexiones compartidas.
- Mantenga una referencia de conexión por entorno (Dev/Test/Prod) con nombres estandarizados.
- Si la solución define variables de entorno (URLs, IDs, claves), asígnelas de forma explícita en cada entorno. Consulte `customizations.xml` y `Assets/` para identificar nombres lógicos si necesita validarlo.

## 8. Configuración de la Canvas App
La App Canvas incluida se provisiona con la solución. Tras la importación:
- Verifique que los conectores a Dataverse están resueltos.
- Publique y comparta la app con los roles/grupos adecuados.
- Si necesita modificar la UI, descargue y edite `cr039_copilotassistantmanagementtool_59e71_DocumentUri.msapp` en Power Apps Studio (preferiblemente a través del Maker Portal, ya que la solución gestiona las dependencias y recursos).

## 9. Configuración del Asistente (Copilot Studio)
El bot en `bots/Default_Agent7/` y `botcomponents/Default_Agent7.*` contiene:
- Tópicos: `Greeting`, `ConversationStart`, `CreatenewOrder`, `Search`, `Update`, `Delete`, `Fallback`, `ThankYou`, `Escalate`, `OnError`, `ResetConversation`, etc.
- Acciones: componentes generados para CRUD en Dataverse (`CreateRecord`, `ListRecords`, `GetItem`, `UpdateRecord`, `DeleteRecord`).

Tras la importación:
- Abra Copilot Studio para revisar los tópicos y el enrutamiento de intenciones.
- Verifique que las acciones estén conectadas a las tablas correctas de Dataverse.
- Ejecute pruebas de conversación con utterances representativas (p. ej., “crea un nuevo pedido para el cliente X por 200 €”).

## 10. Carga de Datos de Ejemplo (Opcional)
Puede usar `orders.xlsx` para poblar datos iniciales.
- En Power Apps (Data > Tables > Import data), seleccione la tabla de pedidos y el archivo Excel.
- Mapee columnas y valide datos obligatorios.
- Alternativamente, utilice Power Query Dataflows si requiere transformaciones.

## 11. Despliegue entre Entornos (ALM)
Buenas prácticas para mover la solución Dev → Test → Prod:
- Use soluciones administradas en Test/Prod; mantenga “desbloqueada” (unmanaged) solo en Dev.
- Versionado semántico (ej.: 1.0.0.1 → 1.0.0.2 para parches). Mantenga coherencia en `solution.xml`.
- Automatice con pipelines (Azure DevOps/GitHub Actions) usando `pac`:
  ```cmd
  pac solution export --path out\CopilotAssistedMangementTool_1_0_0_2.zip --name <NombreDeLaSolucion> --managed true --include CanvasApps --process-ConnectionReferences true
  pac solution import --path out\CopilotAssistedMangementTool_1_0_0_2.zip --publish-changes --activate-plugins
  ```
- Bloquee referencias de conexión y variables de entorno mediante plantillas por entorno.

## 12. Seguridad y Cumplimiento
- Control de Acceso Basado en Roles (RBAC): asigne roles de Dataverse que otorguen solo los privilegios mínimos (lectura/escritura sobre la tabla de pedidos según el perfil).
- DLP (Data Loss Prevention): aplique políticas que regulen conectores permitidos.
- Auditoría: habilite auditoría en tablas críticas para trazabilidad.
- Cumplimiento: valide requisitos de protección de datos (PII), retención y almacenamiento conforme a normativas internas.

## 13. Operación y Uso
- Canvas App: navegación para crear, listar y editar pedidos. Use vistas filtradas por estado y búsquedas por cliente/ID.
- Copilot: interacción natural. Ejemplos de intents:
  - “Crea un nuevo pedido para ACME por 4 unidades del SKU 1001”.
  - “Lista los pedidos abiertos de esta semana”.
  - “Actualiza el estado del pedido 12345 a Enviado”.
  - “Elimina el pedido 67890”.
- Manejo de errores: el tópico `OnError` gestiona excepciones; `Fallback` actúa ante utterances no entendidas; `Escalate` permite derivar a un humano.

## 14. Pruebas y Calidad
- Copilot Studio:
  - Pruebe tópicos con frases variadas y cobertura de bordes (valores faltantes, IDs inexistentes, conflictos).
  - Revise el enrutamiento cuando múltiples tópicos coincidan (`MultipleTopicsMatched`).
- Canvas App:
  - Use Test Studio para escenarios críticos (crear/editar/eliminar). Compruebe fórmulas y dependencias.
- Solución:
  - Ejecute Solution Checker para identificar problemas de desempeño o configuración.
- Datos:
  - Valide integridad referencial y reglas de negocio (p. ej., estados permitidos, límites numéricos).

## 15. Observabilidad y Mantenimiento
- Monitor (Canvas App): inspeccione llamadas, delegación de consultas y tiempos de respuesta.
- Analytics (Copilot): revise métricas de conversación, éxito por intención, y transcripciones para mejorar prompts y desambiguaciones.
- Alertas: configure notificaciones en Power Automate para errores críticos.
- Mantenimiento:
  - Rotación de secretos y credenciales en referencias de conexión.
  - Limpieza de tópicos obsoletos y normalización de utterances.
  - Re-evaluación de DLP y roles al introducir nuevos conectores o integraciones.

## 16. Personalización y Extensibilidad
- Campos/Tablas: amplíe el modelo de datos en Dataverse según sus requisitos (líneas de pedido, catálogos, impuestos, envíos).
- Integraciones: conecte ERP/CRM externos mediante conectores estándar o APIs personalizadas; orqueste con Power Automate.
- UX: adapte la Canvas App (temas, accesibilidad, responsive). Controle la delegación de consultas para rendimiento.
- IA: mejore prompts y estrategias de clarificación del bot. Añada entidades personalizadas para términos de negocio.

## 17. Solución de Problemas (FAQ)
- No aparecen tablas/conexiones tras importar la solución:
  - Verifique que la importación finalizó sin errores y que publicó cambios.
  - Revise las referencias de conexión: deben estar asociadas a una conexión válida en el entorno.
- El bot no entiende mis frases:
  - Aumente la cobertura de utterances en los tópicos; añada variantes y sinónimos.
  - Compruebe que las acciones están vinculadas a las tablas correctas.
- Errores al crear/actualizar pedidos:
  - Valide campos obligatorios y tipos de datos. Revise reglas de negocio y seguridad (roles/privilegios).
- Lentitud en listados:
  - Revise delegación en Canvas, índices en Dataverse y límites de página.

## 18. Comandos Útiles (CLI)
```cmd
:: Autenticación y selección de entorno
pac auth create --url https://<su-entorno>.crm.dynamics.com --name DEV
pac auth select --name DEV

:: Importar solución
pac solution import --path "CopilotAssistedMangementTool_1_0_0_1.zip" --publish-changes --activate-plugins

:: Exportar solución administrada
pac solution export --name <NombreDeLaSolucion> --managed true --path out\Solution_Managed.zip

:: Listar soluciones
pac solution list

:: Ejecutar Solution Checker
pac solution checker run --solution-name <NombreDeLaSolucion>
```

## 19. Estructura del Repositorio (Resumen)
- `Copilot_Assisted_Order_management_tool/` — Contiene la solución descomprimida (componentes de bot, Canvas App, activos, workflows).
- `CopilotAssistedMangementTool_1_0_0_1.zip` — Solución empaquetada para importación.
- `orders.xlsx` — Datos de ejemplo.
- `Readme.md` — Documentación original (en inglés u otra referencia).

## 20. Próximos Pasos
- Configurar pipelines de ALM (export/import automatizados, validaciones y promoción entre entornos).
- Completar el glosario de negocio (estados de pedido, SLA, KPIs) y reflejarlo en prompts del bot.
- Añadir notificaciones (p. ej., correo/Teams) al estado del pedido mediante Power Automate.
- Establecer métricas de éxito (tiempo de creación, precisión de intents, tasa de fallback) y revisiones periódicas.

## 21. Glosario de Términos
- Dataverse: plataforma de datos de Power Platform con seguridad basada en roles y modelos de tablas.
- Canvas App: aplicación Power Apps con diseño libre (arrastrar y soltar) y fórmulas.
- Copilot Studio: herramienta para crear asistentes conversacionales con tópicos/intents y acciones.
- Tópico (Topic): flujo conversacional que responde a una intención concreta.
- Acción: operación invocable desde tópicos (por ejemplo, CRUD sobre Dataverse).
- Solución (Solution): contenedor ALM para empaquetar y mover componentes entre entornos.
- Referencia de Conexión: recurso que vincula conectores a conexiones específicas por entorno.
- DLP: políticas de prevención de pérdida de datos aplicadas a conectores.

---

© Este documento resume la implementación técnica y operativa de la solución “Copilot Assisted Order Management Tool” en español para facilitar su adopción y mantenimiento en distintos entornos de Power Platform.
